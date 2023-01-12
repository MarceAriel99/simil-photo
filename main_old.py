import sys

import numpy as np
from FilesManagers.config_file_manager import ConfigFileManager
import FilesManagers.file_searcher as file_searcher
import FilesManagers.cached_features_file_manager as cached_features_file_manager
from similarity_calculator import SimilarityCalculator

import numpy as np
import keras.utils as image
import cv2

# TODO: add constants for the config file parameters
# TODO: add exception checks everywhere
# TODO: add logging
# TODO: add comments
# TODO: add type hints

DEFAULT_CACHE_FILE_PATH = 'cached_features.csv'

class ProgramManager:

    def __init__(self):
        # Set default parameters, some of them will be updated with the config file if it exists

        self.images_path:str = ''
        self.cache_file_path:str = DEFAULT_CACHE_FILE_PATH
        self.feature_extraction_method:str = 'vgg16'
        self.file_types:list[str] = ['.jpg', '.jpeg', '.png']
        self.clustering_method:str = 'affinity_propagation'
        self.feature_extraction_parameters:dict[str,any] = {}
        self.similarity_calculator:SimilarityCalculator = None

        self.images_ids_paths:dict[int,str] = {} #{id: absolute_path}
        self.images_clusters:list[list[int]] = []

        self.force_recalculate_features:bool = False
        self.save_calculated_features:bool = True

        self.configFileManager = ConfigFileManager()
        self._read_config_file()

    # TODO add exception checks if the config file is not valid, try to load the default values for each invalid parameter
    def _read_config_file(self): 
        images_path_in_file = self.configFileManager.get_config_parameter('paths', 'images_path')
        self.images_path = images_path_in_file if images_path_in_file != '' else self.images_path

        cache_file_path_in_file = self.configFileManager.get_config_parameter('paths', 'cache_file_path')
        self.cache_file_path = cache_file_path_in_file if cache_file_path_in_file != '' else self.cache_file_path

        self.feature_extraction_method = self.configFileManager.get_config_parameter('feature_extraction', 'method')
        self.file_types = self.configFileManager.get_config_parameter('file_types', 'supported').split(',')
        self.clustering_method = self.configFileManager.get_config_parameter('clustering', 'method')
        self.force_recalculate_features = True if self.configFileManager.get_config_parameter('cache', 'force_recalculate_features') == 'True' else False
        self.save_calculated_features = True if self.configFileManager.get_config_parameter('cache', 'save_calculated_features') == 'True' else False

    def update_config_file(self):
        config_parameters = {}
        config_parameters['paths'] = {'images_path': self.images_path, 'cache_file_path': self.cache_file_path}
        config_parameters['file_types'] = {'supported': ','.join(self.file_types)}
        config_parameters['feature_extraction'] = {'method': self.feature_extraction_method}
        config_parameters['clustering'] = {'method': self.clustering_method}
        config_parameters['cache'] = {'force_recalculate_features': str(self.force_recalculate_features), 'save_calculated_features': str(self.save_calculated_features)}
        self.configFileManager.set_config_parameters(config_parameters)

    def _set_feature_extraction_parameters(self, parameters:dict[str,any]={}):
        self.feature_extraction_parameters = parameters

    def set_file_types(self, file_types:list[str]):
        self.file_types = file_types

    def set_feature_extraction_method(self, feature_extraction_method:str, parameters:dict[str,any]={}):
        self.feature_extraction_method = feature_extraction_method
        self._set_feature_extraction_parameters(parameters)
    
    def set_clustering_method(self, clustering_method:str):
        self.clustering_method = clustering_method
    
    def set_images_path(self, images_path:str):
        self.images_path = images_path

    def set_save_calculated_features(self, save_calculated_features:bool, cache_file_path:str=DEFAULT_CACHE_FILE_PATH):
        self.save_calculated_features = save_calculated_features
        self.cache_file_path = cache_file_path
    
    def set_force_recalculate_features(self, force_recalculate_features:bool):
        self.force_recalculate_features = force_recalculate_features

    def run(self):
        # Search for images in path
        # TODO give option to search in a group of folders
        images_names_paths = file_searcher.file_search(self.images_path, tuple(self.file_types), False)

        if len(images_names_paths) == 0:
            print(f"No images found in the specified path with file types ({self.file_types})")
            return

        # Create dictionary
        for (index, (image_name, image_path)) in enumerate(images_names_paths.items()):
            self.images_ids_paths[index] = f"{image_path}\{image_name}"

        # Load cached features
        # images_cached_features is a dict with {id: features} pairs
        # TODO Check if the features were calculated with the same parameters, if not, recalculate them
        feature_extraction_method_changed:bool = self.feature_extraction_method != self.configFileManager.get_config_parameter('feature_extraction', 'method')
        if self.force_recalculate_features or feature_extraction_method_changed:
            print("Forcing recalculation of features")
            images_cached_features = {}       
        else:
            images_cached_features = cached_features_file_manager.load_cached_features(self.images_ids_paths, self.cache_file_path)
            
        # Load images
        # images_pixel_data is a dict with {id: pixel_data} pairs (without precalculated features)
        images_pixel_data = {} 
        for (image_id, image_path) in self.images_ids_paths.items():
            if image_id in images_cached_features:
                continue
            img = image.load_img(image_path, target_size=(224, 224)) #TODO try other sizes
            img_data = image.img_to_array(img)
            images_pixel_data[image_id] = img_data

        print(f"{len(images_pixel_data)} images loaded")
        print(f"{len(images_cached_features)} images did not need to be loaded")
        
        # Create SimilarityCalculator object
        similarity_calculator = SimilarityCalculator(images_pixel_data, images_cached_features, feature_extraction_method=self.feature_extraction_method)
        similarity_calculator.set_feature_extraction_parameters(self.feature_extraction_parameters)

        # Run similarity calculator
        self.images_clusters = similarity_calculator.run()

        # Save features to cache file
        # If at least one image was loaded and the features need to be saved
        if self.save_calculated_features and len(images_pixel_data) > 0:
            print("Saving calculated features to cache file")
            images_paths_features:dict[str,np.array] = {}
            for (image_id, image_features) in similarity_calculator.get_normalized_features().items():
                images_paths_features[self.images_ids_paths.get(image_id)] = image_features
            
            cached_features_file_manager.save_cached_features(images_paths_features, self.cache_file_path, feature_extraction_method_changed)

        # Filter clusters with only one image
        self.images_clusters = list(filter(lambda cluster: len(cluster) > 1, self.images_clusters))


