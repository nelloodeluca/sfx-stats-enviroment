import streamlit as st
from pathlib import Path
import pandas as pd
from script.parse_data import parse_run

st.set_page_config(
    page_title="Dashboard SFX",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.title("Dashboard")
st.write("Benvenuto nella Dashboard!")