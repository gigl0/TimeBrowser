import tkinter as tk
from tkinter import messagebox, scrolledtext
from utils.whois_handler import ottieni_info_dominio
from utils.wayback_handler import cerca_snapshot, apri_browser
from utils.db_handler import salva_ricerca
from datetime import datetime

class TimeBrowserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TimeBrowser - Analizzatore Web Storico")
        self.root.geometry("700x600")

        # --- SEZIONE INPUT ---
        frame_input = tk.Frame(root, padx=10, pady=10)
        frame_input.pack(fill="x")

        tk.Label(frame_input, text="URL Sito (es. google.com):").grid(row=0, column=0, sticky="w")
        self.entry_url = tk.Entry(frame_input, width=40)
        self.entry_url.grid(row=0, column=1, padx=5)

        tk.Label(frame_input, text="Anno (es. 2015):").grid(row=0, column=2, sticky="w")
        self.entry_anno = tk.Entry(frame_input, width=10)
        self.entry_anno.grid(row=0, column=3, padx=5)
        self.entry_anno.insert(0, str(datetime.now().year - 1)) # Default anno scorso

        self.btn_cerca = tk.Button(frame_input, text="Avvia Analisi", command=self.fai_ricerca, bg="#dddddd")
        self.btn_cerca.grid(row=0, column=4, padx=10)

        # --- SEZIONE RISULTATI WHOIS ---
        tk.Label(root, text="Dati Anagrafici (WHOIS):", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10,0))
        self.text_whois = scrolledtext.ScrolledText(root, height=6, width=80)
        self.text_whois.pack(padx=10, pady=5)

        # --- SEZIONE SNAPSHOT ---
        tk.Label(root, text="Snapshot Trovati (Doppio click per aprire):", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10,0))
        
        # Listbox per mostrare i risultati cliccabili
        self.list_snapshot = tk.Listbox(root, height=10, width=90)
        self.list_snapshot.pack(padx=10, pady=5)
        self.list_snapshot.bind('<Double-1>', self.apri_selezione) # Evento doppio click

        # Variabile per tenere in memoria i link trovati
        self.risultati_correnti = []

        # --- BARRA DI STATO ---
        self.lbl_status = tk.Label(root, text="Pronto.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

    def fai_ricerca(self):
        url = self.entry_url.get().strip()
        anno = self.entry_anno.get().strip()

        if not url or not anno:
            messagebox.showwarning("Attenzione", "Inserisci sia URL che Anno.")
            return

        self.lbl_status.config(text="Elaborazione in corso...")
        self.root.update() # Forza aggiornamento GUI

        # 1. Esegui WHOIS
        self.text_whois.delete(1.0, tk.END)
        self.text_whois.insert(tk.END, "Caricamento WHOIS...\n")
        
        info_whois = ottieni_info_dominio(url)
        self.text_whois.delete(1.0, tk.END)
        self.text_whois.insert(tk.END, info_whois)

        # 2. Cerca Snapshot Wayback
        self.list_snapshot.delete(0, tk.END)
        self.risultati_correnti = cerca_snapshot(url, anno)

        if self.risultati_correnti:
            for idx, res in enumerate(self.risultati_correnti):
                self.list_snapshot.insert(tk.END, f"{idx+1}. Data: {res['data']} - Clicca per aprire")
            
            self.lbl_status.config(text=f"Trovati {len(self.risultati_correnti)} snapshot.")
            
            # 3. Salva nel DB il primo risultato trovato come riferimento (o l'azione di ricerca)
            salva_ricerca(url, anno, f"{len(self.risultati_correnti)} snapshot trovati")
            
        else:
            self.list_snapshot.insert(tk.END, "Nessuno snapshot trovato per questo anno.")
            self.lbl_status.config(text="Nessun risultato.")

    def apri_selezione(self, event):
        """Gestisce il click sulla lista per aprire il browser"""
        selection = self.list_snapshot.curselection()
        if selection:
            index = selection[0]
            if index < len(self.risultati_correnti):
                snapshot = self.risultati_correnti[index]
                url_target = snapshot['link']
                apri_browser(url_target)
                self.lbl_status.config(text=f"Aperto: {snapshot['data']}")