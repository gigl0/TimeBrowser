import tkinter as tk
from tkinter import messagebox

class TimeBrowserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TimeBrowser - GUI Edition")
        self.root.geometry("600x400")
        
        # Esempio di Label
        self.label = tk.Label(root, text="Inserisci URL:", font=("Arial", 12))
        self.label.pack(pady=10)
        
        # Esempio Input
        self.entry_url = tk.Entry(root, width=50)
        self.entry_url.pack(pady=5)
        
        # Esempio Bottone
        self.btn = tk.Button(root, text="Cerca Snapshot", command=self.fai_ricerca)
        self.btn.pack(pady=20)

    def fai_ricerca(self):
        url = self.entry_url.get()
        messagebox.showinfo("Info", f"Cercherò snapshot per: {url}") 