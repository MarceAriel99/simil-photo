import random
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageOps
from image_square_cropper import crop_square

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
        
        

class View(tk.Tk):

    def __init__(self):
        print("View created")
        super().__init__()
        self.title('SimilPhoto')
        self.minsize(width=800, height=600)
        self.geometry('1200x680')
        self.img = ImageTk.PhotoImage(Image.open("E:\Mis_Archivos\Proyects\Programs\SimilPhoto\Images\gato.jpg").resize((100, 100)))

    def init_ui(self, presenter):
        print("Initializing UI")
        self._create_widgets(presenter)

    def _create_widgets(self, presenter):
        print("Creating widgets")
        self.frame = tk.Frame(self, padx=10, pady=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.status_label = tk.Label(self.frame, text="Image Clustering")
        self.status_label.pack(side=tk.TOP, anchor=tk.NW)

        self.run_button = tk.Button(
            self.frame,
            text="RUN",
            width=6,
            pady=5,
        )
        self.run_button.pack(side=tk.BOTTOM, anchor=tk.E)
        self.run_button.bind("<Button-1>", presenter.handle_run_button_click)

        self.gridframe = DynamicGrid(self.frame, self)
        self.gridframe.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # self.gridframe = tk.Frame(self, padx=10, pady=10)
        # self.gridframe.pack(fill=tk.BOTH, expand=True)      

        # button1=tk.Button(self.gridframe, image=self.img)
        # button1.grid(row=0,column=0)
        # button2=tk.Button(self.gridframe, image=self.img)
        # button2.grid(row=0,column=1)
        # button3=tk.Button(self.gridframe, image=self.img)
        # button3.grid(row=0,column=2)
        # button4=tk.Button(self.gridframe, image=self.img)
        # button4.grid(row=0,column=3)

    def load_and_display_images(self, images_paths:list[str]):
        print("Loading images")
        self.gridframe.delete_all_boxes()
        for image_path in images_paths:
            self.gridframe.add_box(image_path)


    def update_status_label(self, text):
        self.status_label.configure(text=text)