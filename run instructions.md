# Run Instructions

```bash
cd ~/Downloads
rm -rf ResilioNet_GitHub_RUN
mkdir -p ResilioNet_GitHub_RUN
unzip -q DisasterTelecomBackupPlanner_GitHub_Complete_NEW.zip -d ResilioNet_GitHub_RUN
cd ResilioNet_GitHub_RUN/DisasterTelecomBackupPlanner_Local

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python -m py_compile app.py telecom_engine.py validate_project.py run.py
python validate_project.py
python -m pytest -q
python run.py
```

Run tests only from this project directory, not from `~/Downloads`, to avoid collecting unrelated projects.
