'''
Autore: Iglis Gjoni
Data: 12/11/2025

Titolo: TimeBrowser 2.0 – Analizzatore storico e anagrafico dei siti web
'''

# ///// SEZIONE IMPORT LIBRERIE
import requests
import json
import webbrowser
import csv
import whois
from datetime import datetime

# ------------------------------------------------------------
# ///// SEZIONE INPUT
def richiediInput() -> dict:
    '''
    ///// Funzione: richiediInput
    Richiede all’utente l’URL del sito da analizzare e la data di riferimento.
    L’utente può specificare anno, mese e giorno (questi ultimi opzionali).

    Valore di ritorno:
    dict -> dizionario con le chiavi 'url', 'anno', 'mese', 'giorno'
    '''
    url = input("Inserisci l'URL del sito (es. https://www.example.com): ").strip()
    anno = input("Inserisci l'anno (es. 2020): ").strip()
    mese = input("Inserisci il mese [opzionale, 01-12]: ").strip()
    giorno = input("Inserisci il giorno [opzionale, 01-31]: ").strip()

    return {"url": url, "anno": anno, "mese": mese, "giorno": giorno}

# ------------------------------------------------------------
# ///// SEZIONE WHOIS
def analizzaDominio(url: str) -> None:
    '''
    ///// Funzione: analizzaDominio
    Analizza il dominio utilizzando la libreria python-whois e
    mostra informazioni anagrafiche di base (registrar, creazione, scadenza).

    Parametri formali:
    str url -> indirizzo web del dominio

    Valore di ritorno:
    None
    '''
    try:
        dominio = whois.whois(url)
        print("\nAnalisi WHOIS del dominio:")
        print(f"- Registrar: {dominio.registrar}")
        print(f"- Creato il: {dominio.creation_date}")
        print(f"- Scade il:  {dominio.expiration_date}\n")
    except Exception as e:
        print(f"Errore durante l'analisi WHOIS: {e}\n")

# ------------------------------------------------------------
# ///// SEZIONE WAYBACK
def costruisciTimestamp(anno: str, mese: str, giorno: str) -> str:
    '''
    ///// Funzione: costruisciTimestamp
    Converte anno, mese e giorno in un formato timestamp compatibile
    con l’API Wayback Machine (es. 2020 + 01 + 01 -> "20200101").

    Parametri formali:
    str anno, mese, giorno

    Valore di ritorno:
    str -> timestamp (formato AAAAMMGG)
    '''
    if mese == "":
        mese = "01"
    if giorno == "":
        giorno = "01"
    return f"{anno}{mese.zfill(2)}{giorno.zfill(2)}"

def ottieniSnapshotDisponibili(url: str, timestamp: str) -> list:
    '''
    ///// Funzione: ottieniSnapshotDisponibili
    Interroga l’API Wayback Machine per ottenere le versioni archiviate
    più vicine al timestamp indicato.

    Parametri formali:
    str url -> indirizzo web originale
    str timestamp -> data di riferimento in formato AAAAMMGG

    Valore di ritorno:
    list -> elenco di snapshot trovate
    '''
    # Placeholder: implementeremo nella prossima fase
    return []

def mostraSnapshot(snapshot_list: list) -> str:
    '''
    ///// Funzione: mostraSnapshot
    Mostra un elenco numerato di snapshot disponibili
    e permette all’utente di selezionarne una da aprire.

    Parametri formali:
    list snapshot_list -> lista di link alle versioni archiviate

    Valore di ritorno:
    str -> link scelto dall’utente
    '''
    # Placeholder
    return None

def apriSnapshot(link: str) -> None:
    '''
    ///// Funzione: apriSnapshot
    Apre nel browser predefinito del sistema
    la versione archiviata selezionata dall’utente.

    Parametri formali:
    str link -> URL della versione archiviata
    '''
    if link:
        webbrowser.open(link)
    else:
        print("Nessuna versione disponibile da aprire.")

