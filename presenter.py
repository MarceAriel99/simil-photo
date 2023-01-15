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
        model_images_path = self.model.get_images_path()
        folder_path_entry = model_images_path if model_images_path else "No folder selected"
        self.view.update_folder_path_entry(folder_path_entry)
        self.view.subdirectories_checkbox.select() if self.model.get_check_subdirectories() else self.view.subdirectories_checkbox.deselect()
        # TODO make this scalable and not hardcoded
        self.view.jpg_checkbox.select() if ".jpg" in self.model.get_file_types() else self.view.jpg_checkbox.deselect()
        self.view.png_checkbox.select() if ".png" in self.model.get_file_types() else self.view.png_checkbox.deselect()
        self.view.jpeg_checkbox.select() if ".jpeg" in self.model.get_file_types() else self.view.jpeg_checkbox.deselect()
        self.view.webp_checkbox.select() if ".webp" in self.model.get_file_types() else self.view.webp_checkbox.deselect()
        
    def _apply_config_to_model(self) -> None:
        #These parameters should be read from the view
        self.model.set_images_path(self.view.path_entry.get())
        self.model.set_check_subdirectories(self.view.check_subdirectories_var.get())
        self.model.set_file_types(["."+file_type_name for file_type_name, value in self.view.file_types_variables.items() if value.get()])
        self.model.set_save_calculated_features(True)
        self.model.set_force_recalculate_features(False)
        self.model.set_feature_extraction_method('mobilenet')

    def run(self) -> None:
        print("Presenter running")
        self.view.init_ui(self)
        self._update_view_with_saved_data()
        self.view.mainloop()

    def run_completed(self) -> None:
        self.current_cluster = 0
        self.clusters = self.model.get_clusters_paths()
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

        self.view.path_entry.config(highlightthickness=0)
        self.view.update_status_label("Folder selected!")

    def handle_run_button_click(self, event=None) -> None:
        
        if self.model.get_images_path() == "":
            self.view.path_entry.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            return

        self._apply_config_to_model()
        self.model.update_config_file() 

        self.view.update_status_label("Running...")
        self.model.run(self)