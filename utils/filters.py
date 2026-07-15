import streamlit as st

def apply_filters(encount):

    st.sidebar.header("Dashboard Filters")

    years = sorted(encount["YP"].dropna().unique())

    selected_years = st.sidebar.multiselect(
        "Select Year",
        years,
        default=years
    )

    encounter_classes = sorted(
        encount["ENCOUNTERCLASS"].dropna().unique()
    )

    selected_classes = st.sidebar.multiselect(
        "Encounter Class",
        encounter_classes,
        default=encounter_classes
    )

    months = sorted(encount["MP"].dropna().unique())

    selected_months = st.sidebar.multiselect(
        "Month",
        months,
        default=months
    )

    filtered_df = encount[
        (encount["YP"].isin(selected_years)) &
        (encount["ENCOUNTERCLASS"].isin(selected_classes)) &
        (encount["MP"].isin(selected_months))
    ]

    return filtered_df