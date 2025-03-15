import requests
import json
import os
import fhirclient.models.patient as p
import fhirclient.models.observation as obs
import fhirclient.models.condition as cond
from fhirclient import client
import pandas as pd
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from authlib.integrations.flask_client import OAuth
import logging
from functools import wraps
from datetime import datetime, timedelta

# Initialize Flask App for Chatbot API
app = Flask(__name__, template_folder="templates")
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')
CORS(app, supports_credentials=True)

# Logging Configuration
logging.basicConfig(level=logging.INFO)

# Epic Client ID Selection
EPIC_ENV = os.getenv('EPIC_ENV', 'non-production')
EPIC_CLIENT_ID = 'e098fdbf-3af1-4514-a08e-13cdbf4ba63c' if EPIC_ENV == 'production' else 'fa15fa9c-8443-4b22-ade7-15de5287ffcc'

app.config.update({
    'EPIC_CLIENT_ID': EPIC_CLIENT_ID,
    'EPIC_CLIENT_SECRET': os.getenv('EPIC_CLIENT_SECRET'),
    'EPIC_AUTH_URL': os.getenv('EPIC_AUTH_URL'),
    'EPIC_TOKEN_URL': os.getenv('EPIC_TOKEN_URL'),
    'EPIC_REDIRECT_URI': os.getenv('EPIC_REDIRECT_URI', 'http://localhost:5000/callback')
})

oauth = OAuth(app)
epic = oauth.register(
    name='epic',
    client_id=app.config['EPIC_CLIENT_ID'],
    client_secret=app.config['EPIC_CLIENT_SECRET'],
    authorize_url=app.config['EPIC_AUTH_URL'],
    access_token_url=app.config['EPIC_TOKEN_URL'],
    redirect_uri=app.config['EPIC_REDIRECT_URI'],
    client_kwargs={'scope': 'patient/*.read user/*.read'}
)

# Initialize FHIR Client for EPIC Integration
settings = {
    'app_id': os.getenv('FHIR_APP_ID', 'genomic_ai_integration'),
    'api_base': os.getenv('FHIR_API_BASE', 'https://epic.fhir.example.com')
}
fhir_client = client.FHIRClient(settings=settings)

# Login Route
@app.route('/login')
def login():
    logging.info("User initiated login.")
    return epic.authorize_redirect(redirect_uri=app.config['EPIC_REDIRECT_URI'])

# Callback Route
@app.route('/callback')
def callback():
    token = epic.authorize_access_token()
    session.update({
        'epic_token': token['access_token'],
        'token_expiry': datetime.utcnow() + timedelta(seconds=token.get('expires_in', 3600)),
        'user_role': token.get('user_role', 'patient'),
        'patient_id': token.get('patient', None)
    })
    logging.info(f"User logged in with role: {session.get('user_role')} and patient_id: {session.get('patient_id')}")
    return redirect(url_for('dashboard'))

# Logout Route
@app.route('/logout')
def logout():
    logging.info("User logged out.")
    session.clear()
    return redirect(url_for('dashboard'))

# Get Epic Token and Refresh if Needed
def get_epic_token():
    if 'epic_token' not in session or datetime.utcnow() > session.get('token_expiry', datetime.utcnow()):
        logging.warning("Token expired or missing. User must reauthenticate.")
        return None
    return session['epic_token']

# Role-Based Access Control Decorator
def role_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = session.get('user_role')
            if user_role not in roles:
                logging.warning(f"Access denied for role {user_role}. Required roles: {roles}")
                return jsonify({"error": "Access denied: Insufficient permissions"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Ensure Patient Data Access is Restricted to Authenticated Patients
def ensure_patient_access(patient_id):
    if session.get('user_role') == 'patient' and session.get('patient_id') != patient_id:
        logging.warning("Patient attempted to access unauthorized data.")
        return jsonify({"error": "Access denied: You can only access your own data"}), 403
    return None

# API Request Handler with Retry Mechanism
def make_api_request(endpoint, patient_id):
    restriction = ensure_patient_access(patient_id)
    if restriction:
        return restriction
    headers = {'Authorization': f'Bearer {get_epic_token()}'}
    for attempt in range(3):
        try:
            logging.info(f"Attempt {attempt + 1}: Making API request to {endpoint} for patient {patient_id}")
            response = requests.get(f"{settings['api_base']}/{endpoint}?patient={patient_id}", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"API Request attempt {attempt + 1} failed: {str(e)}")
            if attempt == 2:
                return {"error": f"API request failed after 3 attempts: {str(e)}"}

# Flask Routes for Fetching Patient Data
@app.route('/api/fetch_patient_data/<patient_id>')
@role_required(['clinician'])
def fetch_patient_data(patient_id):
    return make_api_request('Patient', patient_id)

@app.route('/api/fetch_beaker_reports/<patient_id>')
@role_required(['clinician'])
def fetch_beaker_reports(patient_id):
    return make_api_request('Observation', patient_id)

# Populate CSV with Beaker Report Data
@role_required(['researcher'])
def populate_csv_from_beaker(patient_id, output_file="beaker_report.csv"):
    beaker_data = fetch_beaker_reports(patient_id)
    if "error" in beaker_data:
        return beaker_data
    df = pd.json_normalize(beaker_data.get("entry", []))
    df.to_csv(output_file, index=False)
    logging.info(f"CSV file '{output_file}' generated successfully.")
    return f"CSV file '{output_file}' generated successfully."

# Generate Digital Twins for Mutation Analysis
@role_required(['researcher'])
def generate_digital_twin(patient_id):
    beaker_data = fetch_beaker_reports(patient_id)
    if "error" in beaker_data:
        return beaker_data
    logging.info(f"Generating digital twin for patient {patient_id}")
    digital_twin = {
        "patient_id": patient_id,
        "genomic_profile": beaker_data.get("entry", []),
        "evolution_analysis": "Pending AI-based computation",
        "characteristic_mapping": "Pending AI-based computation",
        "drug_discovery": "Pending AI-based computation"
    }
    return digital_twin

# Serve Frontend Dashboard
@app.route('/')
def dashboard():
    logging.info("Dashboard accessed.")
    return render_template("index.html")

if __name__ == "__main__":
    logging.info("Starting Flask application.")
    app.run(debug=False, threaded=True)
