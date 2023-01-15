from model import Model
from view import View

class Presenter:
    def __init__(self, model: Model, view: View) -> None:
        print("Presenter created")
        self.model = model
        self.view = view
        self.clusters = None
        self.current_cluster = 0

    def _update_view_with_saved_data(self) -> None:
        folder_path_entry = self.model.programManager.get_images_path() if self.model.programManager.get_images_path() else "No folder selected"
        self.view.update_folder_path_entry(folder_path_entry)

    def run(self) -> None:
        print("Presenter running")
        self.view.init_ui(self)
        self.model.init_model(self)
        self._update_view_with_saved_data()
        self.view.mainloop()

    def run_completed(self) -> None:
        self.current_cluster = 0
        self.clusters = self.model.get_images_paths()
        print(self.clusters)
        self.view.update_status_label(f"{len(self.clusters)} Groups found!")
        self.view.current_group_label.config(text=f"{self.current_cluster + 1} / {len(self.clusters)}")
        self.view.load_and_display_images(self.clusters[self.current_cluster])

    def handle_next_group_button_click(self, event=None) -> None:
        if self.current_cluster < len(self.clusters) - 1:
            self.current_cluster += 1
            self.view.load_and_display_images(self.clusters[self.current_cluster])
            self.view.current_group_label.config(text=f"{self.current_cluster + 1} / {len(self.clusters)}")

    def handle_previous_group_button_click(self, event=None) -> None:
        if self.current_cluster > 0:
            self.current_cluster -= 1
            self.view.load_and_display_images(self.clusters[self.current_cluster])
            self.view.current_group_label.config(text=f"{self.current_cluster + 1} / {len(self.clusters)}")

    def handle_select_folder_button_click(self, event=None) -> None:
        self.view.update_status_label("Selecting folder...")

        selected_folder_path = self.view.select_folder()

        if selected_folder_path == "":
            self.view.update_status_label("No folder selected!")
            return

        self.model.programManager.set_images_path(selected_folder_path)
        self.view.path_entry.config(highlightthickness=0)
        self.view.update_status_label("Folder selected!")

    def handle_run_button_click(self, event=None) -> None:
        
        if self.model.programManager.get_images_path() == "":
            self.view.path_entry.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            return

        self.view.update_status_label("Running...")
        self.model.run()
        
        # if self.counter < len(self.clusters):
        #     self.view.update_status_label(f"{len(self.clusters)} Groups found!")
        #     self.view.load_and_display_images(self.clusters[self.counter])
        #     self.counter += 1