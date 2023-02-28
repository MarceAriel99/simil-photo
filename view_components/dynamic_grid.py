import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageOps

from view_components.image_card import ImageCard
from view_components.image_square_cropper import crop_square

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from presenter_components.presenter import Presenter

class DynamicGrid(ttk.Frame):

    def __init__(self, parent, window, presenter:Presenter, *args, **kwargs) -> None:
        ttk.Frame.__init__(self, parent, *args, **kwargs)
    
        self.text = tk.Text(self, wrap="char", borderwidth=0, highlightthickness=0, state="disabled", cursor="arrow", background="#303030")
        
        self.images = []
        self.window = window
        self.presenter = presenter
        
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.text.yview, takefocus=False)
        self.text['yscrollcommand'] = scrollbar.set

        scrollbar.pack(side="right", fill="y", expand=False, padx=5)
        self.text.pack(side="right", fill="both", expand=True)

    def add_image(self, image_path:str) -> None:
    
        img_card = ImageCard(self.text, self.window, self.presenter, image_path, style="ImageCard.TFrame")

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