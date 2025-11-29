import csv
import os
from datetime import datetime

FILENAME = "ricerche.csv"

def accoda_su_csv(url: str, anno: str, esito: str) -> None:
    """
    Salva i dettagli di una ricerca accodandoli al file CSV locale.

    Verifica l'esistenza del file 'ricerche.csv':
    - Se non esiste, lo crea e scrive la riga di intestazione (Header).
    - Se esiste, appende la nuova riga con i dati forniti.

    Args:
        url (str): L'URL del sito cercato.
        anno (str): L'anno di riferimento della ricerca.
        esito (str): Il risultato dell'operazione (es. numero snapshot).
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