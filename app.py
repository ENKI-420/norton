import streamlit as st
import requests
import pandas as pd
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from beaker_report_fetching import authenticate_user, fetch_beaker_report, process_and_save_to_csv
from fpdf import FPDF

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# EPIC API URLs
FHIR_BASE_URL = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/"

# Set up the Streamlit Page
st.set_page_config(page_title="AGENT Platform - Precision Oncology", layout="wide")

# Sidebar Navigation
st.sidebar.title("AGENT AI Platform")
option = st.sidebar.radio(
    "Select a Section",
    ["Home", "Login to Epic", "Fetch Beaker Report", "Genomic Analysis", "Clinical Trials", "Digital Twin Modeling", "Export Reports", "Chat with Mutations"]
)

# Home Section
if option == "Home":
    st.title("Welcome to the AGENT AI Platform for Precision Oncology")
    st.write("""
    The AGENT AI Platform integrates cutting-edge AI and genomic data analysis, pushing the boundaries of healthcare innovation.
    This platform helps clinicians, researchers, and data scientists with genomic analysis, clinical trial matching, 
    and digital twin modeling for precision oncology. 
    Navigate through the platform to explore personalized features and options.
    """)

# EPIC Login Section
elif option == "Login to Epic":
    st.title("Epic Login for FHIR Access")
    username = st.text_input("Epic Username")
    password = st.text_input("Epic Password", type="password")

    if st.button("Login"):
        token = authenticate_user(username, password)
        if token:
            st.session_state.auth_token = token
            st.success("Login successful! You can now fetch Beaker reports and perform analyses.")
        else:
            st.error("Authentication failed. Please check your credentials.")

# Fetch Beaker Report with recursive retry mechanism
def fetch_report_recursive(patient_id, retries=3):
    """Recursively attempt to fetch the Beaker report."""
    try:
        report_data = fetch_beaker_report(patient_id, st.session_state.auth_token)
        if report_data:
            st.write("### Beaker Report Data")
            process_and_save_to_csv(report_data)
            st.dataframe(pd.read_csv("beaker_report_data.csv"))
            st.success("Report fetched successfully!")
        else:
            if retries > 0:
                st.warning(f"Retrying to fetch the Beaker Report... Attempt {4 - retries}")
                fetch_report_recursive(patient_id, retries - 1)
            else:
                st.error("Failed to retrieve the Beaker Report after multiple attempts.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        if retries > 0:
            st.warning("Retrying the fetch operation...")
            fetch_report_recursive(patient_id, retries - 1)

# Fetch Beaker Report Section
elif option == "Fetch Beaker Report":
    st.title("Fetch Beaker Laboratory Reports")
    if "auth_token" not in st.session_state:
        st.error("Please log in to Epic first!")
    else:
        patient_id = st.text_input("Enter Patient ID", value="PATIENT12345")  # Example patient ID
        if st.button("Fetch Report"):
            fetch_report_recursive(patient_id)

# Chat with Mutations Section
def chat_with_mutation(mutation_name):
    """Simulate a chat with the mutation to understand its behavior and treatment suggestions."""
    try:
        prompt = f"Hello, Mutation {mutation_name}. Can you tell me how you affect the patient's health, and what treatments might help?"
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.create(model="gpt-4-turbo", messages=[{"role": "user", "content": prompt}], max_tokens=500)
        st.write(f"### Mutation {mutation_name}'s Response:")
        for message in response['messages']:
            if message['role'] == "assistant":
                st.write(message['content'].strip())
    except Exception as e:
        st.error(f"Error chatting with mutation {mutation_name}: {str(e)}")

# AI-Powered Genomic Analysis with Dynamic Recommendations
def analyze_genomic_data_recursive(mutations, index=0):
    """Recursively analyze genomic mutations and predict next steps."""
    if index < len(mutations):
        mutation = mutations[index]
        st.write(f"Analyzing mutation: {mutation}")
        
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            prompt = f"Analyze the following genetic mutation and suggest personalized treatments: {mutation}"
            response = client.chat.create(model="gpt-4-turbo", messages=[{"role": "user", "content": prompt}], max_tokens=500)
            st.write(f"### AI Response for {mutation}")
            for message in response['messages']:
                if message['role'] == "assistant":
                    st.write(message['content'].strip())
        except Exception as e:
            st.error(f"Error during AI analysis for {mutation}: {str(e)}")
        
        # Recursively move to the next mutation analysis
        if st.button(f"Analyze Next Mutation for {mutation}"):
            analyze_genomic_data_recursive(mutations, index + 1)

# Genomic Analysis Section
elif option == "Genomic Analysis":
    st.title("AI-Powered Genomic Data Analysis")

    mutations = ["EGFR T790M", "P53 Mutation", "BRCA1 Mutation", "KRAS G12V"]
    st.subheader("Predicted Mutations")
    st.write(f"Detected Mutations: **{', '.join(mutations)}**")

    st.subheader("AI Treatment Insights")
    st.write("""
    The detected mutations suggest potential resistance to first-line therapies.
    AI-recommended therapies will be provided based on these findings.
    """)

    if st.button("Run Advanced AI Analysis"):
        analyze_genomic_data_recursive(mutations)

# Chat with Mutations - Interactive section
elif option == "Chat with Mutations":
    st.title("Chat with Genomic Mutations")

    mutation_name = st.selectbox("Select a Mutation to Chat With", ["EGFR T790M", "P53 Mutation", "BRCA1 Mutation", "KRAS G12V"])

    if st.button(f"Chat with {mutation_name}"):
        chat_with_mutation(mutation_name)

# Export Reports with PDF Generation & Dynamic Customization
elif option == "Export Reports":
    st.title("Export Results")
    export_option = st.selectbox("Select File Format", ["CSV", "JSON", "PDF"])

    if export_option == "CSV":
        st.write("Exporting as CSV...")
        try:
            with open("beaker_report_data.csv", "rb") as file:
                st.download_button("Download CSV", file, file_name="beaker_report_data.csv")
        except FileNotFoundError:
            st.error("No data available for export.")
    elif export_option == "JSON":
        st.write("Exporting as JSON...")
        try:
            with open("beaker_report_data.json", "w") as json_file:
                json.dump(report_data, json_file)  
            with open("beaker_report_data.json", "rb") as file:
                st.download_button("Download JSON", file, file_name="beaker_report_data.json")
        except Exception as e:
            st.error(f"Error exporting to JSON: {str(e)}")
    elif export_option == "PDF":
        st.write("Exporting as PDF...")
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Beaker Report - Patient ID: PATIENT12345", ln=True, align="C")
        pdf.output("beaker_report.pdf")
        
        with open("beaker_report.pdf", "rb") as file:
            st.download_button("Download PDF", file, file_name="beaker_report.pdf")
