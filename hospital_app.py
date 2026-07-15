import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import sqlite3
import calendar
from utils.filters import apply_filters


st.set_page_config(
    page_title="Hospital Dashboard",
    layout="wide"
)



st.title("Healthcare Dashboard")

st.write("Welcome to my Streamlit application")






st.markdown("""
### Welcome

Use the sidebar to navigate between pages.

- Encounter Analytics
- Cost & Insurance Insights
- Patient and Procedures Analytics
""")

st.markdown("""
<style>

.report-header {
    background-color: #d9e7de;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
}

.report-title {
    font-size: 40px;
    font-weight: bold;
    color: #1a3faa;
}

.report-subtitle {
    font-size: 18px;
    font-style: italic;
    color: #333333;
}

.section-title {
    background-color: #0c3b6b;
    color: white;
    text-align: center;
    padding: 12px;
    border-radius: 5px;
    font-weight: bold;
    font-size: 22px;
}

.metric-card {
    background: #f5f7f8;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 3px 3px 8px rgba(0,0,0,0.3);
    text-align: center;
    min-height: 130px;
}

.metric-title {
    font-size: 20px;
    font-weight: bold;
}

.metric-value {
    font-size: 42px;
    margin-top: 15px;
    color: #222;
}

.filter-btn {
    background: white;
    border-radius: 25px;
    padding: 25px 15px;
    text-align:center;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    font-size: 24px;
    font-weight:bold;
    color:#0c3b6b;
}
            
# .kpi-card {
#     border: 10px;
#     border-radius: 15px;
#     background-color: #ddfcdf;
#     gap: 10px;
#     font-weight: bold;
#     padding: 10px 10px;
#     width: 150px;
#     margin-right: 10px;
    
# }
            
.kpi-card {
    background: linear-gradient(135deg, #ffffff, #f8fbff);
    border-radius: 18px;
    padding: 10px;
    min-height: 120px;
    width: 160px;

    box-shadow:
        0 4px 12px rgba(0,0,0,0.08),
        0 2px 4px rgba(0,0,0,0.05);

    border-left: 6px solid #1A3FAA;

    display: flex;
    flex-direction: column;
    justify-content: space-between;

    transition: all 0.3s ease;
}

.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow:
        0 8px 20px rgba(0,0,0,0.12),
        0 4px 8px rgba(0,0,0,0.08);
}

.kpi-title {
    font-size: 15px;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 38px;
    font-weight: 700;
    color: #1A3FAA;
    line-height: 1;
}

</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="report-header">
    <div class="report-title">Hospital Performance Report</div>
    <div class="report-subtitle">
        Driving Efficiency, Cost Management, and Policy Support
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-title">
    Encounter and Operational Overview
</div>
""", unsafe_allow_html=True)




with st.expander("Hospital Dataset"):
    first_col, second_col, third_col, forth_col = st.columns(4) 

    with first_col:
        tab1, tab2 = st.tabs(['Encounter_Table', 'Patient_table'])
        with tab1:
            st.header("Encounter Table")
            encount = pd.read_csv("encount.csv")
            st.write(encount.head(20))

            encount = apply_filters(encount)


        with tab2:
            st.header("Patient Table")
            patient = pd.read_csv("patient.csv")
            st.write(patient.head(20))
    with second_col:
        pays_tab1, pays_tab2 = st.tabs(['Payers Table', 'Procedure'])
        with pays_tab1:
            st.header("Payers Table")
            payers = pd.read_csv("payers.csv")
            st.write(payers.head(20))
        with pays_tab2:
            st.header("Procedure Table")
            procedure = pd.read_csv("procedure.csv")
            st.write(procedure.head(20))
    with third_col:
        tabs1, tabs2 = st.tabs(['Encount_nd_Patient', 'Encount_nd_Payers'])
        with tabs1:
            st.header("Encounter And Patient")
            encount_nd_patient = pd.read_csv("encount_nd_patient.csv")
            st.write(encount_nd_patient.head(20))
        with tabs2:
            st.header("Encounter And Payers")
            encount_nd_payers = pd.read_csv("encount_nd_payers.csv")
            st.write(encount_nd_payers.head(20))

    with forth_col:
        loc1, loc2 = st.tabs(['Encount_nd_Procedure', 'research_questions'])
        with loc1:
            st.header("Encounter and Procedure")
            encount_nd_proce = pd.read_csv("encount_nd_proce.csv")
            st.write(encount_nd_proce.head(20))

        # with loc2:
        #     st.header("Research Questions")

        #     conn = sqlite3.connect("create_hospital_db")

        #     with open("hospital_analytics_questions.sql", "r") as f:
        #             query = f.read()
        #     research = pd.read_sql(query, conn)

