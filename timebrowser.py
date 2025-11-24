import sys
import ttkbootstrap as ttk
from utils.db_handler import init_db

# Importiamo entrambe le interfacce
from utils.gui_interface import TimeBrowserApp
from utils.cui_interface import start_cui

if __name__ == "__main__":
    # Inizializza il database (comune a entrambe le modalità)
    init_db()
    
    # Controlla gli argomenti passati al comando
    # Esempio: python timebrowser.py --cui
    if len(sys.argv) > 1 and sys.argv[1] == "--cui":
        # Avvia Modalità Testuale (Requisito Base 26 pt)
        start_cui()
    else:
        # Avvia Modalità Grafica (Requisito Bonus +2 pt)
        root = ttk.Window(themename="superhero")
        app = TimeBrowserApp(root)
        root.mainloop()