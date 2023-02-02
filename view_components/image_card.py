import tkinter as tk
import os
from PIL import ImageTk, Image, ImageOps

from view_components.image_square_cropper import crop_square
import view_components.tooltip as tooltip

class ImageCard(tk.Frame):

    def __init__(self, parent, window, presenter, path, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.presenter = presenter
        self.window = window
        self.path = path
        self._initialize(presenter)
        
    def _initialize(self, presenter):
        
        # Title
        # TODO check title length
        title = self.path.split("\\")[-1]
        self.title_label = tk.Label(self, text=title)
        self.title_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        # Image
        img = Image.open(self.path)
        img = ImageOps.exif_transpose(img)
        origial_size = img.size
        img = crop_square(img)
        img = img.resize((180, 180))
        
        self.image = ImageTk.PhotoImage(img)
        self.image_label = tk.Label(self, image=self.image)
        self.image_label.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        # Directory
        splitted_path = self.path.split("\\")
        short_directory = splitted_path[0] + "\\" + splitted_path[1] + "\\..." + "\\" + splitted_path[-2]
        if len(short_directory) > 22:
            short_directory = splitted_path[0] + "\\..." + "\\" + splitted_path[-2]

        self.directory_label = tk.Label(self, text=f"Directory: {short_directory}")
        self.directory_label.grid(row=2, column=0, columnspan=2, sticky=tk.W)

        # Tooltip
        tooltip.CreateToolTip(self.directory_label, self.path)

        # File size
        file_size_by_os = str(round(os.path.getsize(self.path) / 1048576, 2)) + " MB"
        self.file_size_by_os_label = tk.Label(self, text=f"File size: {file_size_by_os}")
        self.file_size_by_os_label.grid(row=3, column=0, sticky=tk.W)

        # Resolution
        resolution = f"{origial_size[0]}x{origial_size[1]}"
        self.resolution_label = tk.Label(self, text=f"Resolution: {resolution}")
        self.resolution_label.grid(row=4, column=0, sticky=tk.W)
        
        # Delete button
        self.delete_button = tk.Button(self, text="Delete")
        self.delete_button.bind("<Button-1>", lambda: self.presenter.handle_delete_button_click(self.path))
        self.delete_button.grid(row=5, column=0, sticky=tk.W)

        # Open button
        self.open_button = tk.Button(self, text="Open")
        self.open_button.bind("<Button-1>", lambda: self.presenter.handle_open_button_click(self.path))
        self.open_button.grid(row=5, column=1, sticky=tk.E)