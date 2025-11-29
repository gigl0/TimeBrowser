import whois
from urllib.parse import urlparse

def ottieni_info_dominio(url: str) -> str:
    """
    Esegue una query WHOIS sul dominio fornito per recuperare dati anagrafici.

    Esegue il parsing dell'URL per estrarre il dominio pulito (netloc)
    e gestisce eventuali formati di dati complessi (liste o date) restituiti
    dalla libreria whois.

    Args:
        url (str): L'indirizzo web completo o parziale (es. "https://google.com").

    Returns:
        str: Una stringa formattata contenente Registrar, Date e Paese,
             oppure un messaggio di errore leggibile.
    """
    try:
        # 1. Pulizia URL: da "https://www.google.com/search" a "google.com"
        if not url.startswith("http"):
            url = "http://" + url
        
        parsed_url = urlparse(url)
        dominio = parsed_url.netloc
        
        # Rimuove 'www.' se presente per evitare problemi con whois
        if dominio.startswith("www."):
            dominio = dominio[4:]

        # 2. Esecuzione Query WHOIS
        w = whois.whois(dominio)

        # 3. Formattazione Risultati
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        expiration_date = w.expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        risultato = (
            f"--- ANALISI WHOIS: {dominio} ---\n"
            f"Registrar: {w.registrar}\n"
            f"Data Creazione: {creation_date}\n"
            f"Data Scadenza: {expiration_date}\n"
            f"Paese: {w.country}\n"
            f"---------------------------------\n"
        )
        return risultato

    except Exception as e:
        return f"Errore WHOIS: Impossibile recuperare dati per questo dominio.\nDettaglio: {e}\n"