import tkinter as tk
from tkinter import messagebox, scrolledtext
import ttkbootstrap as ttk
from datetime import datetime

# Importiamo le nostre funzioni
from utils.whois_handler import ottieni_info_dominio
from utils.wayback_handler import cerca_snapshot, apri_browser
from utils.db_handler import salva_ricerca, leggi_cronologia
from utils.csv_handler import accoda_su_csv

class TimeBrowserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TimeBrowser - Analisi Siti Web")
        self.root.geometry("850x750")
        
        # --- MENU IN ALTO ---
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Esporta CSV", command=self.esporta_csv)
        filemenu.add_separator()
        filemenu.add_command(label="Esci", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)

        # --- CONTENITORE PRINCIPALE ---
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill="both", expand=True)

        # --- SEZIONE 1: INPUT ---
        # Labelframe raggruppa gli input
        input_box = ttk.Labelframe(main_frame, text=" Ricerca ", padding=15)
        input_box.pack(fill="x", pady=(0, 10))

        ttk.Label(input_box, text="Sito Web:").grid(row=0, column=0, padx=5)
        self.entry_url = ttk.Entry(input_box, width=30)
        self.entry_url.grid(row=0, column=1, padx=5)
        self.entry_url.insert(0, "google.com")

        ttk.Label(input_box, text="Anno:").grid(row=0, column=2, padx=5)
        self.entry_anno = ttk.Entry(input_box, width=10)
        self.entry_anno.grid(row=0, column=3, padx=5)
        self.entry_anno.insert(0, "2015")

        # Bottoni (Primary = Blu, Info = Azzurro)
        btn_cerca = ttk.Button(input_box, text="Cerca", command=self.avvia_ricerca, bootstyle="primary")
        btn_cerca.grid(row=0, column=4, padx=15)

        btn_storia = ttk.Button(input_box, text="Cronologia", command=self.apri_cronologia, bootstyle="info-outline")
        btn_storia.grid(row=0, column=5, padx=5)

        # --- BARRA STATO E CARICAMENTO ---
        self.lbl_status = ttk.Label(root, text="Pronto.", bootstyle="inverse", padding=5)
        self.lbl_status.pack(side="bottom", fill="x")

        # Barra di caricamento (inizialmente nascosta)
        self.progress = ttk.Progressbar(root, mode='indeterminate', bootstyle="success")

        # --- SEZIONE 2: RISULTATI ---
        result_box = ttk.Frame(main_frame)
        result_box.pack(fill="both", expand=True)

        # Sinistra: WHOIS
        left_frame = ttk.Labelframe(result_box, text=" Dati Whois ", padding=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        self.text_whois = scrolledtext.ScrolledText(left_frame, height=15, width=40)
        self.text_whois.pack(fill="both", expand=True)

        # Destra: SNAPSHOT
        right_frame = ttk.Labelframe(result_box, text=" Snapshot Storici ", padding=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # Lista con scrollbar
        scroll = ttk.Scrollbar(right_frame, bootstyle="round")
        scroll.pack(side="right", fill="y")
        
        self.list_snapshot = tk.Listbox(right_frame, height=15, width=40, yscrollcommand=scroll.set)
        self.list_snapshot.pack(side="left", fill="both", expand=True)
        self.list_snapshot.bind('<Double-1>', self.clicca_snapshot)
        
        scroll.config(command=self.list_snapshot.yview)

        # Variabile per memorizzare i link trovati
        self.lista_dati = []

    def avvia_ricerca(self):
        url = self.entry_url.get().strip()
        anno = self.entry_anno.get().strip()

        if not url or not anno:
            messagebox.showwarning("Attenzione", "Inserisci URL e Anno.")
            return

        # Avvio animazione caricamento
        self.lbl_status.config(text="Ricerca in corso...")
        self.progress.pack(fill="x", pady=5, before=self.lbl_status)
        self.progress.start(10)
        self.root.update()

        try:
            # 1. Whois
            self.text_whois.delete(1.0, tk.END)
            self.text_whois.insert(tk.END, "Caricamento dati...\n")
            self.root.update()
            
            info = ottieni_info_dominio(url)
            self.text_whois.delete(1.0, tk.END)
            self.text_whois.insert(tk.END, info)

            # 2. Wayback Machine
            self.list_snapshot.delete(0, tk.END)
            self.lista_dati = cerca_snapshot(url, anno)
            
            esito = "Nessun risultato"

            if self.lista_dati:
                esito = f"{len(self.lista_dati)} snapshot trovati"
                for snapshot in self.lista_dati:
                    self.list_snapshot.insert(tk.END, snapshot['data'])
                self.lbl_status.config(text=f"Operazione completata. Trovati: {len(self.lista_dati)}")
            else:
                self.list_snapshot.insert(tk.END, "Nessuno snapshot trovato.")
                self.lbl_status.config(text="Nessun risultato.")

            # 3. Salvataggio doppio (DB + CSV)
            salva_ricerca(url, anno, esito)
            accoda_su_csv(url, anno, esito)

        except Exception as e:
            self.lbl_status.config(text="Errore.")
            messagebox.showerror("Errore", str(e))

        finally:
            # Ferma caricamento
            self.progress.stop()
            self.progress.pack_forget()

    def clicca_snapshot(self, event):
        selezione = self.list_snapshot.curselection()
        if selezione:
            index = selezione[0]
            if index < len(self.lista_dati):
                link = self.lista_dati[index]['link']
                apri_browser(link)

    def apri_cronologia(self):
        # Finestra popup per vedere il database
        top = ttk.Toplevel(self.root)
        top.title("Cronologia")
        top.geometry("700x400")

        colonne = ('id', 'url', 'anno', 'esito', 'data')
        tree = ttk.Treeview(top, columns=colonne, show='headings', bootstyle="info")

        tree.heading('id', text='ID')
        tree.heading('url', text='Sito')
        tree.heading('anno', text='Anno')
        tree.heading('esito', text='Risultato')
        tree.heading('data', text='Data Ricerca')

        # Larghezza colonne
        tree.column('id', width=40)
        tree.column('url', width=150)
        
        # Scrollbar verticale
        scroll = ttk.Scrollbar(top, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)

        # Leggiamo dal DB
        dati = leggi_cronologia()
        for riga in dati:
            tree.insert('', tk.END, values=riga)

    def esporta_csv(self):
        # Funzione veloce per esportare tutto il DB in un file
        import csv
        filename = f"export_{datetime.now().strftime('%H%M%S')}.csv"
        try:
            dati = leggi_cronologia()
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "URL", "Anno", "Esito", "Data"])
                writer.writerows(dati)
            messagebox.showinfo("Fatto", f"Esportato in: {filename}")
        except Exception as e:
            messagebox.showerror("Errore", str(e))