import os
import queue
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import json

from view_components.stoppable_thread import StoppableThread
from constants import *

from view_components.custom_entry import CustomEntry

import view_components.tooltip as tooltip

'''
This class represents the configuration panel on the right side of the main window.
'''
class ConfigPanel(ttk.Frame):

    def __init__(self, parent, window, presenter, *args, **kwargs) -> None:
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.presenter = presenter
        self.window = window
        self.processing_thread = None
        self._initialize(presenter)
        
    def _initialize(self, presenter) -> None:
        self.config_title_label = ttk.Label(self, text="Configuration", font=("Arial", 20))
        self.config_title_label.grid(row=0, column=0, sticky="nw", pady=(0, 10))
        self.file_search_frame = ttk.Frame(self)
        self.file_search_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        ttk.Separator(self, orient='horizontal').grid(row=2, column=0, sticky="nsew", pady=30)
        self.feature_extraction_frame = ttk.Frame(self)
        self.feature_extraction_frame.grid(row=3, column=0, sticky="nsew", pady=10)
        ttk.Separator(self, orient='horizontal').grid(row=4, column=0, sticky="nsew", pady=30)
        self.run_frame = ttk.Frame(self)
        self.run_frame.grid(row=5, column=0, sticky="nsew", pady=10)

        self.load_feature_extraction_methods_descriptions()

        self._create_file_search_submenu(presenter)
        self._create_feature_extraction_submenu(presenter)
        self._create_run_submenu(presenter)

    def _create_file_search_submenu(self, presenter) -> None:

        self.file_search_title_label = ttk.Label(self.file_search_frame, text="File search", font=("Arial", 15, 'bold', 'underline'))
        self.path_label = ttk.Label(self.file_search_frame, text="Searching for images in path:")
        tooltip.CreateToolTip(self.path_label, TOOLTIP_IMAGES_PATH)
        self.path_entry = CustomEntry(self.file_search_frame, width=50)
        self.path_entry.set_border_color("#303030")
        self.subdirectories_label = ttk.Label(self.file_search_frame, text="Include subdirectories")
        tooltip.CreateToolTip(self.subdirectories_label, TOOLTIP_INCLUDE_SUBDIRECTORIES)
        self.subdirectories_var = tk.BooleanVar()
        self.subdirectories_checkbox = ttk.Checkbutton(self.file_search_frame, variable=self.subdirectories_var)
        self.select_folder_button = ttk.Button(self.file_search_frame, text="Select folder", width=12)
        self.select_folder_button.bind("<Button-1>", presenter.handle_select_folder_button_click)

        self.file_types_frame = ttk.Frame(self.file_search_frame,)
        self.file_types_label = ttk.Label(self.file_types_frame, text="File types:")
        tooltip.CreateToolTip(self.file_types_label, TOOLTIP_FILE_TYPES)
        self.jpg_label = ttk.Label(self.file_types_frame, text="JPG")
        self.jpg_var = tk.BooleanVar()
        self.jpg_checkbox = ttk.Checkbutton(self.file_types_frame, variable=self.jpg_var)
        self.jpeg_label = ttk.Label(self.file_types_frame, text="JPEG")
        self.jpeg_var = tk.BooleanVar()
        self.jpeg_checkbox = ttk.Checkbutton(self.file_types_frame, variable=self.jpeg_var)
        self.png_label = ttk.Label(self.file_types_frame, text="PNG")
        self.png_var = tk.BooleanVar()
        self.png_checkbox = ttk.Checkbutton(self.file_types_frame, variable=self.png_var)
        self.webp_label = ttk.Label(self.file_types_frame, text="WEBP")
        self.webp_var = tk.BooleanVar()
        self.webp_checkbox = ttk.Checkbutton(self.file_types_frame, variable=self.webp_var)
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

    def _create_feature_extraction_submenu(self, presenter) -> None:

        self.feature_extraction_title_label = ttk.Label(self.feature_extraction_frame, text="Feature extraction", font=("Arial", 15, 'bold', 'underline'))

        self.feature_extraction_method_label = ttk.Label(self.feature_extraction_frame, text="Feature extraction method:")

        feature_extraction_methods = self.presenter.get_feature_extraction_methods()
        list_items = tk.Variable(value=feature_extraction_methods)
        self.feature_extraction_listbox = tk.Listbox(self.feature_extraction_frame, listvariable=list_items, selectmode=tk.SINGLE, exportselection=False, width=25, height=6, background="#303030", foreground="#ffffff", selectbackground="#202020", selectforeground="#ffffff", activestyle=tk.NONE, highlightthickness=0, bd=0, relief=tk.FLAT)
        self.feature_extraction_listbox.bind('<<ListboxSelect>>', self._on_feature_extraction_method_selected)
        self.feature_extraction_textbox = tk.Text(self.feature_extraction_frame, width=40, height=8, state=tk.DISABLED, wrap=tk.WORD, background="#303030", foreground="#ffffff", relief=tk.FLAT)

        self.feature_cache_recalculate_frame = ttk.Frame(self.feature_extraction_frame)

        self.cache_features_label = ttk.Label(self.feature_cache_recalculate_frame, text="Cache image features")
        tooltip.CreateToolTip(self.cache_features_label, TOOLTIP_CACHE_FEATURES)
        self.cache_features_var = tk.BooleanVar()
        self.cache_features_checkbox = ttk.Checkbutton(self.feature_cache_recalculate_frame, variable=self.cache_features_var)

        self.force_recalculate_features_label = ttk.Label(self.feature_cache_recalculate_frame, text="Force recalculate features")
        tooltip.CreateToolTip(self.force_recalculate_features_label, TOOLTIP_FORCE_RECALCULATE_FEATURES)
        self.force_recalculate_features_var = tk.BooleanVar()
        self.force_recalculate_features_checkbox = ttk.Checkbutton(self.feature_cache_recalculate_frame, variable=self.force_recalculate_features_var)

        self.feature_extraction_title_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0,15))
        self.feature_extraction_method_label.grid(row=1, column=0, columnspan=1, sticky=tk.W)
        self.feature_extraction_listbox.grid(row=2, column=0, columnspan=1, sticky=tk.W)
        self.feature_extraction_textbox.grid(row=1, column=1, rowspan=2, columnspan=2, sticky=tk.W, padx=15)

        self.cache_features_label.pack(side=tk.LEFT)
        self.cache_features_checkbox.pack(side=tk.LEFT)
        self.force_recalculate_features_label.pack(side=tk.LEFT, padx=(20,0))
        self.force_recalculate_features_checkbox.pack(side=tk.LEFT)
        self.feature_cache_recalculate_frame.grid(row=3, column=0, columnspan=4, sticky=tk.W, pady=(15,0))

        # POSSIBLE UPGRADE: Make a second listbox for choosing the parameters of the selected feature extraction method

    def _create_run_submenu(self, presenter) -> None:
        
        self.run_status_label = ttk.Label(self.run_frame, text="Status: Waiting to start...", font=("Arial", 12))
        self.run_status_label.grid(row=0, column=0, sticky=tk.W, pady=(0,10), columnspan=3)

        self.progress_bar = ttk.Progressbar(self.run_frame, orient=tk.HORIZONTAL, mode='determinate', length=500, maximum=100.1, )
        self.progress_bar.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(10,5))

        self.progress_bar_ind = ttk.Progressbar(self.run_frame, orient=tk.HORIZONTAL, mode='indeterminate', length=500)
        self.progress_bar_ind.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(5,5))

        self.run_cancel_button = ttk.Button(self.run_frame, text="Run", command=self.start_process)
        self.run_cancel_button.grid(row=3, column=2, sticky=tk.E, pady=(10,15), ipadx=15, ipady=2)
        self.queue = queue.Queue()
        self.periodic_call()

    def start_process(self) -> None:
        self.processing_thread = StoppableThread(target=self.presenter.handle_run_button_click)
        self.update_run_cancel_button("Cancel", self.cancel_process)
        self.processing_thread.start()

    def cancel_process(self) -> None:
        self.run_status_label['text'] = "Stopping..."
        print("Stopping...")
        self.processing_thread.stop()

    def periodic_call(self) -> None:
        """ Check every 100 ms if there is something new in the queue. """
        self.master.after(100, self.periodic_call)
        self.processIncoming()

    def processIncoming(self) -> None:
        """ Handle all the messages currently in the queue, if any. """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do what it says
                if msg[0] == "STARTED_STEP":
                    self.update_run_status_label(msg[1])
                elif msg[0] == "COMPLETED_STEP":
                    self.progress_bar['value'] = msg[1]
                elif msg[0] == "STEP_PROGRESS":
                    self.update_run_status_label(msg[1])

                self.progress_bar_ind.start(interval=25)

                if self.progress_bar['value'] >= 100:
                    self.update_run_cancel_button("Run", self.start_process)
                    self.progress_bar_ind.stop()
                
            except queue.Empty:
                pass
    
    def update_run_cancel_button(self, text:str, command:callable) -> None:
        self.run_cancel_button['text'] = text
        self.run_cancel_button['command'] = command

    def select_feature_extraction_method(self, method:str) -> None:
        self.feature_extraction_listbox.select_set(method)
        self._on_feature_extraction_method_selected(None)

    def _on_feature_extraction_method_selected(self, event) -> None:
        method = self.feature_extraction_listbox.get(self.feature_extraction_listbox.curselection())
        self.update_feature_extraction_textbox(self.feature_extraction_methods_descriptions[method])

    def update_feature_extraction_textbox(self, text:str) -> None:
        self.feature_extraction_textbox.config(state=tk.NORMAL)
        self.feature_extraction_textbox.delete(1.0, tk.END)
        self.feature_extraction_textbox.insert(tk.END, text)
        self.feature_extraction_textbox.config(state=tk.DISABLED)

    def update_path_entry(self, path:str) -> None:
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)

    def update_run_status_label(self, text:str) -> None:
        self.run_status_label.config(text=text)

    def set_path_entry_highlight(self, highlight:bool=True):
        if highlight:
            self.path_entry.set_border_color("red")
        else:
            self.path_entry.set_border_color("#303030")

    def select_folder(self) -> str:
        folder_path = os.path.normpath(filedialog.askdirectory())

        if folder_path != "" and folder_path != ".":
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_path)
        
        return folder_path

    def get_images_path(self) -> str:
        return self.path_entry.get()

    def get_subdirectories_checkbox_state(self) -> bool:
        return self.subdirectories_var.get()

    def get_file_types_variables(self) -> dict[str, tk.BooleanVar]:
        return self.file_types_variables

    def get_selected_feature_extraction_method(self) -> str:
        print(self.feature_extraction_listbox.get(self.feature_extraction_listbox.curselection()))
        return self.feature_extraction_listbox.get(self.feature_extraction_listbox.curselection())

    def get_cache_features_checkbox_state(self) -> bool:
        return self.cache_features_var.get()

    def get_force_recalculate_features_checkbox_state(self) -> bool:
        return self.force_recalculate_features_var.get()
    
    def load_feature_extraction_methods_descriptions(self) -> None:
        try:
            with open(PATH_FEATURE_EXTRACTION_METHOD_DESCRIPTIONS_FILE, "r") as f:
                self.feature_extraction_methods_descriptions = json.load(f)
        except Exception as e:
            print(e)
            self.feature_extraction_methods_descriptions = {}
            for method in CONFIG_DEFAULT_VALUE_SUPPORTED_FEATURE_EXTRACTION_METHODS.split(','):
                self.feature_extraction_methods_descriptions[method] = "No description available for " + method