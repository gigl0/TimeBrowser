import requests
import webbrowser
import json
import time

def cerca_snapshot(url, anno):
    """
    Interroga l'API. Se il server è in manutenzione, restituisce dati simulati
    per permettere di testare l'applicazione.
    """
    api_url = "http://web.archive.org/cdx/search/cdx"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
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

    print(f"[*] Cercando snapshot per {url} ({anno})...")

    try:
        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        
        # Controllo specifico per Manutenzione
        if "Maintenance" in response.text or response.status_code >= 500:
            print("⚠️ ATTENZIONE: Wayback Machine è in MANUTENZIONE.")
            return genera_dati_finti(url, anno)

        data = response.json() # Se fallisce qui, va nell'except

        if not data or len(data) <= 1:
            return []

        risultati_puliti = []
        for riga in data[1:]:
            timestamp = riga[0]
            url_orig = riga[1]
            link_wayback = f"https://web.archive.org/web/{timestamp}/{url_orig}"
            
            # Formattazione veloce data
            data_leggibile = f"{timestamp[6:8]}/{timestamp[4:6]}/{timestamp[:4]} - {timestamp[8:10]}:{timestamp[10:12]}"
            
            risultati_puliti.append({
                'data': data_leggibile,
                'link': link_wayback,
                'timestamp': timestamp
            })
        
        return risultati_puliti

    except (json.JSONDecodeError, requests.exceptions.RequestException) as e:
        print(f"[!] Errore connessione/API ({e}). Attivo modalità DEMO.")
        return genera_dati_finti(url, anno)

def genera_dati_finti(url, anno):
    """Genera dati simulati per testare la GUI quando Internet Archive è giù."""
    print(f"[*] Generazione dati simulati per {url}...")
    # Simuliamo un piccolo ritardo per realismo
    time.sleep(1)
    
    return [
        {
            'data': f'01/01/{anno} - 10:00 (SIMULATO)',
            'link': f'https://web.archive.org/web/{anno}0101000000/{url}',
            'timestamp': f'{anno}0101000000'
        },
        {
            'data': f'15/08/{anno} - 14:30 (SIMULATO)',
            'link': f'https://web.archive.org/web/{anno}0815000000/{url}',
            'timestamp': f'{anno}0815000000'
        },
        {
            'data': f'31/12/{anno} - 23:59 (SIMULATO)',
            'link': f'https://web.archive.org/web/{anno}1231235959/{url}',
            'timestamp': f'{anno}1231235959'
        }
    ]

def apri_browser(url):
    print(f"[*] Apertura browser: {url}")
    webbrowser.open(url)