true_count = encount['Readmitted_Within_30_Days'].sum()
total_count = len(encount)

deceased_patients = (patient['DEATHDATE'] != 'Alive').sum()
 
total_patients = encount['PATIENT'].nunique()
total_encounters = encount['CODE'].count()
avg_visits = len(encount) / encount['PATIENT'].nunique()
readmiss_rate = (true_count / total_count) * 100
mortality_rate = (deceased_patients / len(patient)) * 100



col1, col2, col3, col4, col5 = st.columns(5)

# col1.metric("Total Patients", total_patients)
# col2.metric("Total Encounters", total_encounters)
# col3.metric("Avg Visits", avg_visits)
# col4.metric("Readmission", readmiss_rate)
# col5.metric("Mortality Rate", mortality_rate)


# KPI Row
cols = st.columns([1,2,2,2,2,2])

with cols[1]:
    st.markdown(f"""
    <div class="kpi-card">
    <div class="kpi-title">👨‍⚕️ Total Patients</div>
    <div class="kpi-value">{total_patients:,}</div>
    </div>  
    """, unsafe_allow_html=True)

with cols[2]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Encounters</div>
        <div class="kpi-value">{round(total_encounters/1000):.0f}K</div>
    </div>
    """, unsafe_allow_html=True)

with cols[3]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🏥 Avg Visits Per Patient</div>
        <div class="kpi-value">{avg_visits:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with cols[4]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">📈 Readmission Rate</div>
        <div class="kpi-value">{readmiss_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with cols[5]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title"> ⚕️ Mortality Rate</div>
        <div class="kpi-value">{mortality_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)




left_column, right_column = st.columns(2)

with left_column:
    
    st.markdown(
    '<p style="color:#1A3FAA; font-size:30px; font-weight:600; text-align:left;">'
    'ENCOUNTERS OVERVIEW'
    '</p>', 
    unsafe_allow_html=True
    )

    hourly_trend = (
    encount.groupby('HP')['Id']
    .count()
    .reset_index(name='Total_Encounters')
    )

    fig=px.line(
    hourly_trend,
    x='HP',
    y='Total_Encounters',
    title="Total Encounter Hourly Trend",
    markers=True
    )
    fig.update_traces(
    mode="lines+markers",  # Tells Plotly to show both lines and markers
    line=dict(
        shape="spline", 
        width=2.5, 
        color="#9cefa2"
    ),
    marker=dict(
        symbol="star", 
        size=5, 
        line=dict(width=2, color="#5bc0c7")
    )
    )

    fig.update_layout(
        title_x=0.1,
        xaxis_title="Hour",
        yaxis_title="Encounters",
        height=250,
        width=250,
        template="plotly_dark",
        paper_bgcolor="#D9E7DE",
        plot_bgcolor="white",
        font=dict(size=14),
        title_font=dict(size=20, color="#1A3FAA"),
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    fig.add_scatter(
        x=encount["HP"], 
        y=encount["Id"], 
        fill='tozeroy', 
        fillcolor="#B5C1EB", # Soft ambient shadow/glow
        mode='none', 
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)


    # st.space(size="medium")

    qtn1 = (
            encount.groupby('YP')['Id']
            .size()
            .reset_index(name='Total_Encounters', )
        )
    
    fig = px.bar(
    qtn1,
    x="YP",
    y="Total_Encounters",
    title="Total Encounters Each Year",
    color="YP",
    color_continuous_scale=["#c3e8c6", "#1b7008"],
    text_auto=True
    )

    fig.update_traces(
    textposition="outside",  # Places numbers cleanly above bars
    textfont=dict(color="#a6b3f1", size=12, family="Inter"),
    marker=dict(
        line=dict(width=1, color="#35334f"), # Subtle border highlight
        opacity=0.90
    ),
    width=0.6 # Adjusts bar thickness for a modern look (default is wider)
    )

    
    fig.update_layout(
        title_x=0.3,
        xaxis_title="Year",
        yaxis_title="Encounters",
        height=350,
        width=250,
        template="plotly_white",
        title_font=dict(size=20, color="#1A3FAA")
    )

    st.plotly_chart(fig, use_container_width=True)

    st.space(size="medium")

    st.markdown(
    '<p style="color:#1A3FAA; font-size:30px; font-weight:600; text-align:left;">'
    'Average Length Of Stay by Encounter Class'
    '</p>', 
    unsafe_allow_html=True
    )

    ave_len_stay = (
        encount_nd_proce.groupby(['ENCOUNTERCLASS']).agg(
            avg_total=('Duration_Hours', 'mean')
        ).sort_values('avg_total', ascending=False).reset_index()
        )
       
    ave_len_stay["avg_total"] = ave_len_stay["avg_total"].round(0)
    fig = px.bar(
    ave_len_stay, 
    x="avg_total",       
    y="ENCOUNTERCLASS",      
    title="Encounter Class by Average Hours Spent",
    orientation="h",       
    color="ENCOUNTERCLASS",    
    color_continuous_scale=["#1e293b", "#00f2fe"], 
    text="avg_total"      
    )

    fig.update_traces(
    textposition="outside",  # Places numbers cleanly above bars
    textfont=dict(color="#a6b3f1", size=12, family="Inter"),
    marker=dict(
        line=dict(width=1, color="#35334f"), # Subtle border highlight
        opacity=0.90
    ),
    width=0.5 # Adjusts bar thickness for a modern look (default is wider)
    )

    fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", # Blends chart background completely away
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=40, r=40, t=20, b=10), # Snug custom padding alignment
    height=250,
    
    # Hide the bulky legend scale for minimalist dashboards
    coloraxis_showscale=False,
    
    # X-Axis Customization (Horizontal Scale)
    xaxis=dict(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.05)", # Ultra-faint vertical helper lines
        tickfont=dict(color="#64748b", size=11),
        title="Encounter Hours",
        zeroline=False
    ),
    
    yaxis=dict(
        showgrid=False, # Strips out horizontal grids completely
        tickfont=dict(color="#94a3b8", size=12),
        title="Encounter Class",
        linecolor="rgba(255,255,255,0.1)" # Modern minimal border edge line
    ),
    title_font=dict(size=15, color="#1A3FAA")
    )
    
    # 4. Render directly into Streamlit canvas
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    encount_by_cls = (
        encount.groupby('ENCOUNTERCLASS')['Id']
        .count()
        .reset_index(name='Total_Encounters')
    )

    fig = px.pie(
        encount_by_cls,
        names='ENCOUNTERCLASS',
        values='Total_Encounters',
        title='Encounters by Class',
        hole=0.2  # Creates a donut chart
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Encounters: %{value:,}<br>Percentage: %{percent}<extra></extra>'
    )

    fig.update_layout(
        width=200,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=18, color='#1A3FAA'),
        legend_title='Encounter Class'
    )

    fig.update_traces(
        pull=[0.05] * len(encount_by_cls),  # Slight separation
        marker=dict(
            line=dict(color='white', width=2)
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


with right_column:
    st.markdown(
    '<p style="color:#1A3FAA; font-size:30px; font-weight:600; text-align:left;">'
    'ClASS OVERVIEW'
    '</p>', 
    unsafe_allow_html=True
    )
    encout_cl_readmssn = (
                encount_nd_patient[encount_nd_patient['Readmission']]
                .groupby(['ENCOUNTERCLASS'])
                .size()
                .reset_index(name='Readmission_count')
                .sort_values('Readmission_count', ascending=False)
    )

    fig = px.bar(
    encout_cl_readmssn, 
    x="Readmission_count",       
    y="ENCOUNTERCLASS",      
    title="Encounter Class Readmit Count",
    orientation="h",       
    color="ENCOUNTERCLASS",    
    color_continuous_scale=["#1e293b", "#00f2fe"], 
    text="Readmission_count"      
    )

    fig.update_traces(
    textposition="outside",  # Places numbers cleanly above bars
    textfont=dict(color="#a6b3f1", size=12, family="Inter"),
    marker=dict(
        line=dict(width=1, color="#35334f"), # Subtle border highlight
        opacity=0.90
    ),
    width=0.5 # Adjusts bar thickness for a modern look (default is wider)
    )

    fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", # Blends chart background completely away
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=40, r=40, t=20, b=10), # Snug custom padding alignment
    height=250,
    
    # Hide the bulky legend scale for minimalist dashboards
    coloraxis_showscale=False,
    
    # X-Axis Customization (Horizontal Scale)
    xaxis=dict(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.05)", # Ultra-faint vertical helper lines
        tickfont=dict(color="#64748b", size=11),
        title="Encounter Count",
        zeroline=False
    ),
    
    yaxis=dict(
        showgrid=False, # Strips out horizontal grids completely
        tickfont=dict(color="#94a3b8", size=12),
        title="Encounter Class",
        linecolor="rgba(255,255,255,0.1)" # Modern minimal border edge line
    ),
    title_font=dict(size=15, color="#1A3FAA")
    )

    # 4. Render directly into Streamlit canvas
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


    st.markdown(
    '<p style="color:#1A3FAA; font-size:30px; font-weight:600; text-align:left;">'
    'Encounter Reason resulting to Death'
    '</p>', 
    unsafe_allow_html=True
    )

    st.markdown("""
    <style>
    .table-card {
        background: #edeff1;
        padding: 5px;
        border-radius: 15px;
        border: 10px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
    }
    </style>
    """, unsafe_allow_html=True)
    
    deaths_by_reason = (
    encount_nd_patient[encount_nd_patient['DEATHDATE'] != 'Alive']
    .groupby(['ENCOUNTERCLASS','REASONDESCRIPTION'])
    .size()
    .reset_index(name='Death_Count')
    .sort_values('Death_Count', ascending=False)
    )

    styled_dbr = deaths_by_reason.head(40).style.set_properties(
        **{
        'background-color': "#edeff1",
        'color': "#286b15",
        'border-color': '#286b15',
        'height': 200,
        }
    )
    

    with st.container(border=True):
        st.dataframe(styled_dbr,height=300, hide_index=True, use_container_width=True)


    encount['Month'] = encount['MP'].apply(
    lambda x: calendar.month_name[int(x)]
    )
    monthly_encounters = (
    encount.groupby('MP')['Id']
    .count()
    .reset_index(name='Total_Encounters')
    .sort_values('MP')
    )

    monthly_encounters['Month'] = monthly_encounters['MP'].apply(
    lambda x: calendar.month_abbr[int(x)]
    )

    month_order = [
    'Jan','Feb','Mar','Apr','May','Jun',
    'Jul','Aug','Sep','Oct','Nov','Dec'
    ]

    fig = px.area(
    monthly_encounters,
    x='Month',
    y='Total_Encounters',
    title='Total Encounters by Month',
    category_orders={'Month': month_order},
    color_discrete_sequence=['#0c3b6b']
    )

    fig.update_traces(
        mode='lines+markers+text',
        text=[f"{x/1000:.1f}K" for x in monthly_encounters['Total_Encounters']],
        textposition='top center',
        fillcolor="#cbf89b",
        line=dict(width=4)
    )


    fig.update_layout(
        height=450,
        template='plotly_white',
        title_x=0.3,
        xaxis_title='Month',
        yaxis_title='Total Encounters',
        hovermode='x unified',
        title_font=dict(size=15, color="#7287ef")
    )

    st.plotly_chart(fig, use_container_width=True)


st.markdown("""
<div class="section-title">
    SUMMARY OF ANALYSIS/RESULTS
