import os
import shutil
import datetime
from pathlib import Path

def backup_csv_to_folder(file_path, backup_folder):
    """
    Crea un backup del file CSV in backup_folder.
    Restituisce il percorso del backup creato, oppure None se il file non esiste.
    """
    os.makedirs(backup_folder, exist_ok=True)
    if os.path.exists(file_path):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_folder, f"sfx_data_{timestamp}.csv")
        shutil.copy(file_path, backup_file)
        print(f"Backup creato in {backup_folder}: {backup_file}")
        return backup_file
    else:
        print("Nessun file CSV trovato per creare il backup.")
        return None

def undo_last_update(file_path, undo_folder="data/backups", redo_folder="data/redo"):
    """
    Esegue un'operazione di undo:
      1. Crea un backup dell'attuale stato del file CSV nella cartella redo.
      2. Ripristina il backup più recente dalla cartella undo nel file CSV principale.
    
    Restituisce True se l'undo è andato a buon fine, False altrimenti.
    """
    # Backup corrente per poter fare redo in seguito
    backup_csv_to_folder(file_path, redo_folder)
    
    # Verifica la presenza di backup nella cartella undo
    undo_dir = Path(undo_folder)
    if not undo_dir.exists():
        print("Cartella undo non trovata.")
        return False
    
    # Trova tutti i backup nella cartella undo
    backups = [os.path.join(undo_folder, f) for f in os.listdir(undo_folder)
               if f.startswith("sfx_data_") and f.endswith(".csv")]
    
    if not backups:
        print("Nessun backup disponibile per l'undo.")
        return False
    
    # Ordina i backup in ordine decrescente (l'ultimo creato in cima)
    backups.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    latest_backup = backups[0]
    shutil.copy(latest_backup, file_path)
    print(f"Undo completato: {latest_backup} è stato ripristinato in {file_path}.")
    return True

def redo_last_update(file_path, undo_folder="data/backups", redo_folder="data/redo"):
    """
    Esegue un'operazione di redo (cioè, annulla l'undo):
      1. Crea un backup dell'attuale stato del file CSV nella cartella undo.
      2. Ripristina il backup più recente dalla cartella redo nel file CSV principale.
    
    Restituisce True se il redo è andato a buon fine, False altrimenti.
    """
    # Backup corrente per poter annullare il redo (e fare nuovamente undo se necessario)
    backup_csv_to_folder(file_path, undo_folder)
    
    redo_dir = Path(redo_folder)
    if not redo_dir.exists():
        print("Cartella redo non trovata.")
        return False
    
    redo_backups = [os.path.join(redo_folder, f) for f in os.listdir(redo_folder)
                    if f.startswith("sfx_data_") and f.endswith(".csv")]
    
    if not redo_backups:
        print("Nessun backup disponibile per il redo.")
        return False
    
    redo_backups.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    latest_redo = redo_backups[0]
    shutil.copy(latest_redo, file_path)
    print(f"Redo completato: {latest_redo} è stato ripristinato in {file_path}.")
    return True