def main(images_path):

    programManager = ProgramManager()

    programManager.set_images_path(images_path)
    programManager.set_file_types(['.jpg', '.png', '.jpeg', '.webp'])
    programManager.set_save_calculated_features(True)
    programManager.set_force_recalculate_features(False)
    programManager.set_feature_extraction_method('mobilenet')
    #programManager.set_feature_extraction_method('vgg16')
    #programManager.set_feature_extraction_method('color_distribution', {'color_bins': 3})
    

    # This shoud be done when the user selects all parameters and presses the "Run" button
    programManager.run()

    images_ids_paths = programManager.images_ids_paths
    images_clusters = programManager.images_clusters

    programManager.update_config_file()

    # For each cluster, print the images
    for cluster in images_clusters:
        cluster_list = []
        for image_id in cluster:
            img = cv2.imread(images_ids_paths.get(image_id))
            if img is None: # TODO check how to handle files with non ascii characters (rename them?)
                continue
            img = cv2.resize(img, (img.shape[1] // 5, img.shape[0] // 5))
            cluster_list.append(img)
            print(images_ids_paths.get(image_id).split("\\")[-1])
        try:
            Hori = np.concatenate(cluster_list, axis=1)
            cv2.imshow('HORIZONTAL', Hori)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print("-------------------------------")
        except ValueError:
            print("Error concatenating images")
            continue

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python main.py <path to images>")
        sys.exit(1)
    
    main(sys.argv[1])