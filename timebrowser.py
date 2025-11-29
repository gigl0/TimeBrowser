"""
Modulo principale (Entry Point) dell'applicazione TimeBrowser.

Questo script si occupa di:
1. Inizializzare il database locale.
2. Analizzare gli argomenti da riga di comando.
3. Avviare l'interfaccia appropriata (GUI o CUI) in base alla richiesta dell'utente.

Utilizzo:
    python timebrowser.py          -> Avvia l'interfaccia Grafica (GUI)
    python timebrowser.py --cui    -> Avvia l'interfaccia Testuale (CUI)
"""

import sys
import ttkbootstrap as ttk
from utils.db_handler import init_db
from utils.gui_interface import TimeBrowserApp
from utils.cui_interface import start_cui

if __name__ == "__main__":
    # Creiamo la tabella nel database se non esiste
    init_db()

    # Controlliamo se l'utente vuole la modalità testuale
    if len(sys.argv) > 1 and sys.argv[1] == "--cui":
        start_cui()
    else:
        # Avvia la modalità grafica
        # Il tema "superhero" è scuro e moderno
        root = ttk.Window(themename="superhero")
        app = TimeBrowserApp(root)
        root.mainloop()