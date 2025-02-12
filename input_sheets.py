import csv
import json
import re
from datetime import datetime
import io
import streamlit as st

# Funzione per elaborare il campo "Gain"
def process_gain(gain_str):
    """
    Rimuove le parole "POINTS", "POINT" e "PIPS" lasciando solo il numero.
    Ad esempio: "-15 PIPS" diventa -15.
    """
    gain_str = gain_str.replace("POINTS", "").replace("POINT", "").replace("PIPS", "")
    gain_str = gain_str.strip()
    match = re.search(r'(-?\d+)', gain_str)
    if match:
        return int(match.group(1))
    else:
        return gain_str

# Funzione per elaborare il campo "StopLoss" e la data
def process_stoploss_and_date(line):
    """
    La riga è del tipo:
       "<status>    <MonthName> <DD>"
    Esempio: "stop-loss    February 10" oppure "won    February 04"
    
    La funzione:
      - Estrae lo status (ad es. "stop-loss" o "won")
      - Estrae la data (ad es. "February 10") e la converte nel formato YYYY-MM-DD
        usando l’anno corrente.
    """
    parts = line.split()
    if len(parts) < 2:
        status = ""
        date_str = line.strip()
    else:
        status = parts[0].strip()              # "stop-loss" o "won"
        date_str = " ".join(parts[1:]).strip()  # ad es. "February 10"
    
    try:
        parsed_date = datetime.strptime(date_str, "%B %d")
        current_year = datetime.now().year
        parsed_date = parsed_date.replace(year=current_year)
        date_formatted = parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        print(f"Errore nel parsing della data: '{date_str}'")
        date_formatted = date_str
        
    return status, date_formatted

# Funzione per combinare la data e l'orario
def combine_date_time(date_str, time_str):
    """
    Combina una data (in formato "YYYY-MM-DD") e un orario (in formato "hh:mm:ss AM/PM")
    per restituire una stringa datetime nel formato "YYYY-MM-DD HH:MM:SS" (24 ore).
    """
    combined_str = f"{date_str} {time_str}"
    try:
        # Il formato di input è: data in YYYY-MM-DD, orario in 12h con AM/PM
        dt_obj = datetime.strptime(combined_str, "%Y-%m-%d %I:%M:%S %p")
        return dt_obj.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        print("Errore nel combinare data e orario:", e)
        return combined_str

# Funzione per elaborare un record composto da 5 righe
def process_record(lines):
    if len(lines) < 5:
        return None
    symbol = lines[0].strip()
    action = lines[1].strip()
    gain = process_gain(lines[2].strip())
    stop_loss, date_formatted = process_stoploss_and_date(lines[3].strip())
    time_field = lines[4].strip()
    datetime_combined = combine_date_time(date_formatted, time_field)
    
    return {
        "Symbol": symbol,
        "Action": action,
        "Gain": gain,
        "StopLoss": stop_loss,
        "Datetime": datetime_combined
    }

# Funzione per aggiornare automaticamente i dati su Google Sheets
def update_google_sheet(records):
    """
    Aggiorna un Google Sheet con i record forniti.
    
    Assicurati di aver:
      - Installato le librerie: gspread e oauth2client
      - Configurato il file delle credenziali del service account (JSON)
      - Sostituito 'path_to_your_credentials.json' e 'YourGoogleSheetName' con i valori corretti.
    """
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    
    # Definisci lo scope per le API di Google
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # Carica il contenuto dal segreto
    credentials_str = st.secrets["google"]["service_account"]

    # Sostituisci i ritorni a capo letterali con le sequenze di escape
    credentials_str_fixed = credentials_str.replace('\n', '\\n')
    # Carica le credenziali dal segreto definito
    credentials_dict = json.loads(st.secrets["google"]["service_account"])

    # Autorizza il client usando le credenziali lette dai segreti
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(creds)
    
    # Apri il Google Sheet (puoi usare il nome o l'URL)
    sheet = client.open("trade-sfx").sheet1
    
    # Pulisce il foglio e inserisce l'intestazione
    sheet.clear()
    headers = ["Symbol", "Action", "Gain", "StopLoss", "Datetime"]
    sheet.append_row(headers)
    
    # Aggiunge ogni record come nuova riga
    for record in records:
        row = [
            record.get("Symbol"),
            record.get("Action"),
            record.get("Gain"),
            record.get("StopLoss"),
            record.get("Datetime")
        ]
        sheet.append_row(row)
    
    print("Dati aggiornati su Google Sheets.")

# -------------------------
# Data set fornito (puoi sostituirlo con la lettura da file se preferisci)
data_set = """EUR/CAD
buy
-15 PIPS
stop-loss	February 10
02:36:27 PM
GBP/CAD
buy
-15 PIPS
stop-loss	February 10
01:07:20 PM
EUR/USD
buy
-15 PIPS
stop-loss	February 10
01:04:49 PM
EUR/JPY
buy
-15 PIPS
stop-loss	February 05
09:15:45 AM
EUR/CAD
buy
-15 PIPS
stop-loss	February 05
08:48:18 AM
EUR/USD
buy
-15 PIPS
stop-loss	February 05
08:39:08 AM
USD/CAD
sell
-15 PIPS
stop-loss	February 04
09:02:27 AM
GBP/USD
buy
75 PIPS
won	February 04
08:10:01 AM
EUR/USD
buy
75 PIPS
won	February 04
08:04:33 AM
EUR/CHF
sell
15 PIPS
won	February 03
09:27:12 AM
GBP/CAD
sell
-15 PIPS
stop-loss	February 03
08:55:30 AM
EUR/USD
sell
15 PIPS
won	February 03
08:52:57 AM
EUR/CAD
buy
75 PIPS
won	January 14
09:22:38 AM
EUR/USD
buy
75 PIPS
won	January 14
08:16:42 AM
EUR/JPY
buy
-30 PIPS
stop-loss	January 14
12:12:00 AM
GBP/CAD
buy
60 PIPS
won	January 13
05:35:07 PM
EUR/CAD
buy
45 PIPS
won	January 13
05:30:03 PM
EUR/CAD
sell
75 PIPS
won	January 10
05:27:38 PM
EUR/USD
sell
75 PIPS
won	January 09
04:50:38 PM
GBP/CAD
sell
-30 PIPS
stop-loss	January 09
04:48:05 PM
"""

# Suddivide il testo in righe, rimuovendo eventuali righe vuote
lines = [line for line in data_set.splitlines() if line.strip() != ""]

# Ogni record è composto da 5 righe
records = []
record_size = 5
for i in range(0, len(lines), record_size):
    record_lines = lines[i:i+record_size]
    record = process_record(record_lines)
    if record:
        records.append(record)

# --- Produzione dell'output CSV (per test) ---
output_csv = io.StringIO()
fieldnames = ["Symbol", "Action", "Gain", "StopLoss", "Datetime"]
writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
writer.writeheader()
for record in records:
    writer.writerow(record)

print("Output CSV:")
print(output_csv.getvalue())

# --- Aggiorna i dati su Google Sheets ---
update_google_sheet(records)
