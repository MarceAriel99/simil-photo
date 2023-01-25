import os
from ModelComponents.model import Model
from ViewComponents.view import View

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
        # TODO should ask not access?
        self.view.config_panel.subdirectories_checkbox.select() if self.model.get_check_subdirectories() else self.view.config_panel.subdirectories_checkbox.deselect()
        # TODO make this scalable and not hardcoded
        self.view.config_panel.jpg_checkbox.select() if ".jpg" in self.model.get_file_types() else self.view.config_panel.jpg_checkbox.deselect()
        self.view.config_panel.png_checkbox.select() if ".png" in self.model.get_file_types() else self.view.config_panel.png_checkbox.deselect()
        self.view.config_panel.jpeg_checkbox.select() if ".jpeg" in self.model.get_file_types() else self.view.config_panel.jpeg_checkbox.deselect()
        self.view.config_panel.webp_checkbox.select() if ".webp" in self.model.get_file_types() else self.view.config_panel.webp_checkbox.deselect()
        self.view.config_panel.cache_features_checkbox.select() if self.model.get_save_calculated_features() else self.view.config_panel.cache_features_checkbox.deselect()
        self.view.config_panel.force_recalculate_features_checkbox.select() if self.model.get_force_recalculate_features() else self.view.config_panel.force_recalculate_features_checkbox.deselect()
        
    def _apply_config_to_model(self) -> None:
        self.model.set_images_path(self.view.config_panel.path_entry.get())
        self.model.set_check_subdirectories(self.view.config_panel.subdirectories_var.get())
        self.model.set_file_types(["."+file_type_name for file_type_name, value in self.view.config_panel.file_types_variables.items() if value.get()])
        #All parameters should be read from the view
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
        self.view.empty_grid()
        
        if len(self.clusters) == 0:
            self.view.change_group_frame_visibility(False)
            return

        self.view.change_group_frame_visibility(True)
        self.view.update_current_group_label(self.current_cluster, len(self.clusters))
        self.view.load_and_display_images(self.clusters[self.current_cluster])

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

    def on_feature_extraction_method_selected(self, event=None) -> None:
        # This should be done in view, because I need Tk to update the text box. Should be a method in view
        self.view.config_panel.feature_extraction_textbox.config(state='normal')
        self.view.config_panel.feature_extraction_textbox.delete('1.0', 'end')
        self.view.config_panel.feature_extraction_textbox.insert('end', "Description of: " + self.view.config_panel.feature_extraction_listbox.get(self.view.config_panel.feature_extraction_listbox.curselection()[0]))
        self.view.config_panel.feature_extraction_textbox.config(state='disabled')

    def handle_select_folder_button_click(self, event=None) -> None:
        self.view.update_status_label("Selecting folder...")

        selected_folder_path = self.view.select_folder()

        if selected_folder_path == "":
            self.view.update_status_label("No folder selected!")
            return

        self.view.config_panel.path_entry.config(highlightthickness=0)
        self.view.update_status_label("Folder selected!")

    def handle_run_button_click(self, event=None) -> None:

        if not os.path.isdir(self.view.config_panel.path_entry.get()):
            self.view.config_panel.path_entry.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
            return

        self.view.config_panel.path_entry.config(highlightthickness=0)

        self._apply_config_to_model()
        self.model.update_config_file() 

        self.view.update_status_label("Running...")
        self.model.run(self)