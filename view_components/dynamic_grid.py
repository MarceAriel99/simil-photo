import tkinter as tk
from PIL import ImageTk, Image, ImageOps

from view_components.image_card import ImageCard
from view_components.image_square_cropper import crop_square

# TODO: Add scrollbar on the right
class DynamicGrid(tk.Frame):

    def __init__(self, parent, window, presenter, *args, **kwargs) -> None:
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.text = tk.Text(self, wrap="char", borderwidth=0, highlightthickness=0, state="disabled", cursor="arrow")
        self.text.pack(fill="both", expand=True)
        self.images = []
        self.window = window
        self.presenter = presenter

    def add_image(self, image_path:str) -> None:
    
        img_card = ImageCard(self.text, self.window, self.presenter, image_path, bd=1, relief="sunken")

        self.images.append(img_card)
        
        self.text.configure(state="normal")
        self.text.window_create("end", window=img_card, padx=5, pady=5)
        self.text.configure(state="disabled", cursor="arrow")

    def delete_all_images(self) -> None:
        for image in self.images:
            image.destroy()
        self.images = []
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")