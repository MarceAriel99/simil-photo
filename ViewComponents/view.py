import tkinter as tk
from tkinter import ttk

from ViewComponents.dynamic_grid import DynamicGrid
from ViewComponents.config_panel import ConfigPanel
from ViewComponents.top_bar import TopBar
  
class View(tk.Tk):

    # GUI SETUP

    def __init__(self):
        print("View created")
        super().__init__()
        self.title('SimilPhoto')
        self.minsize(width=800, height=600)
        self.geometry('1400x680')

    def init_ui(self, presenter):
        print("Initializing UI")
        self.main_frame = tk.Frame(self, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.top_bar = TopBar(self.main_frame, self, presenter)
        self.images_grid = DynamicGrid(self.main_frame, self, padx=10, pady=10)
        self.config_panel = ConfigPanel(self.main_frame, self, presenter)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.top_bar.grid(row=0, column=0, sticky="new")
        self.images_grid.grid(row=1, column=0, sticky="nsew")
        self.config_panel.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # Initial state
        self.change_group_frame_visibility(False)

    # CONFIG PANEL

    def update_folder_path_entry(self, path):
        self.config_panel.update_folder_path_entry(path)

    def select_folder(self) -> str:
        return self.config_panel.select_folder()

    # IMAGES GRID

    def load_and_display_images(self, images_paths:list[str]):
        self.empty_grid()
        for image_path in images_paths:
            self.images_grid.add_box(image_path)

    def empty_grid(self):
        self.images_grid.delete_all_boxes()

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