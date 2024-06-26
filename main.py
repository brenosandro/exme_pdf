from tkinter import Tk, Frame, Button, Label, Toplevel, Listbox, Scrollbar, SINGLE, END, LEFT, RIGHT, BOTH, Y
from extractor import PDFExtractorApp
from merger import PDFMergerApp
import styles

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Tool")
        self.pdf_entries = []  # Inicializar a lista de entradas de PDFs
        self.create_widgets()

    def create_widgets(self):
        self.frame = Frame(self.root)
        self.frame.pack(padx=10, pady=10, fill='both', expand=True)
        self.title_label = Label(self.frame, text="Juntar ou Extrair PDF", font=("Arial", 20, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))
        self.description_label = Label(self.frame, text="Escolha uma das opções abaixo para começar:", font=("Arial", 12))
        self.description_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        self.extractor_button = Button(self.frame, text="Extrair Páginas PDF", command=self.open_extractor, font=("Arial", 14), width=20, height=2)
        self.extractor_button.grid(row=2, column=0, padx=10, pady=10)
        self.merger_button = Button(self.frame, text="Juntar PDFs", command=self.open_merger, font=("Arial", 14), width=20, height=2)
        self.merger_button.grid(row=2, column=1, padx=10, pady=10)
        self.organize_button = Button(self.frame, text="Organizar PDFs", command=self.organize_pdfs, font=("Arial", 14), width=20, height=2)
        self.organize_button.grid(row=2, column=2, padx=10, pady=10)
        self.organize_button.config(state='disabled')  # Inicialmente desabilitado
        styles.apply_styles(self.frame)

    def open_extractor(self):
        self.clear_frame()
        PDFExtractorApp(self.root, self.go_back_to_main)

    def open_merger(self):
        self.clear_frame()
        PDFMergerApp(self.root, self.pdf_entries, self.enable_organize_button, self.go_back_to_main)

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.pack_forget()

    def enable_organize_button(self):
        if self.pdf_entries:  # Verifica se há PDFs adicionados
            self.organize_button.config(state='normal')

    def go_back_to_main(self):
        self.clear_frame()
        self.create_widgets()

    def organize_pdfs(self):
        if not self.pdf_entries:
            return
        
        organize_window = Toplevel(self.root)
        organize_window.title("Organizar PDFs")
        organize_frame = Frame(organize_window)
        organize_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        listbox = Listbox(organize_frame, selectmode=SINGLE)
        listbox.pack(side=LEFT, fill=BOTH, expand=True)
        
        scrollbar = Scrollbar(organize_frame, orient="vertical")
        scrollbar.pack(side=RIGHT, fill=Y)
        
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        
        for entry in self.pdf_entries:
            listbox.insert(END, entry)

        def move_up():
            selected = listbox.curselection()
            if not selected:
                return
            for idx in selected:
                if idx == 0:
                    continue
                text = listbox.get(idx)
                listbox.delete(idx)
                listbox.insert(idx-1, text)
                listbox.selection_set(idx-1)
        
        def move_down():
            selected = listbox.curselection()
            if not selected:
                return
            for idx in reversed(selected):
                if idx == listbox.size()-1:
                    continue
                text = listbox.get(idx)
                listbox.delete(idx)
                listbox.insert(idx+1, text)
                listbox.selection_set(idx+1)

        def preview_pdf(event):
            selected = listbox.curselection()
            if selected:
                pdf_path = listbox.get(selected[0])
                # Código para visualizar o PDF (dependendo da implementação específica)
        
        listbox.bind('<Double-1>', preview_pdf)
        
        up_button = Button(organize_frame, text="Subir", command=move_up)
        up_button.pack(side=LEFT)
        
        down_button = Button(organize_frame, text="Descer", command=move_down)
        down_button.pack(side=RIGHT)

def main():
    root = Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
