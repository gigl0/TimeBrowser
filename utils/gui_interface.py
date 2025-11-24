import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import ttkbootstrap as ttk  
# from ttkbootstrap.constants import
import csv
from datetime import datetime

# Importiamo le nostre funzioni logiche
from utils.whois_handler import ottieni_info_dominio
from utils.wayback_handler import cerca_snapshot, apri_browser
from utils.db_handler import salva_ricerca, leggi_cronologia

class TimeBrowserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TimeBrowser - Analizzatore Web Storico")
        self.root.geometry("750x650")

        # --- MENU BAR (Per Export CSV) ---
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Esporta Cronologia in CSV", command=self.esporta_csv)
        filemenu.add_separator()
        filemenu.add_command(label="Esci", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)

        # --- SEZIONE INPUT ---
        frame_input = tk.Frame(root, padx=10, pady=10)
        frame_input.pack(fill="x")

        tk.Label(frame_input, text="URL Sito (es. google.com):").grid(row=0, column=0, sticky="w")
        self.entry_url = tk.Entry(frame_input, width=30)
        self.entry_url.grid(row=0, column=1, padx=5)

        tk.Label(frame_input, text="Anno:").grid(row=0, column=2, sticky="w")
        self.entry_anno = tk.Entry(frame_input, width=8)
        self.entry_anno.grid(row=0, column=3, padx=5)
        self.entry_anno.insert(0, str(datetime.now().year - 1)) 

        # Bottone Cerca
        self.btn_cerca = tk.Button(frame_input, text="Avvia Analisi", command=self.fai_ricerca, bg="#dddddd")
        self.btn_cerca.grid(row=0, column=4, padx=5)

        # Bottone Cronologia (Database Reader)
        self.btn_history = tk.Button(frame_input, text="Mostra Cronologia", command=self.mostra_cronologia, bg="#add8e6")
        self.btn_history.grid(row=0, column=5, padx=5)

        # --- SEZIONE RISULTATI WHOIS ---
        tk.Label(root, text="Dati Anagrafici (WHOIS):", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10,0))
        self.text_whois = scrolledtext.ScrolledText(root, height=8, width=90)
        self.text_whois.pack(padx=10, pady=5)

        # --- SEZIONE SNAPSHOT ---
        tk.Label(root, text="Snapshot Trovati (Doppio click per aprire):", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10,0))
        
        self.list_snapshot = tk.Listbox(root, height=12, width=100)
        self.list_snapshot.pack(padx=10, pady=5)
        self.list_snapshot.bind('<Double-1>', self.apri_selezione)

        self.risultati_correnti = []

        # --- BARRA DI STATO ---
        self.lbl_status = tk.Label(root, text="Pronto.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

    def fai_ricerca(self):
        """Esegue la logica principale: Whois + Wayback + DB"""
        url = self.entry_url.get().strip()
        anno = self.entry_anno.get().strip()

        if not url or not anno:
            messagebox.showwarning("Attenzione", "Inserisci sia URL che Anno.")
            return

        self.lbl_status.config(text="Elaborazione in corso...")
        self.root.update()

        # 1. WHOIS
        self.text_whois.delete(1.0, tk.END)
        self.text_whois.insert(tk.END, "Caricamento WHOIS...\n")
        info_whois = ottieni_info_dominio(url)
        self.text_whois.delete(1.0, tk.END)
        self.text_whois.insert(tk.END, info_whois)

        # 2. WAYBACK
        self.list_snapshot.delete(0, tk.END)
        self.risultati_correnti = cerca_snapshot(url, anno)

        esito_db = "Nessun risultato"

        if self.risultati_correnti:
            esito_db = f"{len(self.risultati_correnti)} snapshot trovati"
            for idx, res in enumerate(self.risultati_correnti):
                self.list_snapshot.insert(tk.END, f"{idx+1}. {res['data']} (Clicca per aprire)")
            self.lbl_status.config(text=f"Trovati {len(self.risultati_correnti)} snapshot.")
        else:
            self.list_snapshot.insert(tk.END, "Nessuno snapshot trovato (o modalità demo attiva).")
            self.lbl_status.config(text="Nessun risultato.")

        # 3. SALVATAGGIO DB
        salva_ricerca(url, anno, esito_db)

    def apri_selezione(self, event):
        """Apre il link al doppio click"""
        selection = self.list_snapshot.curselection()
        if selection:
            index = selection[0]
            if index < len(self.risultati_correnti):
                snapshot = self.risultati_correnti[index]
                apri_browser(snapshot['link'])

    def mostra_cronologia(self):
        """Apre una finestra popup per leggere il DB"""
        top = tk.Toplevel(self.root)
        top.title("Cronologia Ricerche (da Database)")
        top.geometry("650x400")

        columns = ('id', 'url', 'data_req', 'esito', 'timestamp')
        tree = ttk.Treeview(top, columns=columns, show='headings')

        tree.heading('id', text='ID')
        tree.heading('url', text='URL Originale')
        tree.heading('data_req', text='Anno Richiesto')
        tree.heading('esito', text='Risultato')
        tree.heading('timestamp', text='Data Ricerca')

        tree.column('id', width=30)
        tree.column('url', width=150)
        tree.column('data_req', width=80)
        tree.column('esito', width=150)
        tree.column('timestamp', width=150)

        tree.pack(fill=tk.BOTH, expand=True)

        # Legge dal DB
        dati = leggi_cronologia()
        for riga in dati:
            # riga è una tupla (id, url, data_req, snapshot_trovato, timestamp)
            tree.insert('', tk.END, values=riga)

    def esporta_csv(self):
        """Esporta il contenuto del DB in CSV"""
        dati = leggi_cronologia()
        filename = "cronologia_ricerche.csv"
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "URL", "Anno Richiesto", "Esito", "Data Esecuzione"])
                writer.writerows(dati)
            messagebox.showinfo("Export Completato", f"File salvato come: {filename}")
        except Exception as e:
            messagebox.showerror("Errore Export", f"Impossibile salvare il file: {e}")