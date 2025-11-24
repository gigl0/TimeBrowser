import sys
from utils.whois_handler import ottieni_info_dominio
from utils.wayback_handler import cerca_snapshot, apri_browser
from utils.db_handler import salva_ricerca

# Codici colori ANSI per il terminale (funzionano su Linux)
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def start_cui():
    """
    Avvia l'interfaccia a caratteri (CUI/CLI).
    """
    print(f"{BOLD}{BLUE}\n==============================================")
    print(f"   TIMEBROWSER - CUI MODE (Terminale)")
    print(f"=============================================={RESET}\n")

    while True:
        try:
            # 1. INPUT
            print(f"{YELLOW}--- NUOVA RICERCA ---{RESET}")
            url = input("Inserisci URL (o 'q' per uscire): ").strip()
            
            if url.lower() in ['q', 'quit', 'exit']:
                print("Uscita in corso...")
                break
            
            if not url:
                continue

            anno = input("Inserisci Anno (es. 2015): ").strip()
            if not anno:
                anno = "2024" # Default

            print(f"\n{BLUE}[*] Analisi in corso per {url} ({anno})...{RESET}")

            # 2. WHOIS
            print(f"\n{BOLD}1. DATI ANAGRAFICI (WHOIS):{RESET}")
            try:
                info = ottieni_info_dominio(url)
                print(info)
            except Exception as e:
                print(f"{RED}Errore Whois: {e}{RESET}")

            # 3. WAYBACK
            print(f"{BOLD}2. SNAPSHOT STORICI:{RESET}")
            snapshots = cerca_snapshot(url, anno)
            
            esito_db = "Nessun risultato"

            if not snapshots:
                print(f"{RED}Nessuno snapshot trovato.{RESET}")
            else:
                esito_db = f"{len(snapshots)} snapshot trovati"
                print(f"{GREEN}Trovati {len(snapshots)} snapshot.{RESET} Ecco i primi 20:")
                
                # Mostra max 20 risultati
                limit = min(20, len(snapshots))
                for i in range(limit):
                    print(f"[{i+1}] {snapshots[i]['data']}")

                # 4. INTERAZIONE (APERTURA LINK)
                choice = input(f"\n{YELLOW}Digita il numero per aprire (o Invio per continuare): {RESET}")
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(snapshots):
                        link = snapshots[idx]['link']
                        print(f"Apertura browser: {link}")
                        apri_browser(link)
                    else:
                        print(f"{RED}Numero non valido.{RESET}")

            # 5. SALVATAGGIO DB
            salva_ricerca(url, anno, esito_db)
            print(f"\n{BLUE}[V] Ricerca salvata nel Database.{RESET}\n")
            print("-" * 50)

        except KeyboardInterrupt:
            print("\nUscita forzata.")
            break
        except Exception as e:
            print(f"{RED}Errore imprevisto: {e}{RESET}")