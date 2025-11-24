# TimeBrowser 

**TimeBrowser** è un'applicazione Python progettata per l'analisi storica e anagrafica dei domini web.
Il software integra protocolli di rete e API pubbliche per fornire un quadro completo dell'evoluzione di un sito internet, combinando dati tecnici attuali con snapshot visivi del passato.

## Caratteristiche del Progetto

Il progetto è stato sviluppato seguendo un'architettura **modulare** e supporta una doppia interfaccia utente (Ibrida):

### Funzionalità Base (CUI)
*   **Interfaccia a Riga di Comando (CUI):** Modalità testuale completa (con colori ANSI) per l'utilizzo da terminale, conforme ai requisiti core del progetto.
*   **Analisi WHOIS:** Recupero dati anagrafici del dominio (Registrar, Data Creazione, Scadenza).
*   **Wayback Machine API:** Ricerca avanzata tramite API CDX di Internet Archive per recuperare lo storico del sito.
*   **Interattività:** Possibilità di selezionare e aprire gli snapshot storici direttamente nel browser predefinito.

### Funzionalità Avanzate (Bonus)
*   **Interfaccia Grafica Moderna (GUI):** Sviluppata con `tkinter` e `ttkbootstrap` (Tema: *Superhero*), include barre di caricamento e tabelle interattive.
*   **Database SQLite:** Archiviazione persistente delle ricerche in un database relazionale (`history.db`) invece del semplice file CSV.
*   **Visualizzatore Cronologia:** Modulo dedicato per rileggere e analizzare le ricerche passate salvate nel database.
*   **Export Dati:** Funzionalità per esportare lo storico delle ricerche in formato CSV.

### Robustezza e Gestione Errori
*   **Gestione Timeout:** Il sistema intercetta errori di rete e timeout API senza crashare.
*   **Modalità Demo/Fallback:** In caso di manutenzione dei server di Archive.org, il sistema attiva automaticamente una modalità simulata per permettere la valutazione delle funzionalità.

---

## Installazione

### Prerequisiti
*   Sistema Operativo: Linux (Ubuntu/Debian consigliato), Windows o macOS.
*   Python 3.10 o superiore.

### Setup
1.  **Clona la repository:**
    ```bash
    git clone https://github.com/gigl0/TimeBrowser.git
    cd TimeBrowser
    ```

2.  **Crea l'ambiente virtuale:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Su Linux/Mac
    # venv\Scripts\activate   # Su Windows
    ```

3.  **Installa le dipendenze:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Le dipendenze principali includono: `requests`, `python-whois`, `ttkbootstrap`)*.

---

## Utilizzo

Il software supporta due modalità di avvio. Assicurati di avere l'ambiente virtuale attivo.

### 1. Modalità Grafica (GUI) - *Default*
Avvia l'applicazione con interfaccia a finestre:
```bash
python timebrowser.py


