# Cyber Incident Investigation Dashboard

A fully functional, database-driven cybersecurity investigation dashboard built with **Python**, **Streamlit**, and **MySQL**.

---

## Project Structure

```
Cyber-Investigation-Dashboard/
├── src/
│   ├── main.py           # Streamlit dashboard (entry point)
│   ├── database.py       # MySQL connection (reads .env)
│   └── queries.py        # All SQL query functions
├── database/
│   └── schema.sql        # Full database schema and seed data
├── requirements.txt      # Python dependencies
├── .gitignore
├── .env                  # Database credentials (not committed)
└── README.md
```

---

## Prerequisites

- Python 3.10+
- MySQL Server (running with the `cyber_investigation` database already set up)
- The `.env` file with valid database credentials

---

## Configuration

The `.env` file (already present) must contain:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=cyber_investigation
DB_PORT=3306
```

> **Never commit `.env` to version control.** It is listed in `.gitignore`.

---

## Installation

Using the existing virtual environment:

```bash
cd Cyber-Investigation-Dashboard
# Activate virtual environment
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows
```

Or install fresh:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Running the Dashboard

```bash
streamlit run src/main.py
```

The dashboard opens at **http://localhost:8501** in your browser.

---

## Dashboard Sections

| Section                  | Description                                                                                           |
|--------------------------|-------------------------------------------------------------------------------------------------------|
| Dashboard Overview       | KPI cards and charts for severity, status, attack type, and alert trends                              |
| Incident Investigation   | Filter and search incidents, detailed view, update status, assign investigator, record new incidents  |
| Security Alerts          | All alerts with filtering, alert logs, and critical highlighting                                      |
| Evidence Tracking        | Evidence records per incident, add new evidence                                                       |
| Investigation Activities | Chronological investigation timeline, record new activities                                           |
| Analytical Insights      | IP analysis, attack patterns, investigator workload, resolution patterns                              |
| Reports                  | Incident summary, critical report, resolution report, workload report with CSV export                 |

---

## Database Objects Used

**Tables:** `Incidents`, `Users`, `Devices`, `Investigators`, `Alerts`, `Alert_Logs`, `Evidence`, `Investigation_Logs`, `Incident_Status_History`, `IP_Addresses`

**Views:** `Incident_Report`, `Critical_Incident_Report`, `Investigator_Workload_Report`

**Stored Procedures:** `AddIncident`, `UpdateIncidentStatus`, `AssignInvestigator`, `GetIncidentDetails`

**Functions:** `CalculateIncidentAge`, `CalculateResolutionDuration`

---

## Security Notes

- All SQL queries use **parameterized statements** (no SQL injection risk)
- Database credentials are loaded from `.env` (never hardcoded)
- Database connections are properly closed after each operation
- Transactions are rolled back on failure for write operations
