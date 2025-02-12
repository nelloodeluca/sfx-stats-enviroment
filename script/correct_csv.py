import csv
import re
from datetime import datetime

def fix_gain(gain_str):
    """
    Corregge il campo "Gain" rimuovendo le parole "POINTS", "POINT" e "PIPS"
    e lasciando solo il numero.
    Esempio: "-15 PIPS" diventa "-15".
    """
    gain_str = gain_str.replace("POINTS", "").replace("POINT", "").replace("PIPS", "").strip()
    match = re.search(r'(-?\d+)', gain_str)
    if match:
        return match.group(1)
    return gain_str

def fix_date(date_str):
    """
    Controlla e corregge il campo "Date". Se la data non è nel formato
    "YYYY-MM-DD", prova a interpretarla assumendo che sia nel formato "MonthName DD"
    (es. "February 10") e aggiunge l'anno corrente.
    Se il parsing va a buon fine, restituisce la data formattata come "YYYY-MM-DD".
    Altrimenti restituisce la stringa originale.
    """
    date_str = date_str.strip()
    # Se la data è già nel formato "YYYY-MM-DD" la restituisce così com'è
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return date_str
    try:
        current_year = datetime.now().year
        # Proviamo a parsare la data assumendo il formato "MonthName DD"
        dt = datetime.strptime(f"{date_str} {current_year}", "%B %d %Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        # Se il parsing fallisce, restituisce la stringa originale
        return date_str

def fix_time(time_str):
    """
    Controlla e corregge il campo "Time". Se l'orario non è nel formato
    "HH:MM:SS" (24 ore), prova a interpretarlo come un orario in formato 12 ore
    (es. "12:22:02 AM") e lo converte nel formato a 24 ore.
    Se il parsing fallisce, restituisce la stringa originale.
    """
    time_str = time_str.strip()
    # Se l'orario è già nel formato 24 ore, lo restituisce
    if re.match(r'^\d{2}:\d{2}:\d{2}$', time_str):
        return time_str
    try:
        dt = datetime.strptime(time_str, "%I:%M:%S %p")
        return dt.strftime("%H:%M:%S")
    except ValueError:
        return time_str

def process_csv(input_file, output_file):
    """
    Legge il file CSV di input, corregge i campi "Gain", "Date" e "Time"
    e scrive il risultato in un nuovo file CSV.
    """
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        # Usa lo stesso header del file di input
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            if 'Gain' in row:
                row['Gain'] = fix_gain(row['Gain'])
            if 'Date' in row:
                row['Date'] = fix_date(row['Date'])
            if 'Time' in row:
                row['Time'] = fix_time(row['Time'])
            writer.writerow(row)
    
    print(f"File corretto scritto in: {output_file}")

if __name__ == '__main__':
    # Specifica il file di input e quello di output
    input_csv = "data/sfx_data.csv"
    output_csv = "data/corrected_output.csv"
    process_csv(input_csv, output_csv)
