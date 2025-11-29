import sys
import ttkbootstrap as ttk
from utils.db_handler import init_db
from utils.gui_interface import TimeBrowserApp
from utils.cui_interface import start_cui

if __name__ == "__main__":
    # Creiamo la tabella nel database se non esiste
    init_db()

    # Controlliamo se l'utente vuole la modalità testuale
    # Esempio: python timebrowser.py --cui
    if len(sys.argv) > 1 and sys.argv[1] == "--cui":
        start_cui()
    else:
        # Avvia la modalità grafica
        # Il tema "superhero" è scuro e moderno
        root = ttk.Window(themename="superhero")
        app = TimeBrowserApp(root)
        root.mainloop()