# PQC Migration Analyzer

A tool built with Flask to analyze the readiness of servers for Post-Quantum Cryptography (PQC). It dynamically connects to a target host/port, analyzes the TLS configuration, extracts classical certificates (RSA/ECC), and generates a quantum-risk report and migration simulation.

## Overview
This project helps organizations evaluate their current cryptographic vulnerability to quantum computing threats (like Shor's algorithm attacking RSA/ECC) and provides an actionable migration path to quantum-safe algorithms like Kyber and Dilithium.

## Features
- **Live TLS Scanning:** Connects directly to TLS endpoints (e.g., `example.com:443`).
- **Algorithm Detection:** Scans for classical RSA or Elliptic Curve certificates.
- **Risk Assessment:** Evaluates risk based on Key Sizes, TLS version, and signature algorithm.
- **Migration Simulation:** Projects transition steps from classical to hybrid, and finally to full Post-Quantum Cryptography (PQC).
- **PDF Reporting:** Automatically generates and downloads detailed PDF reports of the scan results.

---

## Local Development & Setup Walkthrough

### 1. Prerequisites
- Python 3.8+
- MySQL Server

### 2. Database Setup
The app expects a MySQL database named `pqc_framework`. A SQL dump file `Dump20260317.sql` is provided to set up the schema.

1. Connect to your local MySQL instance.
2. Create the database:
   ```sql
   CREATE DATABASE pqc_framework;
   ```
3. Import the dump file:
   ```bash
   mysql -u root -p pqc_framework < Dump20260317.sql
   ```

### 3. Environment Variables
This project uses `.env` files to hide database credentials.
1. Copy the `.env.example` file to create a new `.env` file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your local MySQL credentials:
   ```ini
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_local_password
   DB_NAME=pqc_framework
   ```

### 4. Install Dependencies
Create a virtual environment (optional but recommended) and install dependencies via `requirements.txt`:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Running the Application locally
The app currently requires some self-signed certificates in the `certs/` folder to start properly over HTTPS. If you have those in the `certs/` folder, start the app:

```bash
python app.py
```
The application will run securely by default.

---

## Deployment (Production)

If you are hosting this project on a cloud provider like Render, Heroku, or PythonAnywhere:
1. Setup a Managed Cloud MySQL Database with the hosting provider or via an external service like Aiven.
2. In your hosting platform's **Environment Variables** dashboard, replicate the keys specified in `.env.example` (i.e. put in your real production DB host, username, and password).
3. Specify `gunicorn` as your web server command in your cloud configuration (or a hosting equivalent):
   ```bash
   gunicorn app:app
   ```
4. Update `app.route("/")` limits or redirect rules conditionally based on your host domain, if required.