</div>
<h3> 
1. Although ambulatory care is designed for same-day treatment, many patients are returning within
30 days.
</h3> 
<h5>         
Recommendation
            
* Review discharge instructions given in ambulatory clinics.
* Identify the top 10 diagnoses responsible for ambulatory readmissions.
* Introduce follow-up phone calls or SMS reminders within 48–72 hours after discharge.
</h5>      

                                
<h3> 
2. Long inpatient stays reduce bed availability and increase treatment costs.
</h3> 
<h5>         
Recommendation
            
* Review inpatient discharge delays.
* Improve coordination between laboratory, pharmacy, and physician teams.
* Establish discharge planning within the first 24 hours of admission.
</h5>        

<h3> 
3. Chronic Congestive Heart Failure is the leading cause associated with deaths (1,197 cases).
</h3> 
<h5>         
Recommendation
            
* Introduce a Heart Failure Management Program.
* Increase routine monitoring for cardiovascular patients.
* Strengthen chronic disease clinics for heart disease and lipid disorders.
</h5>    

<h3> 
Overall Recommendation
</h3> 
            
<h5>         
The hospital should prioritize reducing ambulatory readmissions, 
shortening inpatient stays, and strengthening chronic disease management—particularly 
for heart failure patients.
</h5>              

 

            

""", unsafe_allow_html=True)