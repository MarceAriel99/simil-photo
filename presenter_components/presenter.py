import os

from model_components.model import Model
from view_components.view import View

from steps import Steps
import timeit

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
        # POSSIBLE UPGRADE should access through a method to change the state of the checkbox
        self.view.config_panel.subdirectories_checkbox.state(['selected']) if self.model.get_check_subdirectories() else self.view.config_panel.subdirectories_checkbox.state(['!selected'])

        # Update file types checkboxes
        for file_type in self.model.get_all_file_types():
            if file_type in self.model.get_selected_file_types():
                self.view.config_panel.file_types_variables[file_type[1:]].set(True)
            else:
                self.view.config_panel.file_types_variables[file_type[1:]].set(False)

        # Update feature extraction method selection
        feature_extraction_methods = self.model.get_all_feature_extraction_methods()
        self.view.config_panel.select_feature_extraction_method(feature_extraction_methods.index(self.model.get_feature_extraction_method()))
        self.view.config_panel.cache_features_checkbox.state(['selected']) if self.model.get_save_calculated_features() else self.view.config_panel.cache_features_checkbox.state(['!selected'])
        self.view.config_panel.force_recalculate_features_checkbox.state(['selected']) if self.model.get_force_recalculate_features() else self.view.config_panel.force_recalculate_features_checkbox.state(['!selected'])
        
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

    def run_completed(self, stopped:bool=False) -> None:
        self.current_cluster = 0
        self.clusters = self.model.get_clusters_paths()
        self.view.update_status_label(f"{len(self.clusters)} Groups found!")
        self.view.empty_grid()

        self.end = timeit.default_timer()

        total_time = (self.end - self.start)

        if total_time < 1:
            time_label = f"Process completed in {int(total_time * 1000)} milisecond" + ("s" if int(total_time * 1000) > 1 else "")
        elif total_time < 60:
            time_label = f"Process completed in {int(total_time)} second" + ("s" if int(total_time) > 1 else "")
        else:
            time_label = f"Process completed in {int(total_time // 60)} minute" + ("s" if int(total_time // 60) > 1 else "") + f" and {int(total_time % 60)} second" + ("s" if int(total_time % 60) > 1 else "")

        if stopped:
            self.add_message_to_queue(("STARTED_STEP", "Process stopped!"))
        else:
            self.add_message_to_queue(("STARTED_STEP", time_label))

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
            self.view.incorrect_path()
            return

        self.view.set_path_entry_highlight(False)
        self._apply_config_to_model() 
        self.view.config_panel.progress_bar["value"] = 0
        self.start = timeit.default_timer()
        self.model.run(self)

    def add_message_to_queue(self, message: Steps) -> None:
        self.view.add_message_to_queue(message)

    def handle_delete_button_click(self, path: str) -> None:
        # Should be done by model?
        print("Deleting", path)
        try:
            os.remove(path)
            self.clusters[self.current_cluster].remove(path) # Remove from current cluster so it doesn't get displayed again
        except Exception as e:
            print(e)

    def handle_open_button_click(self, path: str) -> None:
        # Should be done by model?
        print("Opening", path)
        try:
            os.startfile(path)
        except Exception as e:
            print(e)

    def get_feature_extraction_methods(self) -> list[str]:
        return self.model.get_all_feature_extraction_methods()