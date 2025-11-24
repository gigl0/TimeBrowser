import csv
import os
from datetime import datetime

FILENAME = "ricerche.csv"

def accoda_su_csv(url, anno, esito):
    """
    Salva una riga nel file CSV (Append mode).
    Se il file non esiste, crea anche l'intestazione.
    """
    try:
        # Controlliamo se il file esiste per scrivere l'header
        file_esiste = os.path.isfile(FILENAME)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Apriamo in modalità 'a' (append) per aggiungere senza cancellare
        with open(FILENAME, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Se è la prima volta, scriviamo i nomi delle colonne
            if not file_esiste:
                writer.writerow(["URL_Originale", "Anno_Ricerca", "Esito", "Data_Log"])
            
            # Scriviamo i dati
            writer.writerow([url, anno, esito, timestamp])
            
    except Exception as e:
        print(f"Errore salvataggio CSV: {e}")