# PY-W4-004 — Enterprise Workflow Automation & Intelligent Document Processing System

An educational, local-first implementation of the Week 4 internship brief. It combines employee and department management, document upload/extraction, approval workflows, REST APIs, authentication, reporting, and a Streamlit dashboard.

## Features
- FastAPI REST backend with OpenAPI/Swagger docs.
- SQLite database via SQLAlchemy ORM; tables are created on startup.
- Password hashing (Argon2) and JWT bearer authentication.
- Employee/department CRUD with duplicate checks and status validation.
- PDF, CSV, TXT and DOCX upload; text extraction, SHA-256 duplicate detection, metadata and keyword classification.
- Approval/rejection workflow with activity history.
- JSON summary, CSV employee export and PDF summary export.
- Authenticated Streamlit dashboard with employee search and CSV downloads.
- SQLite database backup helper (`python -m database.backup`).
- Scheduled CSV/JSON/PDF report generator (`python -m reports.scheduled_report`).
- Optional SMTP email notifications when SMTP settings are configured.
- Pytest starter tests and application logging.

## Requirements
- Python 3.10+ recommended
- VS Code (or another editor)

## Setup (Windows PowerShell)
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `.env` and replace `SECRET_KEY` with a long random value before using outside a local demo.

## Run the API
```powershell
python run.py
```
Open http://127.0.0.1:8000/docs for interactive Swagger API documentation.
The first account registered through `POST /auth/register` becomes admin; later accounts receive the user role. This is a simple demo bootstrap rule, not a production account-provisioning policy.

## Run the dashboard
In a second terminal (activate `venv` first):
```powershell
streamlit run dashboard/admin_dashboard.py
```
The dashboard authenticates against the FastAPI `/auth/login` endpoint. Register the first admin account and create additional user accounts through `/auth/register`.

## Main API flow
1. `POST /auth/register` — create the first account.
2. `POST /auth/login` — OAuth2 form fields `username` and `password`; copy `access_token`.
3. Click **Authorize** in Swagger and enter the token as `Bearer <token>`.
4. Create a department: `POST /departments`.
5. Create an employee: `POST /employees`.
6. Upload a document: `POST /documents/upload` (multipart form).
7. Create workflow: `POST /workflows`, optionally referencing `document_id`.
8. Approve/reject: `POST /workflows/{id}/decision`.
9. Reports: `GET /reports/summary`, `/reports/employees.csv`, `/reports/summary.pdf`.

## Tests and backup
```powershell
pytest -q
python -m database.backup
python -m reports.scheduled_report
```

## Project layout
- `app/` — API, database, models, schemas, security and routes
- `document_processing/` — extraction, classification and validation
- `workflow_engine/` — status transition helpers and notification logging
- `dashboard/` — Streamlit admin dashboard
- `reports/` — PDF report helper
- `database/schema.sql` — complete relational schema reference
- `database/backup.py` — consistent SQLite backup helper
- `reports/scheduled_report.py` — point-in-time CSV/JSON/PDF report generator
- `TECHNICAL_DOCUMENTATION.md` — design, data model, API, security and known limitations
- `tests/` — automated tests

## Architecture
```text
Streamlit Dashboard       Swagger / API Clients
         |                         |
         +---------- FastAPI ------+
                       |
          Routes -> Services/Logic
             |          |
          Security   Document & Workflow modules
             |          |
             +---- SQLAlchemy ORM ----+
                                      |
                                   SQLite DB
                                      |
                         uploads/ and logs/
```

## Important scope notes
- Notifications are logged locally; optional SMTP email can be configured in `.env` (SMS is not configured).
- The workflow demo supports Pending -> Approved/Rejected, admin-only decisions, activity history, pending notification logs, and an overdue query (pending longer than three days). The overdue query marks pending items older than three days; OS-level scheduling of periodic reports is configured separately using Task Scheduler/cron.
- The dashboard uses the API bearer token and is a read-only overview; API operations are authenticated.
- For production deployment, replace first-user admin bootstrap with out-of-band provisioning, add migrations, rate limiting, secure secret management, antivirus/content scanning, robust file-type sniffing, scheduled backups, real email delivery, and deployment hardening.
