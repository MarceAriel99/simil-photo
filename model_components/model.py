import sys

import numpy as np
from file_managers.config_file_manager import ConfigFileManager
import file_managers.file_searcher as file_searcher
import file_managers.cached_features_file_manager as cached_features_file_manager
from model_components.similarity_calculator import SimilarityCalculator

import numpy as np
import keras.utils as image
import cv2

from steps import Steps

# TODO: add constants for the config file parameters
# TODO: add exception checks everywhere
# TODO: add logging
# TODO: add comments
# TODO: add type hints

DEFAULT_CACHE_FILE_PATH = 'cached_features.csv'

class Model:
    def __init__(self) -> None:
        # Set default parameters, some of them will be updated with the config file if it exists

        self.images_path:str = ''
        self.check_subdirectories:bool = True
        self.cache_file_path:str = DEFAULT_CACHE_FILE_PATH
        self.feature_extraction_method:str = 'vgg16'
        self.selected_file_types:list[str] = ['.jpg', '.jpeg', '.png']
        self.clustering_method:str = 'affinity_propagation'
        self.feature_extraction_parameters:dict[str,any] = {}
        self.similarity_calculator:SimilarityCalculator = None

        self.images_ids_paths:dict[int,str] = {} #{id: absolute_path}
        self.images_clusters:list[list[int]] = []

        self.force_recalculate_features:bool = False
        self.save_calculated_features:bool = True

        self.configFileManager = ConfigFileManager()
        self._read_config_file()
        print("Model created")

    # TODO add exception checks if the config file is not valid, try to load the default values for each invalid parameter
    def _read_config_file(self): 
        images_path_in_file = self.configFileManager.get_config_parameter('paths', 'images_path')
        self.images_path = images_path_in_file if images_path_in_file != '' else self.images_path

        cache_file_path_in_file = self.configFileManager.get_config_parameter('paths', 'cache_file_path')
        self.cache_file_path = cache_file_path_in_file if cache_file_path_in_file != '' else self.cache_file_path

        self.feature_extraction_method = self.configFileManager.get_config_parameter('feature_extraction', 'method')
        self.selected_file_types = self.configFileManager.get_config_parameter('file_types', 'selected').split(',')
        self.all_file_types = self.configFileManager.get_config_parameter('file_types', 'supported').split(',')
        self.clustering_method = self.configFileManager.get_config_parameter('clustering', 'method')
        self.force_recalculate_features = True if self.configFileManager.get_config_parameter('cache', 'force_recalculate_features') == 'True' else False
        self.save_calculated_features = True if self.configFileManager.get_config_parameter('cache', 'save_calculated_features') == 'True' else False
        self.cached_features_method = self.configFileManager.get_config_parameter('cache', 'method')
        self.check_subdirectories = True if self.configFileManager.get_config_parameter('misc', 'check_subdirectories') == 'True' else False     

    def update_config_file(self):
        config_parameters = {}
        config_parameters['paths'] = {'images_path': self.images_path, 'cache_file_path': self.cache_file_path}
        config_parameters['misc'] = {'check_subdirectories': str(self.check_subdirectories)}
        config_parameters['file_types'] = {'selected': ','.join(self.selected_file_types)}
        config_parameters['feature_extraction'] = {'method': self.feature_extraction_method}
        config_parameters['clustering'] = {'method': self.clustering_method}
        config_parameters['cache'] = {'force_recalculate_features': str(self.force_recalculate_features), 
        'save_calculated_features': str(self.save_calculated_features), 
        'method': self.cached_features_method }
        self.configFileManager.set_config_parameters(config_parameters)

    def _set_feature_extraction_parameters(self, parameters:dict[str,any]={}):
        self.feature_extraction_parameters = parameters

    def set_file_types(self, file_types:list[str]):
        self.selected_file_types = file_types

    def get_selected_file_types(self) -> list[str]:
        return self.selected_file_types
    
    def get_all_file_types(self) -> list[str]:
        return self.all_file_types

    def set_feature_extraction_method(self, feature_extraction_method:str, parameters:dict[str,any]={}):
        self.feature_extraction_method = feature_extraction_method
        self._set_feature_extraction_parameters(parameters)

    def get_feature_extraction_method(self) -> str:
        return self.feature_extraction_method
    
    def set_clustering_method(self, clustering_method:str):
        self.clustering_method = clustering_method
    
    def set_images_path(self, images_path:str):
        self.images_path = images_path

    def get_images_path(self):
        return self.images_path

    def set_check_subdirectories(self, check_subdirectories:bool):
        self.check_subdirectories = check_subdirectories

    def get_check_subdirectories(self):
        return self.check_subdirectories

    def set_save_calculated_features(self, save_calculated_features:bool, cache_file_path:str=DEFAULT_CACHE_FILE_PATH):
        self.save_calculated_features = save_calculated_features
        self.cache_file_path = cache_file_path

    def get_save_calculated_features(self) -> bool:
        return self.save_calculated_features
    
    def set_force_recalculate_features(self, force_recalculate_features:bool):
        self.force_recalculate_features = force_recalculate_features

    def get_force_recalculate_features(self) -> bool:
        return self.force_recalculate_features

    def run(self, presenter):

        self.images_ids_paths = {}
        self.images_clusters = []

        presenter.step_started(Steps.search_images)

        # Search for images in path
        # TODO give option to search in a group of folders
        print(f"Searching for images in {self.images_path} with file types ({self.selected_file_types})")
        images_names_paths = file_searcher.file_search(self.images_path, tuple(self.selected_file_types), self.check_subdirectories)

        if len(images_names_paths) == 0:
            print(f"No images found in the specified path with file types ({self.selected_file_types})")
            presenter.run_completed()
            return

        # Create dictionary
        for (index, (image_name, image_path)) in enumerate(images_names_paths.items()):
            self.images_ids_paths[index] = f"{image_path}\\{image_name}"

        print("Walk completed")

        presenter.step_completed(Steps.search_images)

        # Load cached features
        # images_cached_features is a dict with {id: features} pairs
        # TODO Check if the features were calculated with the same parameters, if not, recalculate them
        print(f"Selected feature extraction method: {self.feature_extraction_method}")
        print(f"File saved feature extraction method: {self.configFileManager.get_config_parameter('cache', 'method')}")
        feature_extraction_method_changed:bool = self.feature_extraction_method != self.configFileManager.get_config_parameter('cache', 'method')
        if self.force_recalculate_features or feature_extraction_method_changed:
            print("Forcing recalculation of features")
            images_cached_features = {}       
        else:
            presenter.step_started(Steps.load_cached_features)
            images_cached_features = cached_features_file_manager.load_cached_features(self.images_ids_paths, self.cache_file_path)
            presenter.step_completed(Steps.load_cached_features)

        
        # Load images
        # images_pixel_data is a dict with {id: pixel_data} pairs (without cached features)
        presenter.step_started(Steps.load_images)

        images_pixel_data = {} 
        for (image_id, image_path) in self.images_ids_paths.items():
            if image_id in images_cached_features:
                continue
            img = image.load_img(image_path, target_size=(224, 224)) #TODO try other sizes
            img_data = image.img_to_array(img)
            images_pixel_data[image_id] = img_data

        presenter.step_completed(Steps.load_images)

        print(f"{len(images_pixel_data)} images loaded")
        print(f"{len(images_cached_features)} images did not need to be loaded")

        # Create SimilarityCalculator object
        similarity_calculator = SimilarityCalculator(images_pixel_data, images_cached_features, feature_extraction_method=self.feature_extraction_method)
        similarity_calculator.set_feature_extraction_parameters(self.feature_extraction_parameters)
        
        # Run similarity calculator
        presenter.step_started(Steps.calculate_features)
        similarity_calculator.run_feature_calculation()
        presenter.step_completed(Steps.calculate_features)

        presenter.step_started(Steps.calculate_clusters)
        self.images_clusters = similarity_calculator.run_cluster_calculation()
        presenter.step_completed(Steps.calculate_clusters)
        
        # Save features to cache file
        # If at least one image was loaded and the features need to be saved
        if self.save_calculated_features and len(images_pixel_data) > 0:
            print("Saving calculated features to cache file")
            presenter.step_started(Steps.cache_features)
            self.cached_features_method = self.feature_extraction_method
            images_paths_features:dict[str,np.array] = {}
            for (image_id, image_features) in similarity_calculator.get_normalized_features().items():
                images_paths_features[self.images_ids_paths.get(image_id)] = image_features
            
            cached_features_file_manager.save_cached_features(images_paths_features, self.cache_file_path, feature_extraction_method_changed)
            presenter.step_completed(Steps.cache_features)

        # Filter clusters with only one image
        self.images_clusters = list(filter(lambda cluster: len(cluster) > 1, self.images_clusters))
        presenter.run_completed()
    
    def get_clusters_paths(self) -> list[list[str]]:

        result = []

        for cluster in self.images_clusters:
            cluster_paths = []
            for image_id in cluster:
                cluster_paths.append(self.images_ids_paths[image_id])
            result.append(cluster_paths)

        return result