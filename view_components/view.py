from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from view_components.dynamic_grid import DynamicGrid
from view_components.config_panel import ConfigPanel
from view_components.top_bar import TopBar

from ttkthemes import ThemedTk

import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from presenter_components.presenter import Presenter

from constants import PATH_LOGO_IMAGE

class View(ThemedTk):

    # GUI SETUP

    def __init__(self) -> None:
        super().__init__()
        self.title('SimilPhoto')
        self.minsize(width=800, height=730)
        self.geometry('1630x750')
        style = ttk.Style()
        style.theme_use('black')
        self._configure_styles()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.iconphoto(True, tk.PhotoImage(file=PATH_LOGO_IMAGE))
        logging.debug("View created")
        
    def _configure_styles(self) -> None:
        style = ttk.Style()
        style.configure("TButton", anchor=tk.CENTER)
        style.configure("TopBarButton.TButton", font=('TkDefaultFont', 14, "bold"))
        style.configure("TopBarLabel.TLabel", padding=5, font=('TkDefaultFont', 14, "bold"))
        style.configure("Timages_grid.TFrame", borderwidth=4, relief="solid", bordercolor="#303030")
        style.configure("ImageCard.TFrame", borderwidth=4, relief="solid", bordercolor="#ffffff")
        style.configure("Tconfig_panel.TFrame", borderwidth=4, relief="solid", bordercolor="#303030")
        style.configure("Ttop_bar.TFrame", borderwidth=4, relief="solid", bordercolor="#303030")

        style.configure("TCheckbutton", padding=[5, 0, 5, 0], background="#444444")
        style.configure("TProgressbar", troughcolor='#303030', background='#4AA72F', bordercolor="black")


    def init_ui(self, presenter:Presenter) -> None:
        logging.debug("Initializing UI")
        self.presenter = presenter
        self.main_frame = ttk.Frame(self, style="Tmain_frame.TFrame", padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.top_bar = TopBar(self.main_frame, self, presenter, style="Ttop_bar.TFrame", padding=10)
        self.images_grid = DynamicGrid(self.main_frame, self, presenter, style="Timages_grid.TFrame", padding=10)
        self.config_panel = ConfigPanel(self.main_frame, self, presenter, style="Tconfig_panel.TFrame", padding=10)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.top_bar.grid(row=0, column=0, sticky="new", padx=5, pady=5)
        self.images_grid.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.config_panel.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)

        # Initial state
        self.change_group_frame_visibility(False)

    # CONFIG PANEL

    def update_path_entry(self, path:str) -> None:
        self.config_panel.update_path_entry(path)

    def select_folder(self) -> str:
        return self.config_panel.select_folder()

    def set_path_entry_highlight(self, highlight:bool) -> None:
        self.config_panel.set_path_entry_highlight(highlight)

    def incorrect_path(self) -> None:
        self.config_panel.set_path_entry_highlight(True)
        self.config_panel.update_run_cancel_button("Run", self.config_panel.start_process)

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

    def add_message_to_queue(self, message:str) -> None:
        self.config_panel.queue.put(message)

    # IMAGES GRID

    def load_and_display_images(self, images_paths:list[str]) -> None:
        self.images_grid.remove_logo()
        self.empty_grid()
        for image_path in images_paths:
            self.images_grid.add_image(image_path)

    def empty_grid(self) -> None:
        self.images_grid.delete_all_images()

    def add_logo(self) -> None:
        self.images_grid.add_logo()

    # TOP BAR

    def update_status_label(self, text:str) -> None:
        self.top_bar.status_label.configure(text=text)

    def update_current_group_label(self, group_index:int, groups_count:int) -> None:
        self.top_bar.current_group_label.configure(text=f"{group_index+1}/{groups_count}")

    def change_group_frame_visibility(self, visible:bool=True) -> None:
        self.top_bar.group_frame.pack(side=tk.RIGHT) if visible else self.top_bar.group_frame.pack_forget()

    def change_group_buttons_state(self, visible:bool=True, state:str="normal") -> None:
        self.next_button_state(visible, state)
        self.previous_button_state(visible, state)

    def next_button_state(self, state:str="normal") -> None:
        self.top_bar.rigth_arrow_button.configure(state=state)

    def previous_button_state(self, state:str="normal") -> None:
        self.top_bar.left_arrow_button.configure(state=state)

    def on_closing(self):
        self.presenter.update_config_file_with_selected_parameters()
        try:
            logging.debug("Stopping processing thread...")
            self.config_panel.processing_thread.stop(True)
            self.config_panel.processing_thread.join()
        except AttributeError:
            logging.debug("No processing thread to stop")
            pass
        logging.debug("Destroying window...")
        self.destroy()