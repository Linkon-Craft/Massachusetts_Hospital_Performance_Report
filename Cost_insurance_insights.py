import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

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
    Cost and Coverage Insights
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
            procedure = pd.read_csv("payers.csv")
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


total_enct_cost = encount["TOTAL_CLAIM_COST"].sum()
avg_cost_per_vist = encount['TOTAL_CLAIM_COST'].mean()
encount_nd_payers['Revenue_Proxy'] = np.where(
    (
        (encount_nd_payers['PAYER_COVERAGE'].fillna(0) == 0)
        &
        (encount_nd_payers['TOTAL_CLAIM_COST'].fillna(0) == 0)
    ),
    encount_nd_payers['BASE_ENCOUNTER_COST'],
    encount_nd_payers['PAYER_COVERAGE']
)
avg_operating_margin = (
    np.where(
        encount_nd_payers['Revenue_Proxy'] > 0,
        (
            encount_nd_payers['Revenue_Proxy']
            - encount_nd_payers['BASE_ENCOUNTER_COST']
        )
        / encount_nd_payers['Revenue_Proxy'],
        0
    )
).mean() * 100
bad_debt_amount = (
    encount_nd_payers[
        (encount_nd_payers['NAME'] != 'NO_INSURANCE') &
        (encount_nd_payers['PAYER_COVERAGE'] == 0)
    ]['TOTAL_CLAIM_COST']
    .sum()
)
cost_covered_pct = (
    encount_nd_payers['PAYER_COVERAGE'].sum()
    /
    encount_nd_payers['TOTAL_CLAIM_COST'].sum()
    * 100
)
oop_amount = encount_nd_payers['TOTAL_CLAIM_COST'] - encount_nd_payers['PAYER_COVERAGE']
total_oop = oop_amount.sum()


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
        <div class="kpi-title">Total Encounter Cost</div>
        <div class="kpi-value">${round(total_enct_cost/1000000):.0f}M</div>
    </div>
    """, unsafe_allow_html=True)

with cols[2]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Average Cost Per Visit</div>
        <div class="kpi-value">${avg_cost_per_vist/1000:.1f}K</div>
    </div>
    """, unsafe_allow_html=True)

with cols[3]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Operating Margin</div>
        <div class="kpi-value">{avg_operating_margin:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with cols[4]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Bad Debt Amount</div>
        <div class="kpi-value">${human_format(bad_debt_amount)}M</div>
    </div>
    """, unsafe_allow_html=True)

with cols[5]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">% Cost Covered</div>
        <div class="kpi-value">{cost_covered_pct:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with cols[6]:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Out_Of_Pocket Share</div>
        <div class="kpi-value">{human_format(total_oop)}M</div>
    </div>
    """, unsafe_allow_html=True)


left_column, right_column = st.columns(2)

