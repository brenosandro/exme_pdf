from PyPDF2 import PdfMerger
from tkinter import filedialog, messagebox, Button, Entry, Frame, Canvas, Scrollbar, ttk, Label, Tk
import threading
import styles

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.create_widgets()
        self.set_initial_window_size()

    def create_widgets(self):
        self.frame = Frame(self.root)
        self.frame.pack(padx=10, pady=10, fill='both', expand=True)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=0)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=0)
        self.frame.grid_rowconfigure(3, weight=1)

        self.title_label = Label(self.frame, text="Juntar arquivos PDF", font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=4, pady=(10, 20))

        self.description_label = Label(self.frame, text="Selecione os arquivos PDF e clique em 'Juntar PDFs':", font=("Arial", 12))
        self.description_label.grid(row=1, column=0, columnspan=4, pady=(0, 20))

        self.add_button = Button(self.frame, text="+", command=self.add_pdf_entry, font=("Arial", 14), width=5, height=2)
        self.add_button.grid(row=2, column=1, padx=5, pady=5, sticky='e')

        self.merge_button = Button(self.frame, text="Juntar PDFs", command=self.merge_pdfs, font=("Arial", 14), width=20, height=2)
        self.merge_button.grid(row=2, column=2, padx=5, pady=5, sticky='w')

        self.canvas = Canvas(self.frame)
        self.scrollbar = Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=3, column=0, columnspan=3, sticky='nsew', pady=(5, 0), padx=(5, 10))
        self.scrollbar.grid(row=3, column=3, sticky='ns', pady=(5, 0), padx=(0, 15))

        self.progress = ttk.Progressbar(self.frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=4, column=0, columnspan=4, pady=10)

        self.pdf_entries = []
        self.add_pdf_entry()

        styles.apply_styles(self.scrollable_frame)

    def set_initial_window_size(self):
        self.root.update_idletasks()
        min_width = 600
        min_height = 400
        self.root.minsize(min_width, min_height)
        self.root.geometry(f"{min_width}x{min_height}")

    def add_pdf_entry(self):
        row = len(self.pdf_entries)
        label = Label(self.scrollable_frame, text=f"{row + 1}.", font=("Arial", 12))
        label.grid(row=row, column=0, padx=5, pady=5, sticky='e')

        entry = Entry(self.scrollable_frame, width=50)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        self.pdf_entries.append(entry)

        browse_button = Button(self.scrollable_frame, text="Importar", command=lambda e=entry: self.browse_file(e))
        browse_button.grid(row=row, column=2, padx=5, pady=5)

        self.scrollable_frame.grid_columnconfigure(0, weight=0)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.scrollable_frame.grid_columnconfigure(2, weight=0)

    def browse_file(self, entry):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            entry.delete(0, 'end')
            entry.insert(0, file_path)

    def merge_pdfs(self):
        pdf_files = [entry.get() for entry in self.pdf_entries if entry.get()]

        if not pdf_files:
            messagebox.showerror("Erro", "Nenhum PDF foi selecionado.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not save_path:
            return

        threading.Thread(target=self.perform_merge, args=(pdf_files, save_path)).start()

    def perform_merge(self, pdf_files, save_path):
        try:
            self.progress["value"] = 0
            self.progress["maximum"] = len(pdf_files)
            merger = PdfMerger()

            for idx, pdf in enumerate(pdf_files):
                merger.append(pdf)
                self.progress["value"] = idx + 1
                self.root.update_idletasks()

            with open(save_path, 'wb') as output_pdf:
                merger.write(output_pdf)

            messagebox.showinfo("Sucesso", f"PDFs unidos com sucesso em {save_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao juntar os PDFs: {e}")

def main():
    root = Tk()
    app = PDFMergerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
