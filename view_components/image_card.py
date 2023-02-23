import tkinter as tk
import os
from PIL import ImageTk, Image, ImageOps

from view_components.image_square_cropper import crop_square
import view_components.tooltip as tooltip

class ImageCard(tk.Frame):

    def __init__(self, parent, window, presenter, path, *args, **kwargs) -> None:
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.presenter = presenter
        self.window = window
        self.path = path
        self.grid = parent
        self._initialize(presenter)
        
    def _initialize(self, presenter) -> None:
        
        # Title
        self.title_label = tk.Label(self)

        title = self.path.split("\\")[-1]
        full_title = title
        if len(title) > 23:
            title = title[:18] + "..." + title.split(".")[-1]
            tooltip.CreateToolTip(self.title_label, full_title)

        self.title_label.config(text=title, font=('TkDefaultFont', 10, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=5, pady=2)

        # Image
        img = Image.open(self.path)
        img = ImageOps.exif_transpose(img)
        origial_size = img.size
        img = crop_square(img)
        img = img.resize((180, 180))
        
        self.image = ImageTk.PhotoImage(img)
        self.image_label = tk.Label(self, image=self.image)
        self.image_label.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=3)

        # Directory
        self.directory_label = tk.Label(self)

        splitted_path = self.path.split("\\")
        short_directory = splitted_path[0] + "\\" + splitted_path[1] + "\\..." + "\\" + splitted_path[-2]
        if len(short_directory) > 22:
            short_directory = splitted_path[0] + "\\..." + "\\" + splitted_path[-2]
            tooltip.CreateToolTip(self.directory_label, self.path)

        self.directory_label.config(text=f"Directory: {short_directory}")
        self.directory_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5)    

        # File size
        file_size_in_bytes = os.path.getsize(self.path)
        if file_size_in_bytes < 1024:
            file_size = str(file_size_in_bytes) + " B"
        elif file_size_in_bytes < 1048576:
            file_size = str(round(file_size_in_bytes / 1024, 2)) + " KB"
        else:
            file_size = str(round(file_size_in_bytes / 1048576, 2)) + " MB"
        
        self.file_size_by_os_label = tk.Label(self, text=f"File size: {file_size}")
        self.file_size_by_os_label.grid(row=3, column=0, sticky=tk.W, padx=5)

        # Resolution
        resolution = f"{origial_size[0]}x{origial_size[1]}"
        self.resolution_label = tk.Label(self, text=f"Resolution: {resolution}")
        self.resolution_label.grid(row=4, column=0, sticky=tk.W, padx=5)
        
        # Delete button
        self.delete_button = tk.Button(self, text="Delete file")
        self.delete_button.bind("<Button-1>", lambda event, path=self.path: self.handle_delete_button_click(path))
        self.delete_button.grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        tooltip.CreateToolTip(self.delete_button, "WARNING: This will delete the file permanently!")

        # Open button
        self.open_button = tk.Button(self, text="Open")
        self.open_button.bind("<Button-1>", lambda event, path=self.path: self.presenter.handle_open_button_click(path))
        self.open_button.grid(row=5, column=1, sticky=tk.E, padx=5, pady=2)
    
    def handle_delete_button_click(self, path:str) -> None:
        self.presenter.handle_delete_button_click(path)
        self.destroy()