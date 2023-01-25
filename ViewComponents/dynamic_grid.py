import tkinter as tk
from PIL import ImageTk, Image, ImageOps

from ViewComponents.image_square_cropper import crop_square


class DynamicGrid(tk.Frame):
    def __init__(self, parent, window, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.text = tk.Text(self, wrap="char", borderwidth=0, highlightthickness=0, state="disabled")
        self.text.pack(fill="both", expand=True)
        self.images = []
        self.boxes = []
        self.window = window

    def add_box(self, image_path):

        img = Image.open(image_path)
        img = ImageOps.exif_transpose(img)
        img = crop_square(img)
        img = img.resize((100, 100))
        img = ImageTk.PhotoImage(img)

        self.images.append(img)

        box = tk.Frame(self.text, bd=1, relief="sunken", width=100, height=100)

        button = tk.Button(box, image=img, cursor="hand2", command=lambda: self.delete_all_boxes())
        button.pack()
        
        self.boxes.append(box)
        self.text.configure(state="normal")
        self.text.window_create("end", window=box)
        self.text.configure(state="disabled", cursor="arrow")

    def delete_all_boxes(self):
        for box in self.boxes:
            box.destroy()
        self.boxes = []
        self.images = []
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")