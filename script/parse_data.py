import csv
import re
from datetime import datetime
from pathlib import Path

# Funzione per elaborare il campo "Gain"
def process_gain(gain_str):
    gain_str = gain_str.replace("POINTS", "").replace("POINT", "").replace("PIPS", "")
    gain_str = gain_str.strip()
    match = re.search(r'(-?\d+)', gain_str)
    return int(match.group(1)) if match else gain_str

# Funzione per elaborare il campo "StopLoss" e la data
def process_stoploss_and_date(line):
    parts = line.split()
    if len(parts) < 2:
        status = ""
        date_str = line.strip()
    else:
        status = parts[0].strip()              # ad es. "stop-loss" o "won"
        date_str = " ".join(parts[1:]).strip()  # ad es. "January 10"
    try:
        current_year = datetime.now().year
        parsed_date = datetime.strptime(f"{date_str} {current_year}", "%B %d %Y")
        date_formatted = parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        print(f"Errore nel parsing della data: '{date_str}'")
        date_formatted = date_str
    return status, date_formatted

# Funzione per convertire l'orario dal formato 12 ore (AM/PM) a 24 ore (HH:MM:SS)
def process_time(time_str):
    try:
        dt_obj = datetime.strptime(time_str, "%I:%M:%S %p")
        return dt_obj.strftime("%H:%M:%S")
    except ValueError as e:
        print("Errore nel parsing dell'orario:", e)
        return time_str

# Funzione per elaborare un singolo record composto da 5 "righe"
def process_record(lines):
    if len(lines) < 5:
        return None
    symbol = lines[0].strip()
    action = lines[1].strip()
    gain = process_gain(lines[2].strip())
    stop_loss, date_formatted = process_stoploss_and_date(lines[3].strip())
    time_field = process_time(lines[4].strip())
    return {
        "Symbol": symbol,
        "Action": action,
        "Gain": gain,
        "StopLoss": stop_loss,
        "Date": date_formatted,
        "Time": time_field
    }

# Funzione per effettuare il parsing dell'intero dataset
def parse_data(data_set):
    """
    Se il data_set contiene newline, utilizza il metodo classico (ogni record su 5 righe).
    Altrimenti, assume che il data_set sia una singola riga con token separati da spazi,
    e che ogni record sia composto da 9 token.
    """
    data_set = data_set.strip()
    # Se troviamo almeno una newline, utilizziamo il metodo tradizionale.
    if "\n" in data_set:
        lines = [line for line in data_set.splitlines() if line.strip() != ""]
        records = []
        record_size = 5
        for i in range(0, len(lines), record_size):
            record_lines = lines[i:i+record_size]
            record = process_record(record_lines)
            if record:
                records.append(record)
        return records
    else:
        # Input su una sola riga: suddividi in token
        tokens = data_set.split()
        # Ogni record deve avere 9 token
        if len(tokens) % 9 != 0:
            raise ValueError("Il numero di token nell'input non è multiplo di 9. Totale token: {}".format(len(tokens)))
        records = []
        for i in range(0, len(tokens), 9):
            rec_tokens = tokens[i:i+9]
            # Ricostruisci le "righe" del record
            line1 = rec_tokens[0]  # Symbol
            line2 = rec_tokens[1]  # Action
            line3 = rec_tokens[2] + " " + rec_tokens[3]  # Gain (es. "75 PIPS")
            line4 = rec_tokens[4] + " " + rec_tokens[5] + " " + rec_tokens[6]  # StopLoss e Date (es. "won January 10")
            line5 = rec_tokens[7] + " " + rec_tokens[8]  # Time (es. "05:27:38 PM")
            record_lines = [line1, line2, line3, line4, line5]
            record = process_record(record_lines)
            if record:
                records.append(record)
        return records

# Funzione per salvare i record in un file CSV
def write_csv(records, output_file):
    fieldnames = ["Symbol", "Action", "Gain", "StopLoss", "Date", "Time", "Fornitore"]
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record)
    print(f"Output CSV scritto in: {output_file}")

# Funzione per rimuovere duplicati da una lista di record
def remove_duplicates(records):
    unique = []
    seen = set()
    for record in records:
        key = (
            record.get("Symbol"),
            record.get("Action"),
            record.get("Gain"),
            record.get("StopLoss"),
            record.get("Date"),
            record.get("Time"),
            record.get("Fornitore")
        )
        if key not in seen:
            seen.add(key)
            unique.append(record)
    return unique

# Funzione principale che elabora l'input e aggiorna il CSV
def parse_run(data_input, fornitore):
    # Elabora i nuovi record
    new_records = parse_data(data_input)
    for record in new_records:
        record["Fornitore"] = fornitore

    output_file = "data/sfx_data.csv"
    existing_records = []
    # Se il file CSV esiste già, carica i record esistenti
    if Path(output_file).exists():
        with open(output_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_records.append(row)

    # Unisci i record esistenti con quelli nuovi e rimuovi i duplicati
    all_records = existing_records + new_records
    unique_records = remove_duplicates(all_records)

    # Scrivi l'insieme aggiornato nel file CSV
    write_csv(unique_records, output_file)
