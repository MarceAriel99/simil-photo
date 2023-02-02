import tkinter as tk
from PIL import ImageTk, Image, ImageOps

from view_components.image_card import ImageCard
from view_components.image_square_cropper import crop_square

class DynamicGrid(tk.Frame):

    def __init__(self, parent, window, presenter, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.text = tk.Text(self, wrap="char", borderwidth=0, highlightthickness=0, state="disabled")
        self.text.pack(fill="both", expand=True)
        self.images = []
        self.boxes = []
        self.window = window
        self.presenter = presenter

    def add_box(self, image_path):

        box = tk.Frame(self.text, bd=1, relief="sunken", width=200, height=320)
        box.pack_propagate(False)

        img_card = ImageCard(box, self.window, self.presenter, image_path)
        img_card.pack(padx=5, pady=5)

        self.images.append(img_card)
        
        self.boxes.append(box)
        self.text.configure(state="normal")
        self.text.window_create("end", window=box, padx=5, pady=5)
        self.text.configure(state="disabled", cursor="arrow")

    def delete_all_boxes(self):
        for box in self.boxes:
            box.destroy()
        self.boxes = []
        self.images = []
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")