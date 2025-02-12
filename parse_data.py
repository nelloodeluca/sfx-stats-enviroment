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

# Funzione per elaborare il campo "StopLoss" e "Date"
def process_stoploss_and_date(line):
    """
    La riga è del tipo:
      "<status>   <MonthName> <DD>"
    Ad esempio: "stop-loss	February 10" oppure "won	February 04"
    La funzione:
      - Estrae lo status (il primo elemento: "stop-loss" o "won")
      - Estrae la data (i restanti elementi) e la converte nel formato YYYY-MM-DD,
        usando l'anno corrente.
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

# Funzione per elaborare un record composto da 5 righe
def process_record(lines):
    if len(lines) < 5:
        return None
    symbol = lines[0].strip()
    action = lines[1].strip()
    gain = process_gain(lines[2].strip())
    stop_loss, date_formatted = process_stoploss_and_date(lines[3].strip())
    time_field = lines[4].strip()
    
    return {
        "Symbol": symbol,
        "Action": action,
        "Gain": gain,
        "StopLoss": stop_loss,
        "Date": date_formatted,
        "Time": time_field
    }

# Data set fornito come stringa multilinea
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
