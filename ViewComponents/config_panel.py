import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class ConfigPanel(tk.Frame):

    def __init__(self, parent, window, presenter, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.presenter = presenter
        self.window = window
        self._initialize(presenter)
        
    def _initialize(self, presenter):
        self.config_title_label = tk.Label(self, text="Configuration", font=("Arial", 20))
        self.config_title_label.grid(row=0, column=0, sticky="nw")
        self.file_search_frame = tk.Frame(self)
        self.file_search_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        ttk.Separator(self, orient='horizontal').grid(row=2, column=0, sticky="nsew", pady=10)
        self.features_frame = tk.Frame(self)
        self.features_frame.grid(row=3, column=0, sticky="nsew", pady=10)
        ttk.Separator(self, orient='horizontal').grid(row=4, column=0, sticky="nsew", pady=10)
        self.feature_extraction_frame = tk.Frame(self)
        self.feature_extraction_frame.grid(row=5, column=0, sticky="nsew", pady=10)

        self._create_file_search_submenu(presenter)
        self._create_feature_extraction_submenu(presenter)
        
        self.run_button = tk.Button(self, text="RUN", width=6, pady=5)
        self.run_button.grid(row=6, column=0, sticky="sew")
        self.run_button.bind("<Button-1>", self.presenter.handle_run_button_click)

    def _create_file_search_submenu(self, presenter):

        self.file_search_title_label = tk.Label(self.file_search_frame, text="File search", font=("Arial", 15, 'bold', 'underline'))
        self.path_label = tk.Label(self.file_search_frame, text="Searching for images in path:")
        self.path_entry = tk.Entry(self.file_search_frame, width=50)
        self.subdirectories_label = tk.Label(self.file_search_frame, text="Include subdirectories")
        self.subdirectories_var = tk.BooleanVar()
        self.subdirectories_checkbox = tk.Checkbutton(self.file_search_frame, variable=self.subdirectories_var)
        self.select_folder_button = tk.Button(self.file_search_frame, text="Select folder", width=10)
        self.select_folder_button.bind("<Button-1>", presenter.handle_select_folder_button_click)

        self.file_types_frame = tk.Frame(self.file_search_frame,)
        self.file_types_label = tk.Label(self.file_types_frame, text="File types:")
        self.jpg_label = tk.Label(self.file_types_frame, text="JPG")
        self.jpg_var = tk.BooleanVar()
        self.jpg_checkbox = tk.Checkbutton(self.file_types_frame, variable=self.jpg_var)
        self.jpeg_label = tk.Label(self.file_types_frame, text="JPEG")
        self.jpeg_var = tk.BooleanVar()
        self.jpeg_checkbox = tk.Checkbutton(self.file_types_frame, variable=self.jpeg_var)
        self.png_label = tk.Label(self.file_types_frame, text="PNG")
        self.png_var = tk.BooleanVar()
        self.png_checkbox = tk.Checkbutton(self.file_types_frame, variable=self.png_var)
        self.webp_label = tk.Label(self.file_types_frame, text="WEBP")
        self.webp_var = tk.BooleanVar()
        self.webp_checkbox = tk.Checkbutton(self.file_types_frame, variable=self.webp_var)
        self.file_types_variables = {'jpg': self.jpg_var, 'jpeg': self.jpeg_var, 'png': self.png_var, 'webp': self.webp_var}

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

    def _create_feature_extraction_submenu(self, presenter):
        self.feature_extraction_title_label = tk.Label(self.features_frame, text="Feature extraction", font=("Arial", 15, 'bold', 'underline'))
        self.feature_extraction_method_label = tk.Label(self.features_frame, text="Feature extraction method:")
        items = ['vgg_16', 'mobilenet', 'color_histogram']
        list_items = tk.Variable(value=items)
        self.feature_extraction_listbox = tk.Listbox(self.features_frame, listvariable=list_items, selectmode=tk.SINGLE, width=25, height=10)
        self.feature_extraction_listbox.bind('<<ListboxSelect>>', presenter.on_feature_extraction_method_selected)
        self.feature_extraction_textbox = tk.Text(self.features_frame, width=40, height=12, state=tk.DISABLED)
        self.feature_cache_recalculate_frame = tk.Frame(self.features_frame)
        self.cache_features_label = tk.Label(self.feature_cache_recalculate_frame, text="Cache image features")
        self.cache_features_var = tk.BooleanVar()
        self.cache_features_checkbox = tk.Checkbutton(self.feature_cache_recalculate_frame, variable=self.cache_features_var)
        self.force_recalculate_features_label = tk.Label(self.feature_cache_recalculate_frame, text="Force recalculate features")
        self.force_recalculate_features_var = tk.BooleanVar()
        self.force_recalculate_features_checkbox = tk.Checkbutton(self.feature_cache_recalculate_frame, variable=self.force_recalculate_features_var)

        self.feature_extraction_title_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0,15))
        self.feature_extraction_method_label.grid(row=1, column=0, columnspan=1, sticky=tk.W)
        self.feature_extraction_listbox.grid(row=2, column=0, columnspan=1, sticky=tk.W)
        self.feature_extraction_textbox.grid(row=1, column=1, rowspan=2, columnspan=2, sticky=tk.W, padx=15)

        self.cache_features_label.pack(side=tk.LEFT)
        self.cache_features_checkbox.pack(side=tk.LEFT)
        self.force_recalculate_features_label.pack(side=tk.LEFT, padx=(20,0))
        self.force_recalculate_features_checkbox.pack(side=tk.LEFT)
        self.feature_cache_recalculate_frame.grid(row=3, column=0, columnspan=4, sticky=tk.W)

    def update_folder_path_entry(self, path):
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)

    def select_folder(self) -> str:
        folder_path = filedialog.askdirectory()

        if folder_path != "":
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_path)
        
        return folder_path