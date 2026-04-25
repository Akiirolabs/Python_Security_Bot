# SOC Alert Automation Pipeline

## What it does
- Loads alerts from CSV or JSON
- Extracts IOCs
- Enriches them with a mock TI engine
- Scores severity
- Writes case.json and report.md

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest ruff
