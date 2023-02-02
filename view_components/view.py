import tkinter as tk
from tkinter import ttk

from view_components.dynamic_grid import DynamicGrid
from view_components.config_panel import ConfigPanel
from view_components.top_bar import TopBar
  
class View(tk.Tk):

    # GUI SETUP

    def __init__(self):
        print("View created")
        super().__init__()
        self.title('SimilPhoto')
        self.minsize(width=800, height=730)
        self.geometry('1600x680')

    def init_ui(self, presenter):
        print("Initializing UI")
        self.main_frame = tk.Frame(self, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.top_bar = TopBar(self.main_frame, self, presenter, padx=10, pady=10)
        self.images_grid = DynamicGrid(self.main_frame, self, presenter, padx=10, pady=10)
        self.config_panel = ConfigPanel(self.main_frame, self, presenter)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.top_bar.grid(row=0, column=0, sticky="new")
        self.images_grid.grid(row=1, column=0, sticky="nsew")
        self.config_panel.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Initial state
        self.change_group_frame_visibility(False)

    # CONFIG PANEL

    def update_path_entry(self, path):
        self.config_panel.update_path_entry(path)

    def select_folder(self) -> str:
        return self.config_panel.select_folder()

    def set_path_entry_highlight(self, highlight:bool):
        self.config_panel.set_path_entry_highlight(highlight)

    def get_images_path(self) -> str:
        return self.config_panel.get_images_path()

    def get_subdirectories_checkbox_state(self) -> bool:
        return self.config_panel.get_subdirectories_checkbox_state()

    def get_file_types_variables(self) -> dict[str, tk.BooleanVar]:
        return self.config_panel.get_file_types_variables()

    def get_selected_feature_extraction_method(self) -> str:
        return self.config_panel.get_selected_feature_extraction_method()

    def get_cache_features_checkbox_state(self) -> bool:
        return self.config_panel.get_cache_features_checkbox_state()

    def get_force_recalculate_features_checkbox_state(self) -> bool:
        return self.config_panel.get_force_recalculate_features_checkbox_state()

    def add_message_to_queue(self, message:str):
        self.config_panel.queue.put(message)

    # IMAGES GRID

    def load_and_display_images(self, images_paths:list[str]):
        self.empty_grid()
        for image_path in images_paths:
            self.images_grid.add_image(image_path)

    def empty_grid(self):
        self.images_grid.delete_all_images()

    # TOP BAR

    def update_status_label(self, text):
        self.top_bar.status_label.configure(text=text)

    def update_current_group_label(self, group_index:int, groups_count:int):
        self.top_bar.current_group_label.configure(text=f"{group_index+1}/{groups_count}")

    def change_group_frame_visibility(self, visible:bool=True):
        self.top_bar.group_frame.pack(side=tk.RIGHT) if visible else self.top_bar.group_frame.pack_forget()

    def change_group_buttons_state(self, visible:bool=True, state:str="normal"):
        self.next_button_state(visible, state)
        self.previous_button_state(visible, state)

    def next_button_state(self, state:str="normal"):
        self.top_bar.rigth_arrow_button.configure(state=state)

    def previous_button_state(self, state:str="normal"):
        self.top_bar.left_arrow_button.configure(state=state)