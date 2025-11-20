import tkinter as tk
from utils.gui_interface import TimeBrowserApp
from utils.db_handler import init_db

if __name__ == "__main__":
    # 1. Inizializza il database
    init_db()
    
    # 2. Avvia la GUI  
    root = tk.Tk()
    app = TimeBrowserApp(root)
    root.mainloop()