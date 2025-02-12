import streamlit as st
import pandas as pd
from pathlib import Path
from script.parse_data import parse_run

# Seleziona l'anno tramite una selectbox
anno = st.selectbox('Che anno stai inserendo?', ['2025', '2024'])
# Seleziona il fornitore tramite una selectbox
fornitore = st.selectbox('Chi è il fornitore?', ['LunarEclipse-LKS', 'ReyNova-RYD'])


# Crea il form per l'input dei dati
with st.form(key='input_data', clear_on_submit=True):
    sentence = st.text_input('I trade da inserire', '')
    submit = st.form_submit_button(f'Aggiungi i trade per {fornitore}!')

if submit:
    if not sentence.strip():
        st.error('Non hai scritto niente!')
    else:
        # Aggiorna il CSV
        parse_run(sentence, fornitore)
        st.success('Trade aggiunti!')

# Visulalizza Dati CSV --------------------------------
st.title("Visualizzazione Dati CSV")

# Definisci il percorso al file CSV
data_path = Path("data/sfx_data.csv")

# Controlla se il file esiste
if data_path.exists():
    # Leggi il CSV in un DataFrame
    df = pd.read_csv(data_path)
    st.write("Dati dal CSV:")
    st.dataframe(df, key="my_data")
else:
    st.error(f"Il file CSV non è stato trovato: {data_path}")