with left_column:
    
    st.markdown(
    '<p style="color:#1A3FAA; font-size:30px; font-weight:600; text-align:left;">'
    'COST AND INSURANCE OVERVIEW'
    '</p>', 
    unsafe_allow_html=True
    )

    coverage_by_insurer = (
    encount_nd_payers
    .groupby('NAME')['PAYER_COVERAGE']
    .sum()
    .reset_index(name='Total_Coverage')
    .sort_values('Total_Coverage', ascending=False)
    )

    fig = px.bar(
    coverage_by_insurer,
    x='Total_Coverage',
    y='NAME',
    orientation='h',
    text='Total_Coverage',
    color='Total_Coverage',
    color_continuous_scale=["#a335bc", "#0CC40F"],
    title='Insurers Covering the Largest Share of Costs',
    text_auto=True
    )
    
    fig.update_traces(
    texttemplate='$%{x:,.0f}',
    textposition='outside'
    )

    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        height=400,
        title_x=0.2,
        xaxis_title='Total Coverage Amount ($)',
        yaxis_title='Insurer',
        coloraxis_showscale=False,
        title_font=dict(size=15, color="#1A3FAA")
    )

    st.plotly_chart(fig, use_container_width=True)


    # Insurance  COVERAGE

    insurer_costs = (
    encount_nd_payers
    .groupby('NAME')['TOTAL_CLAIM_COST']
    .sum()
    .reset_index(name='Total_Claim_Cost')
    .sort_values('Total_Claim_Cost', ascending=False)
    )
    insurer_costs['Coverage_M'] = (
    insurer_costs['Total_Claim_Cost'] / 1_000_000
    ).round(1)


    fig = px.bar(
    insurer_costs,
    x='Total_Claim_Cost',
    y='NAME',
    orientation='h',
    text='Coverage_M',
    color='NAME',
    color_continuous_scale=["#a335bc", "#0CC40F"],
    title='TOTAL CLAIM COST BY PAYERS',
    text_auto=True
    )
    
    fig.update_traces(
        texttemplate='$%{text}M',
        textposition='outside'
    )

    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        height=400,
        title_x=0.2,
        xaxis_title='Total_Claim_Cost',
        yaxis_title='Payers',
        coloraxis_showscale=False,
        title_font=dict(size=15, color="#1A3FAA")
    )

    st.plotly_chart(fig, use_container_width=True)

    tabs1, tabs2, tabs3 = st.tabs(['Tabs 1', 'Tabs 2', 'Tabs 3'])
    with tabs1:   
        oop_by_gender = (
        encount_nd_patient
        .groupby('GENDER')['Out_of_Pocket']
        .mean()
        .reset_index()
        )
        oop_by_gender['Out_of_Pocket'] = oop_by_gender['Out_of_Pocket']/1000

        fig = px.bar(
        oop_by_gender,
        x='GENDER',
        y='Out_of_Pocket',
        text='Out_of_Pocket',
        color='GENDER',
        title='Average Out-of-Pocket Cost by Gender'
        )

        fig.update_traces(
            texttemplate='$%{y:,.1f}K',
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
    with tabs2:

        oop_by_race = (
        encount_nd_patient
        .groupby('RACE')['Out_of_Pocket']
        .mean()
        .reset_index()
        )

        oop_by_race['Out_of_Pocket'] = oop_by_race['Out_of_Pocket']/1000

        fig = px.bar(
        oop_by_race,
        x='RACE',
        y='Out_of_Pocket',
        text='Out_of_Pocket',
        color='RACE',
        title='Average Out-of-Pocket Cost by Race'
        )

        fig.update_traces(
            texttemplate='$%{y:,.1f}K',
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
    
    with tabs3:

        encount_nd_patient['BIRTHDATE'] = pd.to_datetime(encount_nd_patient['BIRTHDATE'])

        encount_nd_patient['AGE'] = (
            (pd.Timestamp.today() - encount_nd_patient['BIRTHDATE']).dt.days // 365
        )

        encount_nd_patient['Age_Group'] = pd.cut(
        encount_nd_patient['AGE'],
        bins=[0, 18, 35, 50, 65, 120],
        labels=['0-18', '19-35', '36-50', '51-65', '65+']
        )

        oop_by_age = (
            encount_nd_patient.groupby('Age_Group')['Out_of_Pocket']
            .mean()
            .reset_index()
        )

        oop_by_age['Out_of_Pocket'] = oop_by_age['Out_of_Pocket']/1000

        fig = px.bar(
        oop_by_age,
        x='Age_Group',
        y='Out_of_Pocket',
        text='Out_of_Pocket',
        color='Age_Group',
        title='Average Out-of-Pocket Cost by AGE'
        )

        fig.update_traces(
            texttemplate='$%{y:,.1f}K',
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


with right_column:
    encount_nd_payers['avg_operating_margin'] = (
        np.where(
            encount_nd_payers['Revenue_Proxy'] > 0,
            (
                encount_nd_payers['Revenue_Proxy']
                - encount_nd_payers['BASE_ENCOUNTER_COST']
            )
            / encount_nd_payers['Revenue_Proxy'],
            0
        )
    )

    profit_by_class = (
    encount_nd_payers
    .groupby('ENCOUNTERCLASS')['avg_operating_margin']
    .mean()
    .reset_index(name='avg_margin')
    .sort_values('avg_margin', ascending=False)
    )

    profit_by_class['Operating_Margin_Pct'] = (
    profit_by_class['avg_margin'] * 100
    ).round(2)


    profit_by_class = profit_by_class.sort_values(
    'Operating_Margin_Pct',
    ascending=False
    )

    profit_by_class['Margin_Color'] = np.where(
    profit_by_class['Operating_Margin_Pct'] >= 0,
    'Profit',
    'Loss'
    )

    fig = px.bar(
    profit_by_class,
    x="Operating_Margin_Pct",
    y="ENCOUNTERCLASS",
    title="Profit Generated by Encounter Class",
    orientation='h',
    text='Operating_Margin_Pct',
    color='Margin_Color',
    color_discrete_map={
        'Profit': '#22c55e',
        'Loss': '#ef4444'
    }
    )

    fig.update_traces(
    texttemplate='%{x:,.2f}%',
    textposition='outside'
    )

    
    fig.update_layout(
    yaxis={'categoryorder':'total ascending'},
    height=450,
    title_x=0.25,
    xaxis_title='Average Operating Margin (%)',
    yaxis_title='Encounter Class',
    coloraxis_showscale=False,
    title_font=dict(size=15, color="#1A3FAA")
    )

    st.plotly_chart(fig, use_container_width=True)


    tab1, tab2, tab3 = st.tabs(['Tab 1', 'Tab 2', 'Tab 3'])
    with tab1:
    # What is the % of encounters Cost covered by Insurance

        coverage_by_class = (
        encount_nd_payers
        .groupby('ENCOUNTERCLASS')
        .agg(
            Total_Claim_Cost=('TOTAL_CLAIM_COST', 'sum'),
            Total_Payer_Coverage=('PAYER_COVERAGE', 'sum')
        )
        .reset_index()
        )

        coverage_by_class['Cost_Covered_Pct'] = (
        coverage_by_class['Total_Payer_Coverage']
        / coverage_by_class['Total_Claim_Cost']
        * 100
        ).round(2)

        coverage_by_class = coverage_by_class.sort_values(
        'Cost_Covered_Pct',
        ascending=False
        )

        fig = px.bar(
        coverage_by_class,
        x='Cost_Covered_Pct',
        y='ENCOUNTERCLASS',
        orientation='h',
        text='Cost_Covered_Pct',
        color='Cost_Covered_Pct',
        color_continuous_scale=[
            '#dbeafe',
            '#60a5fa',
            "#ccd81d",
            "#1dd8a0",
            "#a63d93"
        ],
        title='ENCOUNTER CLASS COVERAGE'
        )

        fig.update_traces(
        texttemplate='%{x:.2f}%',
        textposition='outside'
        )

        fig.update_layout(
            height=450,
            title_x=0.25,
            xaxis_title='% Cost Covered',
            yaxis_title='Encounter Class',
            coloraxis_showscale=False,
            yaxis={'categoryorder': 'total ascending'},
            title_font=dict(size=20, color="#1A3FAA")
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        total_claim_cost = encount_nd_payers['TOTAL_CLAIM_COST'].sum()

        total_covered = encount_nd_payers['PAYER_COVERAGE'].sum()

        total_uncovered = total_claim_cost - total_covered

        coverage_pie = pd.DataFrame({
        'Category': ['Covered by Insurance', 'Not Covered'],
        'Amount': [total_covered, total_uncovered]
        })


        fig = px.pie(
            coverage_pie,
            names='Category',
            values='Amount',
            title='Percentage of Encounter Costs Covered by Insurance',
            hole=0.45
        )

        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate=
            '<b>%{label}</b><br>' +
            'Amount: $%{value:,.0f}<br>' +
            'Percentage: %{percent}<extra></extra>'
        )

        fig.update_layout(
            height=450,
            title_x=0.2,
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown(
        '<p style="color:#1A3FAA; font-size:30px; font-weight:600; text-align:left;">'
        'Encounter Procedure By Total Claim Cost'
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

        desc_by_cost = (
        encount_nd_proce
        .groupby('DESCRIPTION_x')['TOTAL_CLAIM_COST']
        .sum()
        .reset_index(name='TOTAL_COST')
        .sort_values('TOTAL_COST', ascending=False)
        )

        desc_by_cost['TOTAL_COST'] = desc_by_cost['TOTAL_COST'].apply(
        lambda x: f'${x/1_000_000:.2f}M'
        )

        styled_dbr = desc_by_cost.head(20).style.set_properties(
            **{
            'background-color': "#edeff1",
            'color': "#286b15",
            'border-color': '#286b15',
            'height': 200,
            }
        )
    

        with st.container(border=True):
            st.dataframe(styled_dbr,height=300, hide_index=True, use_container_width=True)


    side1, side2, side3 = st.tabs(['side1', 'side2', 'side3'])

    with side1:
        # Avg Base Cost by Encounter Class

        avg_base_enct = (
            encount_nd_payers.groupby(['ENCOUNTERCLASS']).agg(
                avg_base=('BASE_ENCOUNTER_COST', 'mean')
            ).sort_values('avg_base', ascending=False).reset_index()
            )
        
        fig = px.bar(
        avg_base_enct, 
        x="avg_base",       
        y="ENCOUNTERCLASS",      
        title="Average Base Cost by Encounter Class",
        orientation="h",       
        color="ENCOUNTERCLASS",    
        color_continuous_scale=["#96f44d", "#00f2fe"], 
        text="avg_base"      
        )

        fig.update_traces(
        texttemplate='$%{x:.2f}',
        textposition='outside'
        )

        fig.update_layout(
            height=450,
            title_x=0.25,
            xaxis_title='Avg Base_Cost',
            yaxis_title='Encounter Class',
            coloraxis_showscale=False,
            yaxis={'categoryorder': 'total ascending'},
            title_font=dict(size=20, color="#1A3FAA")
        )

        st.plotly_chart(fig, use_container_width=True)


    with side2:
        # Average Total Cost by Encounter

        avg_cost_by_class = (
        encount_nd_payers
        .groupby('ENCOUNTERCLASS')['TOTAL_CLAIM_COST']
        .mean()
        .reset_index(name='Avg_Cost_Per_Encounter')
        .sort_values('Avg_Cost_Per_Encounter', ascending=False)
        )
        
        avg_cost_by_class['Avg_Cost_K'] = (
        avg_cost_by_class['Avg_Cost_Per_Encounter'] / 1000
        ).round(1)

        fig = px.pie(
            avg_cost_by_class,
            names='ENCOUNTERCLASS',
            values='Avg_Cost_Per_Encounter',
            title='Average Total Cost by Encounter',
            hole=0.45
        )

        fig.update_traces(
        text=avg_cost_by_class['Avg_Cost_K'].astype(str) + 'K',
        textinfo='label+text',
        textposition='inside',
        hovertemplate=
        '<b>%{label}</b><br>' +
        'Cost: $%{value:,.1f}<br>' +
        '<extra></extra>'
        )

        fig.update_layout(
            height=450,
            title_x=0.2,
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)
    
    with side3:
        #Bad debt amount by Encounter Class

        encount_nd_payers['Unpaid_Cost'] = (
            encount_nd_payers[
                (encount_nd_payers['NAME'] != 'NO_INSURANCE') &
                (encount_nd_payers['PAYER_COVERAGE'] == 0)
            ]['TOTAL_CLAIM_COST']- encount_nd_payers['PAYER_COVERAGE']
        )
  
        
                
        
        bad_debt_by_class = (
            encount_nd_payers
            .groupby('ENCOUNTERCLASS')['Unpaid_Cost']
            .sum()
            .reset_index()
            .sort_values('Unpaid_Cost', ascending=False)
        )

        bad_debt_by_class['Unpaid_M'] = (
            bad_debt_by_class['Unpaid_Cost'] / 1_000_000
        ).round(1)

        fig = px.bar(
        bad_debt_by_class,
        x='Unpaid_Cost',
        y='ENCOUNTERCLASS',
        orientation='h',
        text='Unpaid_M',
        color='Unpaid_Cost',
        color_continuous_scale='Blues',
        title='Bad debt amount by Encounter Class'
        )

        fig.update_traces(
            texttemplate='$%{text}M',
            textposition='outside'
        )

        fig.update_layout(
            height=450,
            title_x=0.25,
            xaxis_title='Unpaid Cost($)',
            yaxis_title='Encounter Class',
            coloraxis_showscale=False,
            title_font=dict(size=15, color="#1A3FAA")
        )

        st.plotly_chart(fig, use_container_width=True)


st.markdown("""
<div class="section-title">
    Summary of Financial & Insurance Performance
</div>
<h3> 
1. Ambulatory encounters generate the largest amount of unpaid claims ($8.25 million).
</h3> 
<h5>         
Recommendation
            
* Audit denied or unpaid ambulatory claims.
* Improve coding accuracy before claims are submitted.
* Follow up on outstanding claims more aggressively.
</h5>      

                                
<h3> 
2. Medicare is the hospital's largest payer.
</h3> 
<h5>         
Recommendation
            
* Maintain strong relationships with Medicare and Medicaid.
* Review reimbursement performance from smaller insurers.
* Investigate why some insurers contribute very little to overall reimbursements.
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
4. Out-of-pocket expenses remain substantial.
</h3> 
<h5>         
Recommendation
            
* Increase insurance enrollment assistance.
* Provide financial counseling for uninsured and underinsured patients.
* Explore payment plans to reduce financial barriers to care.
</h5>    

<h3> 
Overall Recommendation
</h3> 
            
<h5>         
The hospital should prioritize reducing unpaid ambulatory claims, improving insurance 
reimbursement processes, managing the costs of high-expense services like prenatal care,
 and helping patients reduce out-of-pocket expenses.
</h5>              

 

            

""", unsafe_allow_html=True)