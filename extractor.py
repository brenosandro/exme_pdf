from PyPDF2 import PdfReader, PdfWriter
from tkinter import filedialog, messagebox, Button, Frame, Checkbutton, Toplevel, IntVar
import styles

class PDFExtractorApp:
    def __init__(self, root, go_back_callback):
        self.root = root
        self.go_back_callback = go_back_callback  # Callback para voltar à tela principal
        self.create_widgets()

    def create_widgets(self):
        self.frame = Frame(self.root)
        self.frame.pack(padx=10, pady=10, fill='both', expand=True)
        self.select_pdf_button = Button(self.frame, text="Selecionar PDF", command=self.select_pdf)
        self.select_pdf_button.grid(row=0, column=0, padx=5, pady=5)
        self.extract_button = Button(self.frame, text="Extrair Páginas", command=self.extract_pdfs, state='disabled')
        self.extract_button.grid(row=0, column=1, padx=5, pady=5)
        self.back_button = Button(self.frame, text="Voltar", command=self.go_back)
        self.back_button.grid(row=0, column=2, padx=5, pady=5)
        styles.apply_styles(self.frame)

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_path:
            self.extract_button.config(state='normal')
            self.show_pdf_pages()

    def show_pdf_pages(self):
        self.page_selection_window = Toplevel(self.root)
        self.page_selection_window.title("Selecionar Páginas")
        
        reader = PdfReader(self.pdf_path)
        num_pages = len(reader.pages)
        
        self.page_vars = [IntVar(value=0) for _ in range(num_pages)]
        
        for i in range(num_pages):
            check_button = Checkbutton(self.page_selection_window, text=f"Página {i+1}", variable=self.page_vars[i])
            check_button.pack(anchor='w')

        select_button = Button(self.page_selection_window, text="Selecionar", command=self.extract_selected_pages)
        select_button.pack()

    def extract_selected_pages(self):
        try:
            reader = PdfReader(self.pdf_path)
            save_dir = filedialog.askdirectory(title="Selecione o diretório para salvar os PDFs extraídos")
            if not save_dir:
                return
            
            for i, var in enumerate(self.page_vars):
                if var.get() == 1:
                    writer = PdfWriter()
                    writer.add_page(reader.pages[i])
                    output_path = f"{save_dir}/pagina_{i + 1}.pdf"
                    with open(output_path, 'wb') as output_pdf:
                        writer.write(output_pdf)
            
            messagebox.showinfo("Sucesso", f"Todas as páginas selecionadas foram extraídas e salvas em {save_dir}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao extrair os PDFs: {e}")
        finally:
            self.page_selection_window.destroy()

    def extract_pdfs(self):
        # Método existente
        pass

    def go_back(self):
        self.frame.destroy()
        self.go_back_callback()
