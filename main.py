import streamlit as st

st.set_page_config(
    page_title="Hospital Analytics Dashboard",
    page_icon="🏥",
    layout="wide"
)

pg = st.navigation([
    st.Page("hospital_app.py", title="Encounter Analytics", icon="🏥"),
    st.Page("Cost_insurance_insights.py", title="Cost & Insurance Insights", icon="💰"),
    st.Page("Patient_Analytics.py", title="Patient & Procedures Analytics", icon="👨‍⚕️"),
])

pg.run()