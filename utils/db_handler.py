import sqlite3

DB_NAME = "history.db"

def init_db():
    """Crea la tabella se non esiste"""
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

def salva_ricerca(url, data_req, snapshot):
    """Salva una nuova ricerca nel DB"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ricerche (url_originale, data_richiesta, snapshot_trovato)
        VALUES (?, ?, ?)
    ''', (url, data_req, snapshot))
    conn.commit()
    conn.close()

def leggi_cronologia():
    """Recupera le ultime 50 ricerche dal DB"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Recuperiamo dati ordinati per data decrescente
    cursor.execute('SELECT url_originale, data_richiesta, snapshot_trovato, timestamp FROM ricerche ORDER BY id DESC LIMIT 50')
    dati = cursor.fetchall()
    conn.close()
    return dati