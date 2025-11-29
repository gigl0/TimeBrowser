import requests
import webbrowser
import json
import time
from typing import List, Dict, Any

def cerca_snapshot(url: str, anno: str) -> List[Dict[str, str]]:
    """
    Interroga l'API CDX di Wayback Machine per trovare snapshot storici.

    Args:
        url (str): Il sito web da cercare.
        anno (str): L'anno di interesse (YYYY).

    Returns:
        List[Dict[str, str]]: Una lista di dizionari, dove ogni dizionario
        contiene la 'data' formattata e il 'link' allo snapshot.
        Restituisce una lista vuota se non trova nulla.
    """
    api_url = "http://web.archive.org/cdx/search/cdx"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
    }

    params = {
        'url': url,
        'output': 'json',
        'from': f"{anno}0101",
        'to': f"{anno}1231",
        'limit': 50,
        'collapse': 'digest',
        'fl': 'timestamp,original'
    }
    
    print(f"[*] Cerco su Wayback Machine: {url} ({anno})...")

    try:
        response = requests.get(api_url, params=params, headers=headers, timeout=5)
        
        if response.status_code >= 500 or "Maintenance" in response.text:
            return dati_finti(url, anno)

        data = response.json()

        if not data or len(data) <= 1:
            return []

        risultati = []
        for riga in data[1:]:
            ts = riga[0] # timestamp
            orig = riga[1] # url originale
            
            link = f"https://web.archive.org/web/{ts}/{orig}"
            data_fmt = f"{ts[6:8]}/{ts[4:6]}/{ts[:4]} - {ts[8:10]}:{ts[10:12]}"
            
            risultati.append({
                'data': data_fmt,
                'link': link
            })
        
        return risultati

    except Exception as e:
        print(f"[!] Errore API: {e}. Uso dati simulati.")
        return dati_finti(url, anno)

def dati_finti(url: str, anno: str) -> List[Dict[str, str]]:
    """
    Genera dati simulati (mock) in caso di errore di rete o manutenzione API.
    
    Returns:
        List[Dict[str, str]]: Lista di snapshot fittizi.
    """
    time.sleep(1)
    return [
        {'data': f'01/01/{anno} (SIMULATO)', 'link': f'https://google.com'},
        {'data': f'15/06/{anno} (SIMULATO)', 'link': f'https://google.com'},
        {'data': f'31/12/{anno} (SIMULATO)', 'link': f'https://google.com'}
    ]

def apri_browser(url: str) -> None:
    """Apre l'URL specificato nel browser web predefinito del sistema."""
    webbrowser.open(url)