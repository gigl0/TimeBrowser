import tkinter as tk
from tkinter import messagebox, scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
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
        self.root.geometry("850x750")
        
        # --- MENU BAR (Standard TK per compatibilità) ---
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Esporta Cronologia in CSV", command=self.esporta_csv)
        filemenu.add_separator()
        filemenu.add_command(label="Esci", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)

        # Container principale con padding
        main_container = ttk.Frame(root, padding=10)
        main_container.pack(fill=BOTH, expand=YES)

        # --- SEZIONE 1: INPUT (Raggruppata in Labelframe) ---
        # CORREZIONE QUI: Labelframe con la 'f' minuscola
        input_group = ttk.Labelframe(main_container, text=" Parametri di Ricerca ", padding=15)
        input_group.pack(fill=X, pady=(0, 10))

        # Grid Layout per input
        ttk.Label(input_group, text="URL Target:").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.entry_url = ttk.Entry(input_group, width=35)
        self.entry_url.grid(row=0, column=1, padx=5)
        self.entry_url.insert(0, "google.com") # Placeholder comodo

        ttk.Label(input_group, text="Anno:").grid(row=0, column=2, sticky="w", padx=(10, 5))
        self.entry_anno = ttk.Entry(input_group, width=10)
        self.entry_anno.grid(row=0, column=3, padx=5)
        self.entry_anno.insert(0, str(datetime.now().year - 10)) 

        # Bottone Cerca
        self.btn_cerca = ttk.Button(input_group, text="🔍 Avvia Analisi", command=self.fai_ricerca, bootstyle=PRIMARY)
        self.btn_cerca.grid(row=0, column=4, padx=15)

        # Bottone Cronologia
        self.btn_history = ttk.Button(input_group, text="📂 Cronologia", command=self.mostra_cronologia, bootstyle="info-outline")
        self.btn_history.grid(row=0, column=5, padx=5)

        # --- PROGRESS BAR (Nascosta inizialmente) ---
        self.progress = ttk.Progressbar(self.root, mode='indeterminate', bootstyle=SUCCESS)

        # --- SEZIONE 2: RISULTATI (Split in due parti) ---
        results_container = ttk.Frame(main_container)
        results_container.pack(fill=BOTH, expand=YES)

        # Sinistra: WHOIS
        # CORREZIONE QUI: Labelframe con la 'f' minuscola
        whois_frame = ttk.Labelframe(results_container, text=" Dati Anagrafici (WHOIS) ", padding=10)
        whois_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 5))
        
        self.text_whois = scrolledtext.ScrolledText(whois_frame, height=15, width=40, font=("Consolas", 9))
        self.text_whois.pack(fill=BOTH, expand=YES)

        # Destra: SNAPSHOT
        # CORREZIONE QUI: Labelframe con la 'f' minuscola
        wayback_frame = ttk.Labelframe(results_container, text=" Snapshot Storici ", padding=10)
        wayback_frame.pack(side=RIGHT, fill=BOTH, expand=YES, padx=(5, 0))

        # Listbox con Scrollbar
        list_scroll = ttk.Scrollbar(wayback_frame, bootstyle="round")
        list_scroll.pack(side=RIGHT, fill=Y)
        
        self.list_snapshot = tk.Listbox(wayback_frame, height=15, width=40, font=("Arial", 10), yscrollcommand=list_scroll.set)
        self.list_snapshot.pack(side=LEFT, fill=BOTH, expand=YES)
        self.list_snapshot.bind('<Double-1>', self.apri_selezione)
        
        list_scroll.config(command=self.list_snapshot.yview)

        self.risultati_correnti = []

        # --- BARRA DI STATO ---
        self.lbl_status = ttk.Label(root, text="Pronto.", bootstyle=INVERSE, padding=5)
        self.lbl_status.pack(side=BOTTOM, fill=X)

    def fai_ricerca(self):
        """Logica di ricerca con gestione UI"""
        url = self.entry_url.get().strip()
        anno = self.entry_anno.get().strip()

        if not url or not anno:
            messagebox.showwarning("Dati Mancanti", "Inserisci sia URL che Anno.")
            return

        self.lbl_status.config(text=f"Analisi in corso per {url} ({anno})...")
        self.progress.pack(fill=X, pady=5, before=self.lbl_status)
        self.progress.start(15)
        self.root.update()

        try:
            # 1. WHOIS
            self.text_whois.delete(1.0, tk.END)
            self.text_whois.insert(tk.END, "⏳ Interrogazione database registrar in corso...\n")
            self.root.update()
            
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
                    self.list_snapshot.insert(tk.END, f"{res['data']}")
                self.lbl_status.config(text=f"✅ Completato: {len(self.risultati_correnti)} snapshot trovati.")
            else:
                self.list_snapshot.insert(tk.END, "Nessuno snapshot disponibile.")
                self.lbl_status.config(text="⚠️ Nessun risultato trovato.")

            # 3. SALVATAGGIO
            salva_ricerca(url, anno, esito_db)

        except Exception as e:
            self.lbl_status.config(text="❌ Errore critico.")
            messagebox.showerror("Errore", f"Si è verificato un problema:\n{e}")

        finally:
            self.progress.stop()
            self.progress.pack_forget()

    def apri_selezione(self, event):
        selection = self.list_snapshot.curselection()
        if selection:
            index = selection[0]
            if index < len(self.risultati_correnti):
                snapshot = self.risultati_correnti[index]
                self.lbl_status.config(text=f"Apertura browser: {snapshot['data']}")
                apri_browser(snapshot['link'])

    def mostra_cronologia(self):
        top = ttk.Toplevel(self.root)
        top.title("Cronologia Ricerche")
        top.geometry("700x400")

        columns = ('id', 'url', 'anno', 'esito', 'data')
        tree = ttk.Treeview(top, columns=columns, show='headings', bootstyle=INFO)

        tree.heading('id', text='ID')
        tree.heading('url', text='URL')
        tree.heading('anno', text='Anno Rif.')
        tree.heading('esito', text='Risultato')
        tree.heading('data', text='Data Esecuzione')

        tree.column('id', width=40)
        tree.column('url', width=150)
        tree.column('anno', width=80)
        tree.column('esito', width=200)
        tree.column('data', width=150)

        scroll = ttk.Scrollbar(top, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        
        scroll.pack(side=RIGHT, fill=Y)
        tree.pack(fill=BOTH, expand=YES)

        dati = leggi_cronologia()
        for riga in dati:
            tree.insert('', tk.END, values=riga)

    def esporta_csv(self):
        dati = leggi_cronologia()
        filename = f"export_timebrowser_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "URL", "Anno Target", "Esito", "Timestamp"])
                writer.writerows(dati)
            messagebox.showinfo("Export Riuscito", f"File salvato nella cartella del progetto:\n{filename}")
        except Exception as e:
            messagebox.showerror("Errore Export", f"Impossibile salvare il file: {e}")