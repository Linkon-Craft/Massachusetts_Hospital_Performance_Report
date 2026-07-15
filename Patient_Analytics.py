import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import calendar

from utils.filters import apply_filters

st.set_page_config(layout="wide")


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

.kpi-card {
    background: linear-gradient(135deg, #ffffff, #f8fbff);
    border-radius: 18px;
    padding: 10px;
    height: 150px;
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
            
.summary-details {
    font-size: 12px;
    font-color:#0c3b6b
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
    Patient and Procedures Analytics
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


encount_nd_patient['BIRTHDATE'] = pd.to_datetime(encount_nd_patient['BIRTHDATE'])

encount_nd_patient['AGE'] = (
            (pd.Timestamp.today() - encount_nd_patient['BIRTHDATE']).dt.days // 365
        )
        
avg_age = encount_nd_patient['AGE'].mean()

avg_los = encount_nd_proce['Duration_Hours'].mean()

oop = (
    encount_nd_payers['TOTAL_CLAIM_COST']
    -
    encount_nd_payers['PAYER_COVERAGE']
)

avg_oop = oop.mean()

total_procedures = len(procedure)

avg_proc_cost = (
    procedure['BASE_COST']
    .mean()
)




avg_duration = (
    encount_nd_proce['Duration_Hours']
    .mean()
)

def human_format(num):
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.1f}"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.1f}"
    elif num >= 1_000:
        return f"{num/1_000:.1f}"
    else:
        return f"${num:.0f}"

# KPI Row
cols = st.columns([1,2,2,2,2,2,2])

with cols[1]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Average Patient Age</div>
        <div class="kpi-value">{avg_age:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

with cols[2]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Average Length of Stay</div>
        <div class="kpi-value">{avg_los:.1f}hr</div>
    </div>
    """, unsafe_allow_html=True)

with cols[3]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Average Out-of-Pocket Cost</div>
        <div class="kpi-value">${human_format(avg_oop)}K</div>
    </div>
    """, unsafe_allow_html=True)

with cols[4]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Procedures</div>
        <div class="kpi-value">{total_procedures}</div>
    </div>
    """, unsafe_allow_html=True)

with cols[5]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Average procedure Cost</div>
        <div class="kpi-value">${human_format(avg_proc_cost)}K</div>
    </div>
    """, unsafe_allow_html=True)

with cols[6]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Average Procedure Duration</div>
        <div class="kpi-value">{avg_duration:.1f}hr</div>
    </div>
    """, unsafe_allow_html=True)

st.space(size="medium")

left_column, right_column = st.columns(2)


with left_column:
    # 1. Which age groups use the hospital most?
    encount_nd_patient['Age_Group'] = pd.cut(
        encount_nd_patient['AGE'],
        bins=[0, 18, 35, 50, 65, 120],
        labels=['0-18', '19-35', '36-50', '51-65', '65+']
        )
    
    age_by_encount = (
        encount_nd_patient.groupby('Age_Group')['Id_x']
        .size()
        .reset_index(name='Total_Encounter')
    )

    age_by_encount['Total_Encounter'] = age_by_encount['Total_Encounter']/1000
    # st.write(age_by_encount)

    fig=px.bar(
        age_by_encount,
        x="Total_Encounter",
        y="Age_Group",
        title="Age With Highest Hospital Utilization",
        orientation="h",
        color="Age_Group",
        color_continuous_scale=["#1e293b", "#00f2fe"], 
        text="Total_Encounter"
    )

    fig.update_traces(
        texttemplate='%{text:,.1f}K',
        textposition='outside'
    )

    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        height=450,
        title_x=0.25,
        coloraxis_showscale=False,
        title_font=dict(size=15, color="#1A3FAA")
        )

    st.plotly_chart(fig, use_container_width=True)

    page1, page2, page3 = st.tabs(['Page 1', 'Page 2', 'Page 3'])
    # Which patient groups have the highest readmission rates?

    with page1:
        readmitted_patients = (
        encount_nd_patient[encount_nd_patient['Readmission'] == True]
        .groupby('Age_Group')
        .size()
        )
        total_patients = encount_nd_patient.groupby('Age_Group').size()

        readmission_rate = (
        readmitted_patients / total_patients * 100
        ).fillna(0)

        readmission_rate_df = (
        readmission_rate
        .reset_index(name='Readmission_Rate')
        .sort_values('Readmission_Rate', ascending=False)
        )
        

        fig=px.bar(
            readmission_rate_df,
            x="Age_Group",
            y="Readmission_Rate",
            title="Age Group Readmission Rate",
            color="Age_Group",
            color_continuous_scale=["#1e293b", "#00f2fe"], 
            text="Readmission_Rate"
        )

        fig.update_traces(
            texttemplate='%{text:,.1f}%',
            textposition='outside'
        )

        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},
            height=450,
            title_x=0.25,
            coloraxis_showscale=False,
            title_font=dict(size=15, color="#1A3FAA")
            )

        st.plotly_chart(fig, use_container_width=True)

    with page2:
        # Highest readmission rate by Gender
        
        rdmission_by_gen = (
        encount_nd_patient[encount_nd_patient['Readmission'] == True]
        .groupby('GENDER')
        .size()
        .reset_index(name='Readmission_rate')
        )

        rdmission_by_gen["GENDER"] = rdmission_by_gen["GENDER"].replace({
            "F": "Female",
            "M": "Male"
        })
        fig=px.pie(
        rdmission_by_gen,
        names='GENDER',
        values='Readmission_rate',
        title='Gender With Most Readmission',
        hole=0.2,
        color='GENDER',
        color_discrete_map={
        'Female': "#b5e794",
        'Male': "#561bc3"
        }
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
            legend_title='Gender'
        )

        st.plotly_chart(fig, use_container_width=True)

    with page3:
        #  Highest readmission rate by Marital Status
        patient_readmission = (
            encount_nd_patient
            .groupby('PATIENT')['Readmission']
            .any()
            .reset_index()
        )
        
        patient_marital = (
            encount_nd_patient[['PATIENT', 'MARITAL']]
            .drop_duplicates('PATIENT')
        )

        patient_readmission = patient_readmission.merge(
            patient_marital,
            on='PATIENT',
            how='left'
        )

        readmitted_patients = (
            patient_readmission[patient_readmission['Readmission']]
            .groupby('MARITAL')
            .size()
        )

        total_patients = (
            patient_readmission
            .groupby('MARITAL')
            .size()
        )

        readmission_rate = (
            readmitted_patients / total_patients * 100
        ).fillna(0)

        rdmission_by_status = (
            readmission_rate
            .reset_index(name='Readmission_Rate')
            .sort_values('Readmission_Rate', ascending=False)
        )

        fig=px.bar(
        rdmission_by_status,
        x="Readmission_Rate",
        y="MARITAL",
        title="Marital Status With Highest Readmission Rate",
        orientation="h",
        color="MARITAL",
        color_continuous_scale=["#880579", "#b2fe00"], 
        text="Readmission_Rate"
        )

        fig.update_traces(
            texttemplate='%{x:,.1f}%',
            textposition='outside'
        )

        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},
            height=450,
            title_x=0.25,
            coloraxis_showscale=False,
            title_font=dict(size=15, color="#1A3FAA")
            )

        st.plotly_chart(fig, use_container_width=True)

    pole1, pole2 = st.tabs(['Tab 1', 'Tab 2'])

    with pole1:
        # Which City have the most patients?
        patient_by_state = (
            patient.groupby('CITY')['Id']
            .size()
            .reset_index(name='Total_patient')
            .sort_values('Total_patient', ascending=False)
            .head(10)
        )

        fig=px.bar(
        patient_by_state,
        x="Total_patient",
        y="CITY",
        title="City With Most Patients",
        orientation="h",
        color="CITY",
        color_continuous_scale=["#880579", "#b2fe00"], 
        text="Total_patient"
        )

        fig.update_traces(
            texttemplate='%{x:,.0f}',
            textposition='outside'
        )

        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},
            height=450,
            title_x=0.25,
            coloraxis_showscale=False,
            title_font=dict(size=15, color="#1A3FAA")
            )

        st.plotly_chart(fig, use_container_width=True)

    with pole2:
        # How has patient volume changed over time?

        month_order = [
        'Jan','Feb','Mar','Apr','May','Jun',
        'Jul','Aug','Sep','Oct','Nov','Dec'
        ]

        encount_nd_patient['START_DATE'] = pd.to_datetime(encount_nd_patient['START_DATE'])

        encount_nd_patient['Month'] = (
            encount_nd_patient['START_DATE']
            .dt.to_period('M')
            .astype(str)
        )

        patient_volume = (
            encount_nd_patient.groupby('Month')['PATIENT']
            .nunique()
            .reset_index(name='Patient_Count')
        )

        fig = px.area(
            patient_volume,
            x='Month',
            y='Patient_Count',
            title='Patient Volume Over Time'
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
            xaxis_title='Month',
            yaxis_title='Patient Count',
            height=450,
            title_font=dict(size=15, color="#7287ef")
        )

        st.plotly_chart(fig, use_container_width=True)
   

st.space(size="medium")

with right_column:
    # Which gender accounts for the most encounters?
    encount_by_gen = (
        encount_nd_patient.groupby('GENDER')['Id_x']
        .size()
        .reset_index(name='Total_Encounter')
    )

    encount_by_gen["GENDER"] = encount_by_gen["GENDER"].replace({
    "F": "Female",
    "M": "Male"
    })

    fig=px.pie(
        encount_by_gen,
        names='GENDER',
        values='Total_Encounter',
        title='Gender With Most Encounter',
        hole=0.2,
        color='GENDER',
        color_discrete_map={
        'Female': "#b5e794",
        'Male': "#561bc3"
        }
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
        legend_title='Gender'
    )

    st.plotly_chart(fig, use_container_width=True)

    pocket1, pocket2, pocket3 = st.tabs(['Pocket 1', 'Pocket 2', 'Pocket 3'])

    with pocket1:
        # Demographic with Highest Mortality Rate
        patient['Died'] = (patient['DEATHDATE'] != "Alive")

        mortality_by_race = (
            patient.groupby('RACE')
            .agg(
                Total_Patients=('Id', 'nunique'),
                Deaths=('Died', 'sum')
            )
            .reset_index()  
        )

        mortality_by_race['Mortality_Rate'] = (
            mortality_by_race['Deaths']
            / mortality_by_race['Total_Patients']
            * 100
        )

        mortality_by_race = mortality_by_race.sort_values(
            'Mortality_Rate',
            ascending=False
        )

        # st.write(mortality_by_race)

        fig=px.bar(
        mortality_by_race,
        x="Mortality_Rate",
        y="RACE",
        title="Mortality Rate by Race",
        orientation="h",
        color="RACE",
        color_continuous_scale=["#1e293b", "#00f2fe"], 
        text="Mortality_Rate"
        )

        fig.update_traces(
            texttemplate='%{text:,.1f}%',
            textposition='outside'
        )

        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},
            height=450,
            title_x=0.25,
            coloraxis_showscale=False,
            title_font=dict(size=15, color="#1A3FAA")
            )

        st.plotly_chart(fig, use_container_width=True)

    with pocket2:
        # Gender with Highest Mortality Rate
        mortality_by_gender = (
            patient.groupby('GENDER')
            .agg(
                Total_Patients=('Id', 'nunique'),
                Deaths=('Died', 'sum')
            )
            .reset_index()  
        )

        mortality_by_gender['Mortality_Rate'] = (
            mortality_by_gender['Deaths']
            / mortality_by_gender['Total_Patients']
            * 100
        )

        mortality_by_gender = mortality_by_gender.sort_values(
            'Mortality_Rate',
            ascending=False
        )

        mortality_by_gender["GENDER"] = mortality_by_gender["GENDER"].replace({
        "F": "Female",
        "M": "Male"
        })

        # st.write(mortality_by_gender)
        fig=px.pie(
        mortality_by_gender,
        names='GENDER',
        values='Mortality_Rate',
        title='Gender with Highest Mortality Rate',
        hole=0.2,
        color='GENDER',
        color_discrete_map={
        'Female': "#6f80ca",
        'Male': "#ecb82a"
        }
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
            legend_title='Gender'
        )

        st.plotly_chart(fig, use_container_width=True)

    with pocket3:
        # Age Group with Highest Mortality Rate
        birthdates_clean = pd.to_datetime(patient['BIRTHDATE'], errors='coerce')
        patient['AGE'] = (pd.Timestamp.today() - birthdates_clean).dt.days // 365

        patient['Age_Group'] = pd.cut(
        patient['AGE'],
        bins=[0, 18, 35, 50, 65, 120],
        labels=['0-18', '19-35', '36-50', '51-65', '65+']
        )
    

        mortality_by_age = (
            patient.groupby('Age_Group')
            .agg(
                Total_Patients=('Id', 'nunique'),
                Deaths=('Died', 'sum')
            )
            .reset_index()  
        )

        mortality_by_age['Mortality_Rate'] = (
            mortality_by_age['Deaths']
            / mortality_by_age['Total_Patients']
            * 100
        )

        mortality_by_age = mortality_by_age.sort_values(
            'Mortality_Rate',
            ascending=False
        )

        # st.write(mortality_by_age)

        fig=px.bar(
        mortality_by_age,
        x="Mortality_Rate",
        y="Age_Group",
        title="Age Group with Highest Mortality Rate",
        orientation="h",
        color="Age_Group",
        color_continuous_scale=["#d29840", "#b8fc8a"], 
        text="Mortality_Rate"
        )

        fig.update_traces(
            texttemplate='%{text:,.1f}%',
            textposition='outside'
        )

        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},
            height=450,
            title_x=0.25,
            coloraxis_showscale=False,
            title_font=dict(size=15, color="#1A3FAA")
            )

        st.plotly_chart(fig, use_container_width=True)

    lob1, lob2, lob3 = st.tabs(['Tab 1', 'Tab 2', 'Tab 3'])

    with lob1:
        # Which procedures are performed most frequently?

        st.markdown(
            """
            <h3 style="
                color:#1A3FAA;
                font-size:20px;
                font-weight:bold;
                margin-bottom:10px;
            ">
                Top 40 Most Frequent Procedures
            </h3>
            """,
            unsafe_allow_html=True
        )

        most_freq_proc = (
            procedure.groupby('DESCRIPTION')['ENCOUNTER']
            .size()
            .reset_index(name='Procedure_count')
            .sort_values('Procedure_count', ascending=False)
        )
        styled_dbr = most_freq_proc.head(40).style.set_properties(
            **{
            'background-color': "#edeff1",
            'color': "#286b15",
            'border-color': '#286b15',
            'height': 200,
            }
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
            

        with st.container(border=True):
            st.dataframe(
                styled_dbr,
                height=300,
                hide_index=True,
                use_container_width=True
            )

    with lob2:
        # Which procedures generate the highest total costs?
        proce_with_highestcost = (
            encount_nd_proce.groupby('DESCRIPTION_x')['TOTAL_CLAIM_COST']
            .sum()
            .reset_index(name='Total_cost')
            .head(10)
        )        

        fig=px.bar(
        proce_with_highestcost,
        x="Total_cost",
        y="DESCRIPTION_x",
        title="Procedure with Highest Cost",
        orientation="h",
        color="Total_cost",
        color_continuous_scale=["#d29840", "#b8fc8a"], 
        text="Total_cost"
        )

        fig.update_traces(
            texttemplate=[f"${x:,.1f}" for x in proce_with_highestcost['Total_cost']],
            textposition='outside'
        )

        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},
            height=450,
            title_x=0.25,
            coloraxis_showscale=False,
            title_font=dict(size=15, color="#1A3FAA")
            )

        st.plotly_chart(fig, use_container_width=True)

    with lob3:
        # Procedure readmission Rate

        procedure_readmission_rate = (
            encount_nd_proce
            .groupby('DESCRIPTION_x')
            .agg(
                Total_Patients=('PATIENT_x', 'nunique'),
                Readmitted_Patients=('Readmitted_Within_30_Days', 'sum')
            )
            .reset_index()
        )

        procedure_readmission_rate['Readmission_Rate'] = (
            procedure_readmission_rate['Readmitted_Patients']
            / procedure_readmission_rate['Total_Patients']
            * 100
        )

        procedure_readmission_rate = (
            procedure_readmission_rate[
                procedure_readmission_rate['Total_Patients'] >= 20
            ]
            .sort_values('Readmission_Rate', ascending=False)
        )

        top_proc = procedure_readmission_rate.head(10)

        top_proc['Readmission_Rate'] = top_proc['Readmission_Rate']/100

        fig = px.bar(
            top_proc,
            x='Readmission_Rate',
            y='DESCRIPTION_x',
            orientation='h',
            title='Procedure Readmission Rate',
            text='Readmission_Rate',
            color='Readmission_Rate'
        )

        fig.update_traces(
            texttemplate='%{x:.1f}%',
            textposition='outside'
        )

        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title='Readmission Rate (%)',
            yaxis_title='Procedure',
            height=600,
            title_font=dict(size=15, color="#1A3FAA")
        )

        st.plotly_chart(fig, use_container_width=True)


st.markdown("""
<div class="section-title">
   Summary of Patient & Clinical Outcomes
</div>
<h3> 
1. Patients aged 65 years and above have the highest readmission rate (66.1%).
</h3> 
<h5>         
Recommendation
            
* Create a High-Risk Patient Follow-up Program for elderly patients.
* Schedule follow-up appointments before discharge.
* Increase medication counseling for older adults.
</h5>      

                                
<h3> 
2. Most patients come from Boston (541 patients).
</h3> 
<h5>         
Recommendation
            
* Expand outreach and preventive health services in these communities.
* Consider satellite clinics or community screening programs in Boston and nearby cities.
</h5>        

<h3> 
3. Prenatal care represents the highest total claim cost.
</h3> 
<h5>         
Recommendation
            
* Review prenatal service costs to identify opportunities for efficiency.
* Ensure appropriate coding and reimbursement for prenatal services.
* Evaluate resource utilization in high-cost service lines.
</h5> 

<h3> 
4. Some procedures show extremely high readmission rates.
</h3> 
<h5>         
Recommendation
            
* Audit postoperative care for procedures with consistently high readmission rates
* Enhance patient education and follow-up for surgical patients.
</h5>    

<h3> 
Overall Recommendation
</h3> 
            
<h5>         
Focus on elderly patients, high-cost procedures, and 
high-readmission procedures to improve patient outcomes and reduce repeat hospital visits.
</h5>              

 

            

""", unsafe_allow_html=True)