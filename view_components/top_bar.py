import tkinter as tk
from tkinter import ttk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from presenter_components.presenter import Presenter

class TopBar(ttk.Frame):

    def __init__(self, parent, window, presenter:Presenter, *args, **kwargs) -> None:
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.presenter = presenter
        self.window = window
        self._initialize(presenter)
        
    def _initialize(self, presenter:Presenter) -> None:
        self.status_label = ttk.Label(self, text="", font=('TkDefaultFont', 16, "bold"))
        self.status_label.pack(side=tk.LEFT)

        self.group_frame = ttk.Frame(self)

        self.rigth_arrow_button = ttk.Button(self.group_frame, text=">", width=2)
        self.rigth_arrow_button.configure(style="TopBarButton.TButton")
        self.rigth_arrow_button.bind("<Button-1>", presenter.handle_next_group_button_click)
        self.rigth_arrow_button.pack(side=tk.RIGHT)

        self.current_group_label = ttk.Label(self.group_frame, text="0/0")
        self.current_group_label.configure(style="TopBarLabel.TLabel")
        self.current_group_label.pack(side=tk.RIGHT)

        self.left_arrow_button = ttk.Button(self.group_frame, text="<", width=2)
        self.left_arrow_button.configure(style="TopBarButton.TButton")
        self.left_arrow_button.bind("<Button-1>", presenter.handle_previous_group_button_click)
        self.left_arrow_button.pack(side=tk.RIGHT)

        self.group_frame.pack(side=tk.RIGHT)



    