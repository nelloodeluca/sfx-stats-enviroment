import csv
import re
from datetime import datetime
import io

# Funzione per elaborare il campo "Gain"
def process_gain(gain_str):
    """
    Rimuove le parole "POINTS", "POINT" e "PIPS" lasciando solo il numero.
    Ad esempio: "-15 PIPS" diventa -15.
    """
    gain_str = gain_str.replace("POINTS", "").replace("POINT", "").replace("PIPS", "")
    gain_str = gain_str.strip()
    
    # Estrae il primo numero (eventualmente negativo)
    match = re.search(r'(-?\d+)', gain_str)
    if match:
        return int(match.group(1))
    else:
        return gain_str

# Funzione per elaborare il campo "StopLoss" e la data
def process_stoploss_and_date(line):
    """
    La riga è del tipo:
      "<status>   <MonthName> <DD>"
    Ad esempio: "stop-loss	February 10" oppure "won	February 04"
    La funzione:
      - Estrae lo status (ad es. "stop-loss" o "won")
      - Estrae la data (i restanti elementi) e la converte nel formato YYYY-MM-DD,
        usando l’anno corrente.
    """
    parts = line.split()
    if len(parts) < 2:
        status = ""
        date_str = line.strip()
    else:
        status = parts[0].strip()              # ad es. "stop-loss" o "won"
        date_str = " ".join(parts[1:]).strip()  # ad es. "February 10"

    try:
        # Parsing della data (formato: "MonthName DD")
        parsed_date = datetime.strptime(date_str, "%B %d")
        current_year = datetime.now().year
        parsed_date = parsed_date.replace(year=current_year)
        date_formatted = parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        print(f"Errore nel parsing della data: '{date_str}'")
        date_formatted = date_str
        
    return status, date_formatted

# Funzione per convertire l'orario in formato 12 ore (AM/PM) al formato 24 ore (HH:MM:SS)
def process_time(time_str):
    """
    Converte un orario in formato "hh:mm:ss AM/PM" nel formato "HH:MM:SS" (24 ore).
    Ad esempio: "12:22:02 AM" -> "00:22:02"
    """
    try:
        dt_obj = datetime.strptime(time_str, "%I:%M:%S %p")
        return dt_obj.strftime("%H:%M:%S")
    except ValueError as e:
        print("Errore nel parsing dell'orario:", e)
        return time_str

# Funzione per elaborare un record composto da 5 righe
def process_record(lines):
    if len(lines) < 5:
        return None
    symbol = lines[0].strip()
    action = lines[1].strip()
    gain = process_gain(lines[2].strip())
    stop_loss, date_formatted = process_stoploss_and_date(lines[3].strip())
    # Processa l'orario e lo converte nel formato 24 ore
    time_field = process_time(lines[4].strip())
    
    return {
        "Symbol": symbol,
        "Action": action,
        "Gain": gain,
        "StopLoss": stop_loss,
        "Date": date_formatted,
        "Time": time_field
    }

# Data set fornito come stringa multilinea
data_set = """XAU/USD
buy
100 PIPS
won	February 04
12:22:02 AM
XAU/USD
buy
20 PIPS
won	January 29
12:14:54 AM
"""

# Suddivide il testo in righe, rimuovendo eventuali righe vuote
lines = [line for line in data_set.splitlines() if line.strip() != ""]

# Si assume che ogni record sia composto da 5 righe
records = []
record_size = 5
for i in range(0, len(lines), record_size):
    record_lines = lines[i:i+record_size]
    record = process_record(record_lines)
    if record:
        records.append(record)

# Scrive l'output in formato CSV in una stringa (per la prova)
output_csv = io.StringIO()
fieldnames = ["Symbol", "Action", "Gain", "StopLoss", "Date", "Time"]
writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
writer.writeheader()
for record in records:
    writer.writerow(record)

# Stampa il CSV risultante
print(output_csv.getvalue())
