import tkinter as tk

class TopBar(tk.Frame):

    def __init__(self, parent, window, presenter, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.presenter = presenter
        self.window = window
        self._initialize(presenter)
        
    def _initialize(self, presenter):
        self.status_label = tk.Label(self, text="", font=('TkDefaultFont', 16, "bold"))
        self.status_label.pack(side=tk.LEFT)

        self.group_frame = tk.Frame(self)

        self.rigth_arrow_button = tk.Button(self.group_frame, text=">")
        self.rigth_arrow_button.bind("<Button-1>", presenter.handle_next_group_button_click)
        self.rigth_arrow_button.pack(side=tk.RIGHT)
        self.current_group_label = tk.Label(self.group_frame, text="0/0")
        self.current_group_label.pack(side=tk.RIGHT)
        self.left_arrow_button = tk.Button(self.group_frame, text="<")
        self.left_arrow_button.bind("<Button-1>", presenter.handle_previous_group_button_click)
        self.left_arrow_button.pack(side=tk.RIGHT)

        self.group_frame.pack(side=tk.RIGHT)



    