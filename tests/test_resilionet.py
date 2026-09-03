from pathlib import Path
import pandas as pd
from telecom_engine import build_scored, validate
R=Path(__file__).parents[1]
def test_schema():
    d=pd.read_csv(R/'data/sample_connectivity_exposure.csv'); assert validate(d)==[]
def test_bounds():
    d=pd.read_csv(R/'data/sample_connectivity_exposure.csv'); s=build_scored(d); assert s.connectivity_loss_risk_score.between(0,100).all(); assert s.backup_priority_score.between(0,100).all()
def test_unique_ids():
    d=pd.read_csv(R/'data/sample_connectivity_exposure.csv'); assert not d.area_id.duplicated().any()
