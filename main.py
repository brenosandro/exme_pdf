from tkinter import Tk, Frame, Button, Label, Listbox, Scrollbar, SINGLE, END, LEFT, RIGHT, BOTH, Y, IntVar, Checkbutton, Canvas, NSEW, Toplevel
from tkinter import filedialog, messagebox, Entry, ttk
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import threading
import os
import webbrowser
import styles

class PDFToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ferramenta PDF")
        self.pdf_entries = []  # Inicializar a lista de entradas de PDFs
        self.create_widgets()

    def create_widgets(self):
        self.frame = Frame(self.root)
        self.frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        self.title_label = Label(self.frame, text="Ferramenta PDF", font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=4, pady=(10, 20))
        
        self.description_label = Label(self.frame, text="Adicione arquivos PDF para começar:", font=("Arial", 12))
        self.description_label.grid(row=1, column=0, columnspan=4, pady=(0, 20))
        
        self.add_button = Button(self.frame, text="Adicionar PDFs", command=self.browse_files, font=("Arial", 14), width=20, height=2)
        self.add_button.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
        
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
        self.canvas.grid(row=3, column=0, columnspan=4, sticky='nsew', pady=(5, 0), padx=(5, 10))
        self.scrollbar.grid(row=3, column=4, sticky='ns', pady=(5, 0), padx=(0, 15))
        
        self.organize_button = Button(self.frame, text="Organizar PDFs", command=self.organize_pdfs, font=("Arial", 14), width=20, height=2)
        self.organize_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.organize_button.config(state='disabled')  # Inicialmente desabilitado
        
        self.extract_button = Button(self.frame, text="Extrair Páginas", command=self.show_pdf_pages, font=("Arial", 14), width=20, height=2)
        self.extract_button.grid(row=4, column=2, columnspan=2, padx=10, pady=10)
        self.extract_button.config(state='disabled')  # Inicialmente desabilitado

        self.combine_button = Button(self.frame, text="Combinar PDFs", command=self.merge_pdfs, font=("Arial", 14), width=20, height=2)
        self.combine_button.grid(row=5, column=0, columnspan=4, padx=10, pady=10)
        self.combine_button.config(state='disabled')  # Inicialmente desabilitado

        self.clear_button = Button(self.frame, text="Limpar Seleção", command=self.clear_selection, font=("Arial", 14), width=20, height=2)
        self.clear_button.grid(row=6, column=0, columnspan=4, padx=10, pady=10)
        
        self.progress = ttk.Progressbar(self.frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=7, column=0, columnspan=4, pady=10)
        styles.apply_styles(self.scrollable_frame)

    def browse_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if file_paths:
            for file_path in file_paths:
                self.add_pdf_entry(file_path)
                self.pdf_entries.append(file_path)  # Adicionar à lista global de PDFs
            self.organize_button.config(state='normal')  # Habilitar botão de organizar PDFs
            self.extract_button.config(state='normal')  # Habilitar botão de extrair PDFs
            self.combine_button.config(state='normal')  # Habilitar botão de combinar PDFs

    def add_pdf_entry(self, file_path=""):
        row = len(self.pdf_entries)
        label = Label(self.scrollable_frame, text=f"{row + 1}.", font=("Arial", 12))
        label.grid(row=row, column=0, padx=5, pady=5, sticky='e')
        entry = Entry(self.scrollable_frame, width=50)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
        entry.insert(0, file_path)
        view_button = Button(self.scrollable_frame, text="Visualizar", command=lambda fp=file_path: self.view_pdf(fp))
        view_button.grid(row=row, column=2, padx=5, pady=5)
        self.scrollable_frame.grid_columnconfigure(0, weight=0)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.scrollable_frame.grid_columnconfigure(2, weight=0)

    def view_pdf(self, file_path):
        # Abrir o arquivo PDF no visualizador padrão do sistema
        if os.path.isfile(file_path):
            webbrowser.open_new(file_path)
        else:
            messagebox.showerror("Erro", "Arquivo não encontrado.")

    def clear_selection(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.pdf_entries.clear()
        self.organize_button.config(state='disabled')
        self.extract_button.config(state='disabled')
        self.combine_button.config(state='disabled')

    def merge_pdfs(self):
        pdf_files = self.pdf_entries
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

    def show_pdf_pages(self):
        self.extract_window = Toplevel(self.root)
        self.extract_window.title("Extrair Páginas de PDF")
        
        back_button = Button(self.extract_window, text="Voltar", command=self.extract_window.destroy, font=("Arial", 14), width=20, height=2)
        back_button.grid(row=0, column=0, padx=10, pady=10)

        select_button = Button(self.extract_window, text="Extrair Selecionados", command=self.extract_selected_pages, font=("Arial", 14), width=20, height=2)
        select_button.grid(row=0, column=1, padx=10, pady=10)

        self.page_selection_frame = Frame(self.extract_window)
        self.page_selection_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

        self.page_canvas = Canvas(self.page_selection_frame)
        self.page_scrollbar = Scrollbar(self.page_selection_frame, orient="vertical", command=self.page_canvas.yview)
        self.page_scrollable_frame = Frame(self.page_canvas)

        self.page_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.page_canvas.configure(
                scrollregion=self.page_canvas.bbox("all")
            )
        )

        self.page_canvas.create_window((0, 0), window=self.page_scrollable_frame, anchor="nw")
        self.page_canvas.configure(yscrollcommand=self.page_scrollbar.set)

        self.page_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.page_scrollbar.pack(side=RIGHT, fill=Y)

        self.page_vars = {}
        self.checkbuttons = []

        for file_path in self.pdf_entries:
            reader = PdfReader(file_path)
            num_pages = len(reader.pages)
            self.page_vars[file_path] = [IntVar(value=0) for _ in range(num_pages)]

            for j in range(num_pages):
                check_button = Checkbutton(self.page_scrollable_frame, text=f"{os.path.basename(file_path)} - Página {j+1}", variable=self.page_vars[file_path][j], command=lambda fp=file_path, p=j: self.display_pdf_page(fp, p))
                check_button.pack(anchor='w', pady=2)
                self.checkbuttons.append(check_button)

        self.pdf_view_canvas = Canvas(self.extract_window, width=600, height=800, bg='white')
        self.pdf_view_canvas.grid(row=1, column=2, rowspan=2, sticky='nsew', padx=10, pady=10)
        self.extract_window.grid_columnconfigure(2, weight=1)
        self.extract_window.grid_rowconfigure(1, weight=1)

    def display_pdf_page(self, file_path, page_number):
        # Exibir a página selecionada no Canvas
        try:
            reader = PdfReader(file_path)
            page = reader.pages[page_number]
            page_text = page.extract_text()
            self.pdf_view_canvas.delete("all")
            self.pdf_view_canvas.create_text(10, 10, anchor='nw', text=page_text, fill="black")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível exibir a página: {e}")

    def extract_selected_pages(self):
        save_dir = filedialog.askdirectory(title="Selecione o diretório para salvar os PDFs extraídos")
        if not save_dir:
            return

        try:
            for file_path, vars_list in self.page_vars.items():
                reader = PdfReader(file_path)
                for i, var in enumerate(vars_list):
                    if var.get() == 1:
                        writer = PdfWriter()
                        writer.add_page(reader.pages[i])
                        output_path = f"{save_dir}/{os.path.basename(file_path).replace('.pdf', '')}_pagina_{i + 1}.pdf"
                        with open(output_path, 'wb') as output_pdf:
                            writer.write(output_pdf)

            messagebox.showinfo("Sucesso", f"Todas as páginas selecionadas foram extraídas e salvas em {save_dir}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao extrair os PDFs: {e}")
        finally:
            self.extract_window.destroy()

    def organize_pdfs(self):
        self.organize_window = Toplevel(self.root)
        self.organize_window.title("Organizar PDFs")

        back_button = Button(self.organize_window, text="Voltar", command=self.organize_window.destroy, font=("Arial", 14), width=20, height=2)
        back_button.grid(row=0, column=0, padx=10, pady=10)

        save_order_button = Button(self.organize_window, text="Salvar Ordem", command=self.save_order, font=("Arial", 14), width=20, height=2)
        save_order_button.grid(row=0, column=1, padx=10, pady=10)

        self.organize_listbox = Listbox(self.organize_window, selectmode=SINGLE)
        self.organize_listbox.grid(row=1, column=0, columnspan=2, sticky='nsew')

        organize_scrollbar = Scrollbar(self.organize_window, orient="vertical")
        organize_scrollbar.grid(row=1, column=2, sticky='ns')

        self.organize_listbox.config(yscrollcommand=organize_scrollbar.set)
        organize_scrollbar.config(command=self.organize_listbox.yview)

        for entry in self.pdf_entries:
            self.organize_listbox.insert(END, entry)

        up_button = Button(self.organize_window, text="Subir", command=self.move_up)
        up_button.grid(row=2, column=0, padx=10, pady=10)

        down_button = Button(self.organize_window, text="Descer", command=self.move_down)
        down_button.grid(row=2, column=1, padx=10, pady=10)

        self.pdf_view_canvas = Canvas(self.organize_window, width=600, height=800, bg='white')
        self.pdf_view_canvas.grid(row=1, column=3, rowspan=3, sticky='nsew', padx=10, pady=10)
        self.organize_window.grid_columnconfigure(3, weight=1)
        self.organize_window.grid_rowconfigure(1, weight=1)

        self.organize_listbox.bind("<<ListboxSelect>>", self.on_select)

    def on_select(self, event):
        selected = self.organize_listbox.curselection()
        if selected:
            index = selected[0]
            file_path = self.pdf_entries[index]
            self.display_pdf_page(file_path, 0)

    def display_pdf_page(self, file_path, page_number):
        # Exibir a página selecionada no Canvas
        try:
            reader = PdfReader(file_path)
            page = reader.pages[page_number]
            page_text = page.extract_text()
            self.pdf_view_canvas.delete("all")
            self.pdf_view_canvas.create_text(10, 10, anchor='nw', text=page_text, fill="black")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível exibir a página: {e}")

    def move_up(self):
        selected = self.organize_listbox.curselection()
        if not selected:
            return
        for idx in selected:
            if idx == 0:
                continue
            text = self.organize_listbox.get(idx)
            self.organize_listbox.delete(idx)
            self.organize_listbox.insert(idx-1, text)
            self.organize_listbox.selection_set(idx-1)

    def move_down(self):
        selected = self.organize_listbox.curselection()
        if not selected:
            return
        for idx in reversed(selected):
            if idx == self.organize_listbox.size()-1:
                continue
            text = self.organize_listbox.get(idx)
            self.organize_listbox.delete(idx)
            self.organize_listbox.insert(idx+1, text)
            self.organize_listbox.selection_set(idx+1)

    def save_order(self):
        self.pdf_entries = [self.organize_listbox.get(idx) for idx in range(self.organize_listbox.size())]
        self.organize_window.destroy()

def main():
    root = Tk()
    app = PDFToolApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
