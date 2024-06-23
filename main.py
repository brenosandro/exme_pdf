from tkinter import Tk, Frame, Button, Label
from extractor import PDFExtractorApp
from merger import PDFMergerApp
import styles

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Tool")
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

        styles.apply_styles(self.frame)

    def open_extractor(self):
        self.clear_frame()
        PDFExtractorApp(self.root)

    def open_merger(self):
        self.clear_frame()
        PDFMergerApp(self.root)

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.pack_forget()

def main():
    root = Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
