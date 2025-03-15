# GenomicsAI

Advanced Genomic Insights for Laboratory Evaluation (AGILE) - A platform for genomic data analysis and interpretation.

## Environment Variables and Security

This project uses environment variables to manage sensitive configuration. Follow these steps to set up your environment securely:

1. **Never commit `.env` files to version control**
   - The `.env` file contains sensitive API keys and credentials
   - This file is included in `.gitignore` to prevent accidental commits

2. **Setting up your environment**
   - Copy `.env.example` to `.env`
   - Fill in your own API keys and credentials
   ```bash
   cp .env.example .env
   # Then edit .env with your actual credentials
   ```

3. **Rotating compromised credentials**
   - If you suspect any API keys or credentials have been compromised:
     - Immediately rotate (change) the affected credentials at their source
     - Update your local `.env` file with the new credentials
     - Never share credentials in code, chat, or public forums

4. **Security best practices**
   - Use environment-specific variables for different deployments
   - Consider using a secrets management service for production
   - Regularly audit and rotate credentials
   - Use the minimum required permissions for each service

## HIPAA Compliance

This application includes features to help maintain HIPAA compliance:

- Automatic detection and redaction of sensitive health information
- Sanitization of messages containing PHI (Protected Health Information)
- Context-aware processing of genomic data

## Getting Started

1. Clone the repository
2. Set up environment variables as described above
3. Install dependencies
4. Run the application

```bash
# Install dependencies
npm install

# Run the development server
npm run dev
```

## Features

- AI-powered genomic data analysis
- HIPAA-compliant data handling
- Integration with clinical systems
- Digital twin modeling for precision medicine
- Clinical trial matching

---

# Epic FHIR Dashboard

## Overview
A React-based dashboard that connects to Epic's open FHIR API for real-time patient data retrieval.

## Setup Instructions

1. Install dependencies:
   ```sh
   npm install
   ```

2. Replace `YOUR_ACCESS_TOKEN` in `src/App.js` with a valid Epic API token.

3. Start the development server:
   ```sh
   npm start
   ```

4. Open `http://localhost:3000` in your browser.

## Features
- Secure OAuth 2.0 authentication
- Real-time Epic FHIR patient data retrieval
- AI-powered insights (to be integrated)

## License
MIT
