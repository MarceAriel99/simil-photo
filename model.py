from main_old import ProgramManager

class Model:
    def __init__(self) -> None:
        print("Model created")
        
        self.programManager = ProgramManager()

        images_path = "..\Images"

        self.programManager.set_images_path(images_path)
        self.programManager.set_file_types(['.jpg', '.png', '.jpeg', '.webp'])
        self.programManager.set_save_calculated_features(True)
        self.programManager.set_force_recalculate_features(False)
        self.programManager.set_feature_extraction_method('mobilenet')
    
    def run(self) -> None:
        print("Model running")
        self.programManager.run()

        self.images_ids_paths = self.programManager.images_ids_paths
        self.images_clusters = self.programManager.images_clusters

    def get_images_paths(self) -> list[list[str]]:

        result = []

        for cluster in self.images_clusters:
            cluster_paths = []
            for image_id in cluster:
                cluster_paths.append(self.images_ids_paths[image_id])
            result.append(cluster_paths)

        return result