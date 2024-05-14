import streamlit as st

st.set_page_config(layout="wide")

# URL de votre tableau de bord Power BI
powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiYWMyMDIyNDYtMWJkOS00M2M3LTk4ZTEtNGYzNWJlNGNlMDJiIiwidCI6IjMzMTM1ZmE1LWY1YTctNGQ1Yy04NjMyLTlhMTdkNGFjZmE1YiIsImMiOjh9"

# Afficher le tableau de bord Power BI dans Streamlit
st.components.v1.iframe(powerbi_url, height=800)
