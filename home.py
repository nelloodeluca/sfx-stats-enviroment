import streamlit as st
from pathlib import Path
import pandas as pd

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
st.header("Dashboard")
st.write("Benvenuto nella Dashboard!")


# Definisci il percorso al file CSV
data_path = Path("data/sfx_data.csv")

# Controlla se il file esiste
if data_path.exists():
    # Leggi il CSV in un DataFrame
    df = pd.read_csv(data_path)
else:
    st.error(f"Il file CSV non è stato trovato: {data_path}")

st.area_chart(df, x='Fornitore', y="Gain")
