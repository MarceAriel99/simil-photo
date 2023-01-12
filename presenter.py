from model import Model
from view import View

class Presenter:
    def __init__(self, model: Model, view: View) -> None:
        print("Presenter created")
        self.model = model
        self.view = view
        self.counter = 0
        self.clusters = None

    def run(self) -> None:
        print("Presenter running")
        self.view.init_ui(self)
        self.view.mainloop()

    def handle_select_folder_button_click(self, event=None) -> None:
        self.view.update_status_label("Selecting folder...")
        self.model.programManager.set_images_path(self.view.select_folder())
        self.view.update_status_label("Folder selected!")

    def handle_run_button_click(self, event=None) -> None:
        if self.counter == 0:
            self.model.run()
            self.view.update_status_label("Running...")
            self.clusters = self.model.get_images_paths()

        if self.counter < len(self.clusters):
            self.view.update_status_label(f"{len(self.clusters)} Groups found!")
            self.view.load_and_display_images(self.clusters[self.counter])
            self.counter += 1