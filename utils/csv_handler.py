import csv
import os
from datetime import datetime

FILENAME = "ricerche.csv"

def accoda_su_csv(url, anno, esito):
    """
    Aggiunge una riga al file CSV.
    Se il file non esiste, lo crea con le intestazioni.
    """
    try:
        file_esiste = os.path.isfile(FILENAME)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(FILENAME, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Scriviamo l'intestazione solo la prima volta
            if not file_esiste:
                writer.writerow(["URL", "Anno", "Esito", "Data"])
            
            writer.writerow([url, anno, esito, timestamp])
            
    except Exception as e:
        print(f"Errore scrittura CSV: {e}")