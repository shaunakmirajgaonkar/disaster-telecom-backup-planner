from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from telecom_engine import build_scored, validate

st.set_page_config(page_title='ResilioNet Local',page_icon='📡',layout='wide',initial_sidebar_state='expanded')
ROOT=Path(__file__).parent; DATA=ROOT/'data'; ASSET=ROOT/'assets'

st.markdown('''<style>
.stApp{background:#f5f8fc;color:#182638}
[data-testid="stSidebar"]{background:#fff;border-right:1px solid #dce6ef}
[data-testid="stSidebar"] *{color:#203149!important}
.hero{background:linear-gradient(135deg,#0b3b67 0%,#0b70a8 35%,#0aa6a6 68%,#8ac926 100%);border-radius:26px;padding:28px 32px;color:#fff;box-shadow:0 18px 48px rgba(11,84,120,.18);margin-bottom:16px}
.hero h1{font-size:37px;font-weight:900;margin:0 0 5px}.hero p{font-size:15px;margin:0;opacity:.96}
.metric{background:#fff;border:1px solid #dfe8ef;border-radius:18px;padding:16px 18px;box-shadow:0 7px 24px rgba(26,56,82,.05)}
.metric .l{font-size:11px;text-transform:uppercase;letter-spacing:.10em;color:#718292}.metric .v{font-size:28px;font-weight:900;color:#16364e}
.section{font-size:21px;font-weight:900;color:#163b56;margin:18px 0 9px}
.note{background:#eef9f9;border:1px solid #bce5e4;border-radius:13px;padding:12px 14px;color:#23515a}
</style>''',unsafe_allow_html=True)

def metric(label,value):
    st.markdown(f'<div class="metric"><div class="l">{label}</div><div class="v">{value}</div></div>',unsafe_allow_html=True)

@st.cache_data
def demo(): return pd.read_csv(DATA/'sample_connectivity_exposure.csv')
base=demo()

with st.sidebar:
    st.markdown('## 📡 ResilioNet Local')
    st.caption('Disaster telecom backup planning intelligence')
    page=st.radio('Workspace',[
        'Command Center','Connectivity Risk Atlas','Area Deep Dive','Infrastructure Resilience',
        'Hazard & Exposure','Backup Priority','Scenario Lab','Data Quality','Reports'
    ])
    st.markdown('---')
    st.markdown('**100% LOCAL PROCESSING**')
    st.write('No carrier API, cloud AI, or external map service is required.')

st.markdown('<div class="hero"><h1>📡 ResilioNet Local</h1><p>Advanced disaster telecom resilience, backup-connectivity and communication-hub planning intelligence.</p></div>',unsafe_allow_html=True)
img=ASSET/'resilionet_dashboard_visual.png'
if img.exists():
    with st.expander('Preview dashboard visual',expanded=False): st.image(str(img),use_container_width=True)

with st.expander('📥 Local Connectivity Data Intake',expanded=(page=='Data Quality')):
    up=st.file_uploader('Connectivity exposure CSV',type='csv',key='up')
    data=pd.read_csv(up) if up else base.copy()
    problems=validate(data)
    if problems:
        st.error('Validation failed:\n\n'+'\n'.join('- '+x for x in problems)); st.stop()
    scored=build_scored(data)
    st.success(f'Loaded {len(scored):,} areas.')

bands=scored.connectivity_risk_band.value_counts().reindex(['Low','Moderate','High','Critical'],fill_value=0)
avg=float(scored.connectivity_loss_risk_score.mean()); high=int((scored.connectivity_loss_risk_score>=50).sum()); crit=int((scored.connectivity_loss_risk_score>=75).sum())
pop_high=int(scored.loc[scored.connectivity_loss_risk_score>=50,'population_exposed'].sum())

if page=='Command Center':
    st.markdown('<div class="section">Telecom Resilience Command Center</div>',unsafe_allow_html=True)
    cols=st.columns(5)
    for c,(l,v) in zip(cols,[('Areas',len(scored)),('Average loss risk',f'{avg:.1f}/100'),('High+',high),('Critical',crit),('Population exposed in High+',f'{pop_high:,}')]):
        with c: metric(l,v)
    a,b=st.columns(2)
    with a:
        fig=px.bar(bands.reset_index(),x='connectivity_risk_band',y='count',text='count',color='connectivity_risk_band',title='Connectivity-loss risk distribution')
        fig.update_layout(template='plotly_white',height=360); st.plotly_chart(fig,use_container_width=True)
    with b:
        fig=go.Figure(go.Indicator(mode='gauge+number',value=avg,title={'text':'Average connectivity-loss risk'},gauge={'axis':{'range':[0,100]}})); fig.update_layout(template='plotly_white',height=360); st.plotly_chart(fig,use_container_width=True)
    a,b=st.columns([1.15,1])
    with a:
        fig=px.scatter(scored,x='mobile_signal_redundancy_pct',y='single_point_dependency_pct',size='population_exposed',color='connectivity_risk_band',hover_name='area_name',title='Signal redundancy × dependency')
        fig.update_layout(template='plotly_white',height=420); st.plotly_chart(fig,use_container_width=True)
    with b:
        st.markdown('#### 🚨 Highest backup priorities'); st.dataframe(scored.sort_values('population_priority',ascending=False)[['area_name','zone','population_exposed','connectivity_loss_risk_score','connectivity_risk_band','backup_priority_score']].head(10),use_container_width=True,hide_index=True)

