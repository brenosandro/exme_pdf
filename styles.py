from tkinter import Button, Canvas, Entry, Frame, ttk

def apply_styles(frame):
    style = {
        'background': '#f0f0f0',
        'foreground': '#000',
        'font': ('Arial', 10)
    }

    for widget in frame.winfo_children():
        if isinstance(widget, (Frame, Button, Entry, Canvas, ttk.Progressbar)):
            widget.configure(bg=style['background'], fg=style['foreground'], font=style['font'])
            if isinstance(widget, Frame):
                for sub_widget in widget.winfo_children():
                    sub_widget.configure(bg=style['background'], fg=style['foreground'], font=style['font'])
