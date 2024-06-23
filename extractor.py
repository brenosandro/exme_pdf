from PyPDF2 import PdfReader, PdfWriter
from tkinter import filedialog, messagebox, Button, Frame
import styles

class PDFExtractorApp:
    def __init__(self, root):
        self.root = root
        self.create_widgets()

    def create_widgets(self):
        self.frame = Frame(self.root)
        self.frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.select_pdf_button = Button(self.frame, text="Selecionar PDF", command=self.select_pdf)
        self.select_pdf_button.grid(row=0, column=0, padx=5, pady=5)

        self.extract_button = Button(self.frame, text="Extrair Páginas", command=self.extract_pdfs, state='disabled')
        self.extract_button.grid(row=0, column=1, padx=5, pady=5)

        styles.apply_styles(self.frame)

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_path:
            self.extract_button.config(state='normal')

    def extract_pdfs(self):
        try:
            reader = PdfReader(self.pdf_path)
            num_pages = len(reader.pages)

            save_dir = filedialog.askdirectory(title="Selecione o diretório para salvar os PDFs extraídos")
            if not save_dir:
                return

            for i in range(num_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[i])

                output_path = f"{save_dir}/pagina_{i + 1}.pdf"
                with open(output_path, 'wb') as output_pdf:
                    writer.write(output_pdf)

            messagebox.showinfo("Sucesso", f"Todas as páginas foram extraídas e salvas em {save_dir}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao extrair os PDFs: {e}")
