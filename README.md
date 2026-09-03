# Disaster Telecom Backup Planner — ResilioNet Local

A privacy-conscious, local-first dashboard for screening areas likely to experience mobile-connectivity loss during disasters and prioritizing backup towers, generators, redundant communication paths, and communication hubs.

## Features
- Explainable 0–100 connectivity-loss risk score
- Low / Moderate / High / Critical bands
- Population-aware backup priority
- Command Center
- Connectivity Risk Atlas
- Area Deep Dive
- Infrastructure Resilience
- Hazard & Exposure
- Backup Priority
- Scenario Lab
- Data Quality
- Reports and CSV exports
- Automatic local port selection
- No external APIs or cloud AI

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python validate_project.py
python -m pytest -q
python run.py
```