# ------------------------------------------------------------
# ///// SEZIONE SALVATAGGIO
def salvaCSV(url: str, anno: str, data_snap: str, link: str) -> None:
    '''
    ///// Funzione: salvaCSV
    Registra i dettagli della ricerca in un file CSV strutturato.

    Parametri formali:
    str url -> indirizzo analizzato
    str anno -> anno richiesto
    str data_snap -> data della versione archiviata
    str link -> link Wayback Machine

    Valore di ritorno:
    None
    '''
    with open("ricerche.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([url, anno, data_snap, link])

# ------------------------------------------------------------
# ///// PROGRAMMA PRINCIPALE
def main():
    '''
    ///// Programma principale
    Descrizione sintetica:
    L'applicazione chiede all’utente l’URL e la data,
    mostra i dati WHOIS del dominio, cerca le versioni archiviate
    e consente di aprirle nel browser, salvando la ricerca in CSV.
    '''
    # Input
    dati = richiediInput()
    url, anno, mese, giorno = dati["url"], dati["anno"], dati["mese"], dati["giorno"]

    # Analisi WHOIS
    analizzaDominio(url)

    # Timestamp e ricerca snapshot
    timestamp = costruisciTimestamp(anno, mese, giorno)
    snapshot_list = ottieniSnapshotDisponibili(url, timestamp)

    # Visualizzazione e selezione
    link_scelto = mostraSnapshot(snapshot_list)

    # Apertura e salvataggio
    if link_scelto:
        apriSnapshot(link_scelto)
        salvaCSV(url, anno, datetime.now().strftime("%Y-%m-%d"), link_scelto)
    else:
        print("Nessuna versione trovata o selezionata.")

# ------------------------------------------------------------
if __name__ == "__main__":
    main()
'''
Autore: Iglis Gjoni
Data: 12/11/2025

Titolo: TimeBrowser 2.0 – Analizzatore storico e anagrafico dei siti web
'''

# ///// SEZIONE IMPORT LIBRERIE
import requests
import json
import webbrowser
import csv
import whois
from datetime import datetime

# ------------------------------------------------------------
# ///// SEZIONE INPUT
def richiediInput() -> dict:
    '''
    ///// Funzione: richiediInput
    Richiede all’utente l’URL del sito da analizzare e la data di riferimento.
    L’utente può specificare anno, mese e giorno (questi ultimi opzionali).

    Valore di ritorno:
    dict -> dizionario con le chiavi 'url', 'anno', 'mese', 'giorno'
    '''
    url = input("Inserisci l'URL del sito (es. https://www.example.com): ").strip()
    anno = input("Inserisci l'anno (es. 2020): ").strip()
    mese = input("Inserisci il mese [opzionale, 01-12]: ").strip()
    giorno = input("Inserisci il giorno [opzionale, 01-31]: ").strip()

    return {"url": url, "anno": anno, "mese": mese, "giorno": giorno}

# ------------------------------------------------------------
# ///// SEZIONE WHOIS
def analizzaDominio(url: str) -> None:
    '''
    ///// Funzione: analizzaDominio
    Analizza il dominio utilizzando la libreria python-whois e
    mostra informazioni anagrafiche di base (registrar, creazione, scadenza).

    Parametri formali:
    str url -> indirizzo web del dominio

    Valore di ritorno:
    None
    '''
    try:
        dominio = whois.whois(url)
        print("\nAnalisi WHOIS del dominio:")
        print(f"- Registrar: {dominio.registrar}")
        print(f"- Creato il: {dominio.creation_date}")
        print(f"- Scade il:  {dominio.expiration_date}\n")
    except Exception as e:
        print(f"Errore durante l'analisi WHOIS: {e}\n")

# ------------------------------------------------------------
# ///// SEZIONE WAYBACK
def costruisciTimestamp(anno: str, mese: str, giorno: str) -> str:
    '''
    ///// Funzione: costruisciTimestamp
    Converte anno, mese e giorno in un formato timestamp compatibile
    con l’API Wayback Machine (es. 2020 + 01 + 01 -> "20200101").

    Parametri formali:
    str anno, mese, giorno

    Valore di ritorno:
    str -> timestamp (formato AAAAMMGG)
    '''
    if mese == "":
        mese = "01"
    if giorno == "":
        giorno = "01"
    return f"{anno}{mese.zfill(2)}{giorno.zfill(2)}"

def ottieniSnapshotDisponibili(url: str, timestamp: str) -> list:
    '''
    ///// Funzione: ottieniSnapshotDisponibili
    Interroga l’API Wayback Machine per ottenere le versioni archiviate
    più vicine al timestamp indicato.

    Parametri formali:
    str url -> indirizzo web originale
    str timestamp -> data di riferimento in formato AAAAMMGG

    Valore di ritorno:
    list -> elenco di snapshot trovate
    '''
    # Placeholder: implementeremo nella prossima fase
    return []

def mostraSnapshot(snapshot_list: list) -> str:
    '''
    ///// Funzione: mostraSnapshot
    Mostra un elenco numerato di snapshot disponibili
    e permette all’utente di selezionarne una da aprire.

    Parametri formali:
    list snapshot_list -> lista di link alle versioni archiviate

    Valore di ritorno:
    str -> link scelto dall’utente
    '''
    # Placeholder
    return None

def apriSnapshot(link: str) -> None:
    '''
    ///// Funzione: apriSnapshot
    Apre nel browser predefinito del sistema
    la versione archiviata selezionata dall’utente.

    Parametri formali:
    str link -> URL della versione archiviata
    '''
    if link:
        webbrowser.open(link)
    else:
        print("Nessuna versione disponibile da aprire.")

# ------------------------------------------------------------
# ///// SEZIONE SALVATAGGIO
def salvaCSV(url: str, anno: str, data_snap: str, link: str) -> None:
    '''
    ///// Funzione: salvaCSV
    Registra i dettagli della ricerca in un file CSV strutturato.

    Parametri formali:
    str url -> indirizzo analizzato
    str anno -> anno richiesto
    str data_snap -> data della versione archiviata
    str link -> link Wayback Machine

    Valore di ritorno:
    None
    '''
    with open("ricerche.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([url, anno, data_snap, link])

# ------------------------------------------------------------
# ///// PROGRAMMA PRINCIPALE
def main():
    '''
    ///// Programma principale
    Descrizione sintetica:
    L'applicazione chiede all’utente l’URL e la data,
    mostra i dati WHOIS del dominio, cerca le versioni archiviate
    e consente di aprirle nel browser, salvando la ricerca in CSV.
    '''
    # Input
    dati = richiediInput()
    url, anno, mese, giorno = dati["url"], dati["anno"], dati["mese"], dati["giorno"]

    # Analisi WHOIS
    analizzaDominio(url)

    # Timestamp e ricerca snapshot
    timestamp = costruisciTimestamp(anno, mese, giorno)
    snapshot_list = ottieniSnapshotDisponibili(url, timestamp)

    # Visualizzazione e selezione
    link_scelto = mostraSnapshot(snapshot_list)

    # Apertura e salvataggio
    if link_scelto:
        apriSnapshot(link_scelto)
        salvaCSV(url, anno, datetime.now().strftime("%Y-%m-%d"), link_scelto)
    else:
        print("Nessuna versione trovata o selezionata.")

# ------------------------------------------------------------
if __name__ == "__main__":
    main()
