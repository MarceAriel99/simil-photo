import os
from model_components.model import Model
from view_components.view import View
from steps import Steps

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
        self.view.update_path_entry(folder_path_entry)
        # TODO should access through a method to change the state of the checkbox
        self.view.config_panel.subdirectories_checkbox.select() if self.model.get_check_subdirectories() else self.view.config_panel.subdirectories_checkbox.deselect()
        # TODO make this scalable and not hardcoded
        self.view.config_panel.jpg_checkbox.select() if ".jpg" in self.model.get_file_types() else self.view.config_panel.jpg_checkbox.deselect()
        self.view.config_panel.png_checkbox.select() if ".png" in self.model.get_file_types() else self.view.config_panel.png_checkbox.deselect()
        self.view.config_panel.jpeg_checkbox.select() if ".jpeg" in self.model.get_file_types() else self.view.config_panel.jpeg_checkbox.deselect()
        self.view.config_panel.webp_checkbox.select() if ".webp" in self.model.get_file_types() else self.view.config_panel.webp_checkbox.deselect()

        # TODO make this scalable and not hardcoded
        items = ['vgg16', 'mobilenet', 'color_histogram']
        self.view.config_panel.select_feature_extraction_method(items.index(self.model.get_feature_extraction_method()))
        self.view.config_panel.cache_features_checkbox.select() if self.model.get_save_calculated_features() else self.view.config_panel.cache_features_checkbox.deselect()
        self.view.config_panel.force_recalculate_features_checkbox.select() if self.model.get_force_recalculate_features() else self.view.config_panel.force_recalculate_features_checkbox.deselect()
        
    def _apply_config_to_model(self) -> None:
        self.model.set_images_path(self.view.get_images_path())
        self.model.set_check_subdirectories(self.view.get_subdirectories_checkbox_state())
        self.model.set_file_types(["." + file_type_name for file_type_name, value in self.view.get_file_types_variables().items() if value.get()])
        self.model.set_feature_extraction_method(self.view.get_selected_feature_extraction_method())
        self.model.set_save_calculated_features(self.view.get_cache_features_checkbox_state())
        self.model.set_force_recalculate_features(self.view.get_force_recalculate_features_checkbox_state())
        
    def run(self) -> None:
        print("Presenter running")
        self.view.init_ui(self)
        self._update_view_with_saved_data()
        self.view.mainloop()

    def run_completed(self) -> None:
        self.current_cluster = 0
        self.clusters = self.model.get_clusters_paths()
        self.view.update_status_label(f"{len(self.clusters)} Groups found!")
        self.view.empty_grid()

        self.add_message_to_queue(("STARTED_STEP", "Done!"))
        self.add_message_to_queue(("COMPLETED_STEP", 100))
        
        if len(self.clusters) == 0:
            self.view.change_group_frame_visibility(False)
            return

        self.view.change_group_frame_visibility(True)
        self.view.update_current_group_label(self.current_cluster, len(self.clusters))
        self.view.load_and_display_images(self.clusters[self.current_cluster])
        self.model.update_config_file()

    def step_started(self, step: Steps) -> None:

        if step == Steps.search_images:
            self.add_message_to_queue(("STARTED_STEP", "Searching images..."))
        elif step == Steps.load_cached_features:
            self.add_message_to_queue(("STARTED_STEP", "Loading cached features..."))
        elif step == Steps.load_images:
            self.add_message_to_queue(("STARTED_STEP", "Loading images..."))
        elif step == Steps.calculate_features:
            self.add_message_to_queue(("STARTED_STEP", "Calculating features..."))
        elif step == Steps.calculate_clusters:
            self.add_message_to_queue(("STARTED_STEP", "Calculating clusters..."))
        elif step == Steps.cache_features:
            self.add_message_to_queue(("STARTED_STEP", "Caching features..."))

    def step_completed(self, step: Steps) -> None:
        
        if step == Steps.search_images:
            self.add_message_to_queue(("COMPLETED_STEP", 5))
        elif step == Steps.load_cached_features:
            self.add_message_to_queue(("COMPLETED_STEP", 20))
        elif step == Steps.load_images:
            self.add_message_to_queue(("COMPLETED_STEP", 40))
        elif step == Steps.calculate_features:
            self.add_message_to_queue(("COMPLETED_STEP", 70))
        elif step == Steps.calculate_clusters:
            self.add_message_to_queue(("COMPLETED_STEP", 80))
        elif step == Steps.cache_features:
            self.add_message_to_queue(("COMPLETED_STEP", 95))

    def handle_next_group_button_click(self, event=None) -> None:
        if self.current_cluster < len(self.clusters) - 1:
            self.current_cluster += 1
            self.view.load_and_display_images(self.clusters[self.current_cluster])
            self.view.top_bar.current_group_label.config(text=f"{self.current_cluster + 1} / {len(self.clusters)}")

    def handle_previous_group_button_click(self, event=None) -> None:
        if self.current_cluster > 0:
            self.current_cluster -= 1
            self.view.load_and_display_images(self.clusters[self.current_cluster])
            self.view.top_bar.current_group_label.config(text=f"{self.current_cluster + 1} / {len(self.clusters)}")

    def handle_select_folder_button_click(self, event=None) -> None:
        self.view.update_status_label("Selecting folder...")

        selected_folder_path = self.view.select_folder()

        if selected_folder_path == "":
            self.view.update_status_label("No folder selected!")
            return

        self.view.set_path_entry_highlight(False)
        self.view.update_status_label("Folder selected!")

    def handle_run_button_click(self, event=None) -> None:
        
        if not os.path.isdir(self.view.get_images_path()):
            self.view.set_path_entry_highlight(True)
            return

        self.view.set_path_entry_highlight(False)

        self._apply_config_to_model() 

        self.view.config_panel.progress_bar["value"] = 0

        self.model.run(self)

    def add_message_to_queue(self, message: Steps) -> None:
        self.view.add_message_to_queue(message)