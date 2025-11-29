import sqlite3
from typing import List, Tuple, Any

DB_NAME = "history.db"

def init_db() -> None:
    """
    Inizializza il database SQLite creando la tabella 'ricerche' se non esiste.
    
    La tabella contiene:
    - id: Identificativo univoco (Auto Increment)
    - url_originale: L'URL cercato
    - data_richiesta: L'anno specificato
    - snapshot_trovato: Esito della ricerca
    - timestamp: Data e ora dell'operazione
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ricerche (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_originale TEXT,
            data_richiesta TEXT,
            snapshot_trovato TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def salva_ricerca(url: str, data_req: str, snapshot: str) -> None:
    """
    Salva una nuova entry di ricerca nel database.

    Args:
        url (str): L'URL del sito web analizzato.
        data_req (str): L'anno richiesto per la ricerca.
        snapshot (str): Il risultato dell'operazione (es. "5 snapshot trovati").
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO ricerche (url_originale, data_richiesta, snapshot_trovato)
        VALUES (?, ?, ?)
    ''', (url, data_req, snapshot))
    
    conn.commit()
    conn.close()

def leggi_cronologia() -> List[Tuple[Any, ...]]:
    """
    Recupera le ultime 50 ricerche effettuate dal database.

    Returns:
        List[Tuple[Any, ...]]: Una lista di tuple contenenti i dati delle righe
        (id, url, anno, esito, timestamp), ordinate dalla più recente.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, url_originale, data_richiesta, snapshot_trovato, timestamp FROM ricerche ORDER BY id DESC LIMIT 50')
    
    dati = cursor.fetchall()
    conn.close()
    return dati