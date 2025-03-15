import requests
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Epic FHIR API Credentials
EPIC_CLIENT_ID = os.getenv("EPIC_CLIENT_ID")
EPIC_CLIENT_SECRET = os.getenv("EPIC_CLIENT_SECRET")
FHIR_BASE_URL = os.getenv("EPIC_FHIR_BASE_URL")
TOKEN_URL = f"{FHIR_BASE_URL}/oauth2/token"

def authenticate_user():
    """Authenticate with Epic FHIR and return an access token."""
    try:
        response = requests.post(
            TOKEN_URL,
            data={"client_id": EPIC_CLIENT_ID, "client_secret": EPIC_CLIENT_SECRET}
        )
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"❌ Authentication Error: {e}")
        return None

def fetch_beaker_report(patient_id):
    """Fetch the beaker report for a specific patient."""
    access_token = authenticate_user()
    if not access_token:
        print("❌ Unable to authenticate.")
        return

    headers = {"Authorization": f"Bearer {access_token}"}
    report_url = f"{FHIR_BASE_URL}/Patient/{patient_id}/report"
    
    try:
        response = requests.get(report_url, headers=headers)
        response.raise_for_status()
        report_data = response.json()
        return report_data
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching report for patient {patient_id}: {e}")
        return None

def process_and_save_to_csv(report):
    """Process the fetched report and save it as a CSV."""
    try:
        df = pd.DataFrame(report)
        df.to_csv("beaker_report.csv", index=False)
        print("✅ Report saved to 'beaker_report.csv'")
    except Exception as e:
        print(f"❌ Error saving report to CSV: {e}")

# Example usage (replace 'patient_id' with an actual patient ID)
patient_id = '12345'
report = fetch_beaker_report(patient_id)
if report:
    process_and_save_to_csv(report)
