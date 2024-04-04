from tkinter import ttk


class Style:
    @staticmethod
    def apply_style(window):
        style = ttk.Style(window)
        window.tk.call('source', './ui/theme/dark.tcl')
        style.theme_use("dark")