elif page=='Connectivity Risk Atlas':
    st.markdown('<div class="section">Connectivity Risk Atlas</div>',unsafe_allow_html=True)
    q=scored.copy(); q['grid_x']=np.arange(len(q))%4; q['grid_y']=-(np.arange(len(q))//4)
    fig=px.scatter(q,x='grid_x',y='grid_y',size='population_exposed',color='connectivity_risk_band',text='area_name',hover_data=['connectivity_loss_risk_score','backup_priority_score'],title='Area-level resilience atlas')
    fig.update_traces(textposition='top center'); fig.update_layout(template='plotly_white',height=620,xaxis_visible=False,yaxis_visible=False); st.plotly_chart(fig,use_container_width=True)
    fig=px.bar(scored.sort_values('connectivity_loss_risk_score'),x='connectivity_loss_risk_score',y='area_name',orientation='h',color='connectivity_risk_band',title='Ranked connectivity-loss risk'); fig.update_layout(template='plotly_white',height=580); st.plotly_chart(fig,use_container_width=True)

elif page=='Area Deep Dive':
    st.markdown('<div class="section">Area Deep Dive</div>',unsafe_allow_html=True)
    aid=st.selectbox('Select area',list(scored.area_id),format_func=lambda x:scored.loc[scored.area_id==x,'area_name'].iloc[0]); r=scored.loc[scored.area_id==aid].iloc[0]
    cols=st.columns(5)
    for c,(l,v) in zip(cols,[('Risk',r.connectivity_loss_risk_score),('Band',r.connectivity_risk_band),('Population',f'{r.population_exposed:,}'),('Backup hours',f'{r.power_backup_hours:.1f} h'),('Signal redundancy',f'{r.mobile_signal_redundancy_pct:.1f}%')]):
        with c: metric(l,v)
    labels=['Hazard','Dependency','Backup power','Generator','Fiber redundancy','Signal redundancy','Hub access','Tower capacity']; vals=[r.hazard_pressure,r.dependency_pressure,r.backup_power_pressure,r.generator_pressure,r.fiber_redundancy_pressure,r.signal_redundancy_pressure,r.hub_access_pressure,r.tower_capacity_pressure]
    a,b=st.columns(2)
    with a:
        fig=go.Figure(go.Bar(x=vals,y=labels,orientation='h')); fig.update_layout(template='plotly_white',height=450,xaxis_range=[0,100],title='Resilience driver fingerprint'); st.plotly_chart(fig,use_container_width=True)
    with b:
        fig=go.Figure(go.Indicator(mode='gauge+number',value=r.connectivity_loss_risk_score,title={'text':'Connectivity-loss score'},gauge={'axis':{'range':[0,100]}})); fig.update_layout(template='plotly_white',height=450); st.plotly_chart(fig,use_container_width=True)
    st.dataframe(pd.DataFrame([r]),use_container_width=True,hide_index=True)

elif page=='Infrastructure Resilience':
    st.markdown('<div class="section">Infrastructure Resilience</div>',unsafe_allow_html=True)
    towers=pd.read_csv(DATA/'sample_backup_towers.csv'); hubs=pd.read_csv(DATA/'sample_communication_hubs.csv')
    a,b=st.columns(2)
    with a:
        fig=px.scatter(towers,x='backup_hours',y='generator_health_pct',color='tower_type',hover_data=['area_id','tower_id'],title='Backup tower resilience profile'); fig.update_layout(template='plotly_white',height=420); st.plotly_chart(fig,use_container_width=True)
    with b:
        fig=px.scatter(hubs,x='distance_km',y='backup_capacity_users',size='backup_capacity_users',color='status',hover_data=['area_id','hub_id'],title='Communication-hub accessibility'); fig.update_layout(template='plotly_white',height=420); st.plotly_chart(fig,use_container_width=True)
    st.dataframe(towers,use_container_width=True,hide_index=True)

elif page=='Hazard & Exposure':
    st.markdown('<div class="section">Hazard & Exposure</div>',unsafe_allow_html=True)
    events=pd.read_csv(DATA/'sample_disaster_events.csv'); a,b=st.columns(2)
    with a:
        hc=events.groupby('hazard_type').size().reset_index(name='events'); fig=px.bar(hc,x='hazard_type',y='events',color='hazard_type',title='Local hazard-event mix'); fig.update_layout(template='plotly_white',height=410); st.plotly_chart(fig,use_container_width=True)
    with b:
        fig=px.scatter(scored,x='disaster_exposure_pct',y='population_exposed',size='connectivity_loss_risk_score',color='connectivity_risk_band',hover_name='area_name',title='Hazard exposure × population'); fig.update_layout(template='plotly_white',height=410); st.plotly_chart(fig,use_container_width=True)
    st.dataframe(events,use_container_width=True,hide_index=True)

elif page=='Backup Priority':
    st.markdown('<div class="section">Backup Deployment Priority</div>',unsafe_allow_html=True)
    q=scored.copy(); q['recommended_action']=np.select([q.connectivity_loss_risk_score>=75,q.backup_power_pressure>=60,q.signal_redundancy_pressure>=65,q.dependency_pressure>=60],['Priority contingency design + authorized emergency telecom review','Increase generator/backup-power readiness','Improve alternate communication paths','Reduce single-point dependency'],default='Routine resilience review')
    st.dataframe(q.sort_values('population_priority',ascending=False)[['area_name','zone','population_exposed','population_priority','connectivity_risk_band','recommended_action']].head(20),use_container_width=True,hide_index=True)
    st.info('Planning support only. Final tower, generator and communication-hub decisions require authorized telecom, emergency-management and infrastructure assessment.')

elif page=='Scenario Lab':
    st.markdown('<div class="section">Scenario Lab</div>',unsafe_allow_html=True)
    aid=st.selectbox('Scenario area',list(scored.area_id),format_func=lambda x:scored.loc[scored.area_id==x,'area_name'].iloc[0]); r=scored.loc[scored.area_id==aid].iloc[0]
    a,b,c=st.columns(3)
    with a: backup_gain=st.slider('Backup-power gain (hours)',0.0,8.0,2.0,.5)
    with b: signal_gain=st.slider('Signal-redundancy gain (points)',0,40,15)
    with c: dependency_drop=st.slider('Dependency reduction %',0,50,15)
    sim=pd.DataFrame([{'area_id':r.area_id,'area_name':r.area_name,'zone':r.zone,'population_exposed':r.population_exposed,'tower_count':r.tower_count,'single_point_dependency_pct':max(0,r.single_point_dependency_pct-dependency_drop),'power_backup_hours':r.power_backup_hours+backup_gain,'generator_health_pct':r.generator_health_pct,'fiber_route_count':r.fiber_route_count,'mobile_signal_redundancy_pct':min(100,r.mobile_signal_redundancy_pct+signal_gain),'disaster_exposure_pct':r.disaster_exposure_pct,'communication_hub_distance_km':r.communication_hub_distance_km}])
    ss=build_scored(sim).iloc[0]; a,b=st.columns(2)
    with a: metric('Current risk',r.connectivity_loss_risk_score)
    with b: metric('Scenario risk',ss.connectivity_loss_risk_score)
    delta=float(r.connectivity_loss_risk_score-ss.connectivity_loss_risk_score); st.success(f'Scenario change: {delta:+.1f} risk points (positive means improvement).')

elif page=='Data Quality':
    st.markdown('<div class="section">Data Quality Lab</div>',unsafe_allow_html=True)
    a,b,c=st.columns(3)
    with a: metric('Areas',len(data))
    with b: metric('Columns',len(data.columns))
    with c: metric('Missing cells',int(data.isna().sum().sum()))
    st.dataframe(data,use_container_width=True,hide_index=True)
    st.code(', '.join(['area_id','area_name','zone','population_exposed','tower_count','single_point_dependency_pct','power_backup_hours','generator_health_pct','fiber_route_count','mobile_signal_redundancy_pct','disaster_exposure_pct','communication_hub_distance_km']))

else:
    st.markdown('<div class="section">Reports & Export</div>',unsafe_allow_html=True)
    summary=pd.DataFrame({'metric':['Areas','Average risk','High+ areas','Critical areas','Population in High+ areas'],'value':[len(scored),round(avg,1),high,crit,pop_high]}); st.dataframe(summary,use_container_width=True,hide_index=True)
    st.download_button('Download telecom resilience intelligence',scored.to_csv(index=False).encode(),file_name='resilionet_risk_intelligence.csv',mime='text/csv')
    st.download_button('Download source dataset',data.to_csv(index=False).encode(),file_name='resilionet_connectivity_exposure.csv',mime='text/csv')
    st.markdown('<div class="note">Scores are planning indicators and do not guarantee network outages, public-safety performance, or infrastructure failure.</div>',unsafe_allow_html=True)
