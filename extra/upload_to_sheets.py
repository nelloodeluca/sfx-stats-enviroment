import csv
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st  # Per accedere a st.secrets

def update_google_sheet(records):
    """
    Aggiorna un Google Sheet con i record forniti.
    
    È necessario aver configurato i segreti (st.secrets) con il file JSON delle credenziali.
    """
    # Definisce lo scope per le API di Google
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # Carica le credenziali dal segreto definito (assicurati che in st.secrets il JSON sia corretto)
    credentials_str = st.secrets["google"]["service_account"]
    # Se necessario, sostituisci i ritorni a capo letterali con le sequenze di escape
    credentials_str_fixed = credentials_str.replace('\n', '\\n')
    credentials_dict = json.loads(credentials_str_fixed)

    # Autorizza il client usando le credenziali
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(creds)
    
    # Apri il Google Sheet (sostituisci "trade-sfx" con il nome (o ID) del tuo sheet)
    sheet = client.open("trade-sfx").sheet1
    
    # Pulisce il foglio e inserisce l'intestazione
    sheet.clear()
    headers = ["Symbol", "Action", "Gain", "StopLoss", "Date", "Time"]
    sheet.append_row(headers)
    
    # Aggiunge ogni record come nuova riga
    for record in records:
        row = [
            record.get("Symbol"),
            record.get("Action"),
            record.get("Gain"),
            record.get("StopLoss"),
            record.get("Date"),
            record.get("Time")
        ]
        sheet.append_row(row)
    
    print("Dati aggiornati su Google Sheets.")

def load_records_from_csv(csv_file):
    """
    Legge i record da un file CSV e li restituisce come lista di dizionari.
    """
    records = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records

# --- Esempio di utilizzo ---
if __name__ == '__main__':
    # Carica i record dal CSV generato dallo script di parsing
    records = load_records_from_csv("data/sfx_data.csv")
    update_google_sheet(records)
