import tkinter as tk

class CustomEntry(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.entry = tk.Entry(self, *args, **kwargs)
        self.entry.pack(fill="both", expand=2, padx=2, pady=2)
        self.entry.configure(background="#303030", fg="#ffffff", relief="flat")

        self.delete = self.entry.delete
        self.get = self.entry.get
        self.insert = self.entry.insert

    def set_border_color(self, color):
        self.configure(background=color)