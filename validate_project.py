from pathlib import Path
import pandas as pd
from telecom_engine import build_scored, validate
R=Path(__file__).parent
d=pd.read_csv(R/'data/sample_connectivity_exposure.csv')
err=validate(d); assert not err, err
s=build_scored(d); assert s.connectivity_loss_risk_score.between(0,100).all(); assert s.backup_priority_score.between(0,100).all()
print('PASS: ResilioNet disaster-telecom backup screening')
print(f'Areas: {len(s)}')
print(f'Risk range: {s.connectivity_loss_risk_score.min():.1f} - {s.connectivity_loss_risk_score.max():.1f}')
print(f'High/Critical: {(s.connectivity_loss_risk_score>=50).sum()}')
