from __future__ import annotations
import numpy as np
import pandas as pd

REQUIRED = [
    'area_id','area_name','zone','population_exposed','tower_count',
    'single_point_dependency_pct','power_backup_hours','generator_health_pct',
    'fiber_route_count','mobile_signal_redundancy_pct','disaster_exposure_pct',
    'communication_hub_distance_km'
]

def num(v, default=0.0):
    try:
        x=float(v)
        return default if not np.isfinite(x) else x
    except (TypeError, ValueError):
        return default

def clamp(v, lo=0.0, hi=100.0):
    return float(np.clip(num(v), lo, hi))

def risk_band(score):
    s=num(score)
    if s < 25: return 'Low'
    if s < 50: return 'Moderate'
    if s < 75: return 'High'
    return 'Critical'

def score_row(row):
    dependency=clamp(row['single_point_dependency_pct'])
    backup=clamp((100 - num(row['power_backup_hours'])*9))
    gen=clamp(100-num(row['generator_health_pct']))
    fiber=clamp(70-num(row['fiber_route_count'])*18)
    signal=clamp(100-num(row['mobile_signal_redundancy_pct']))
    hazard=clamp(row['disaster_exposure_pct'])
    hub=clamp(num(row['communication_hub_distance_km'])*13)
    towers=clamp(50-num(row['tower_count'])*10)
    risk=(.22*hazard+.20*dependency+.15*backup+.13*gen+.10*fiber+.10*signal+.06*hub+.04*towers)
    return pd.Series({
        'hazard_pressure':round(hazard,1), 'dependency_pressure':round(dependency,1),
        'backup_power_pressure':round(backup,1), 'generator_pressure':round(gen,1),
        'fiber_redundancy_pressure':round(fiber,1), 'signal_redundancy_pressure':round(signal,1),
        'hub_access_pressure':round(hub,1), 'tower_capacity_pressure':round(towers,1),
        'connectivity_loss_risk_score':round(clamp(risk),1),
        'connectivity_risk_band':risk_band(risk)
    })

def build_scored(df:pd.DataFrame)->pd.DataFrame:
    x=df.copy()
    x=pd.concat([x.reset_index(drop=True), x.apply(score_row,axis=1).reset_index(drop=True)],axis=1)
    x['backup_priority_score']=(.55*x.connectivity_loss_risk_score+.20*x.dependency_pressure+.15*x.backup_power_pressure+.10*x.generator_pressure).clip(0,100).round(1)
    pop=pd.to_numeric(x.population_exposed,errors='coerce').fillna(0).clip(lower=0)
    x['population_priority']=(x.backup_priority_score*(1+np.log1p(pop)/12)).clip(0,100).round(1)
    return x

def validate(df):
    issues=[]
    for c in REQUIRED:
        if c not in df.columns: issues.append(f"missing required column: {c}")
    if 'area_id' in df.columns:
        if df.area_id.isna().any() or (df.area_id.astype(str).str.strip()=='').any(): issues.append('area_id contains blank values')
        if df.area_id.duplicated().any(): issues.append('duplicate area_id values found')
    return issues
