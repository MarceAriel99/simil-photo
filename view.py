import random
from tkinter import filedialog
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

    def init_ui(self, presenter):
        print("Initializing UI")
        self._create_widgets(presenter)

    def _create_widgets(self, presenter):
        print("Creating widgets")
        self.main_frame = tk.Frame(self, padx=10, pady=10, bg="yellow")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.top_bar = tk.Frame(self.main_frame, bg="red")
        self.images_grid = tk.Frame(self.main_frame, bg="blue")
        self.config_panel = tk.Frame(self.main_frame, bg="green", padx=10, pady=10)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self._create_top_bar()
        self._create_images_grid(presenter)
        self._create_config_panel(presenter)

        self.top_bar.grid(row=0, column=0, sticky="new")
        self.images_grid.grid(row=1, column=0, sticky="nsew")
        self.config_panel.grid(row=0, column=1, rowspan=2, sticky="nsew")

    def _create_top_bar(self):

        self.groups_label = tk.Label(self.top_bar, text="0 Groups found!")
        self.groups_label.pack(side=tk.LEFT)

        self.rigth_arrow = tk.Button(self.top_bar, text=">")
        self.rigth_arrow.pack(side=tk.RIGHT)
        self.current_group_label = tk.Label(self.top_bar, text="0/0")
        self.current_group_label.pack(side=tk.RIGHT)
        self.left_arrow = tk.Button(self.top_bar, text="<")
        self.left_arrow.pack(side=tk.RIGHT)

    def _create_images_grid(self, presenter):
        self.gridframe = DynamicGrid(self.images_grid, self)
        self.gridframe.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _create_config_panel(self, presenter):
        self.config_title_label = tk.Label(self.config_panel, text="Configuration", font=("Arial", 20))
        self.config_title_label.grid(row=0, column=0, sticky="nw")
        self.file_search_frame = tk.Frame(self.config_panel)
        self.file_search_frame.grid(row=1, column=0, sticky="nsew", pady=20)

        self._create_file_search_submenu(presenter)


        self.run_button = tk.Button(
            self.config_panel,
            text="RUN",
            width=6,
            pady=5,
        )
        self.run_button.grid(row=2, column=0, sticky="nsew")
        self.run_button.bind("<Button-1>", presenter.handle_run_button_click)

    def _create_file_search_submenu(self, presenter):

        self.file_search_title_label = tk.Label(self.file_search_frame, text="File search", font=("Arial", 15, 'bold', 'underline'))
        self.path_label = tk.Label(self.file_search_frame, text="Searching for images in path:")
        self.path_entry = tk.Entry(self.file_search_frame, width=40)
        self.subdirectories_label = tk.Label(self.file_search_frame, text="Include subdirectories")
        self.subdirectories_checkbox = tk.Checkbutton(self.file_search_frame, variable=tk.IntVar())
        self.select_folder_button = tk.Button(self.file_search_frame, text="Select folder", width=10)
        self.select_folder_button.bind("<Button-1>", presenter.handle_select_folder_button_click)
        self.file_types_frame = tk.Frame(self.file_search_frame,)
        self.file_types_label = tk.Label(self.file_types_frame, text="File types:")
        self.jpg_label = tk.Label(self.file_types_frame, text="JPG")
        self.jpg_checkbox = tk.Checkbutton(self.file_types_frame, variable=tk.IntVar())
        self.jpeg_label = tk.Label(self.file_types_frame, text="JPEG")
        self.jpeg_checkbox = tk.Checkbutton(self.file_types_frame, variable=tk.IntVar())
        self.png_label = tk.Label(self.file_types_frame, text="PNG")
        self.png_checkbox = tk.Checkbutton(self.file_types_frame, variable=tk.IntVar())
        self.webp_label = tk.Label(self.file_types_frame, text="WEBP")
        self.webp_checkbox = tk.Checkbutton(self.file_types_frame, variable=tk.IntVar())

        self.file_types_label.pack(side=tk.LEFT, padx=(0,10))
        self.jpg_label.pack(side=tk.LEFT, padx=(10,0))
        self.jpg_checkbox.pack(side=tk.LEFT, padx=(0,10))
        self.jpeg_label.pack(side=tk.LEFT, padx=(10,0))
        self.jpeg_checkbox.pack(side=tk.LEFT, padx=(0,10))
        self.png_label.pack(side=tk.LEFT, padx=(10,0))
        self.png_checkbox.pack(side=tk.LEFT, padx=(0,10))
        self.webp_label.pack(side=tk.LEFT, padx=(10,0))
        self.webp_checkbox.pack(side=tk.LEFT, padx=(0,10))

        self.file_search_title_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0,10))
        self.path_label.grid(row=1, column=0, sticky=tk.W, padx=(0,10), pady=5)
        self.path_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W, padx=(10,0), pady=5)
        self.subdirectories_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.subdirectories_checkbox.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.select_folder_button.grid(row=2, column=2, sticky=tk.E, pady=5)
        self.file_types_frame.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(5,0))

    def select_folder(self) -> str:
        folder_path = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, folder_path)
        return folder_path

    def load_and_display_images(self, images_paths:list[str]):
        print("Loading images")
        self.gridframe.delete_all_boxes()
        for image_path in images_paths:
            self.gridframe.add_box(image_path)

    def update_status_label(self, text):
        self.groups_label.configure(text=text)