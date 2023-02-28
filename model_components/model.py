import sys

import numpy as np
from file_managers.config_file_manager import ConfigFileManager
import file_managers.file_searcher as file_searcher
import file_managers.cached_features_file_manager as cached_features_file_manager
from model_components.similarity_calculator import SimilarityCalculator

import numpy as np
import keras.utils as image
import cv2

from view_components.stoppable_thread import StoppableThread, current_thread

from steps import Steps
from constants import *

# TODO: add logging
class Model:
    def __init__(self) -> None:
        # Set default parameters, some of them will be updated with the config file if it exists

        self.images_path:str = ''
        self.check_subdirectories:bool = True
        self.cache_file_path:str = PATH_DEFAULT_CACHE_FILE
        self.selected_feature_extraction_method:str = CONFIG_DEFAULT_VALUE_SELECTED_FEATURE_EXTRACTION_METHOD
        self.selected_file_types:list[str] = CONFIG_DEFAULT_VALUE_SELECTED_FILE_TYPES
        self.clustering_method:str = CONFIG_DEFAULT_VALUE_CLUSTERING_METHOD
        self.feature_extraction_parameters:dict[str,any] = {}
        self.similarity_calculator:SimilarityCalculator = None

        self.images_ids_paths:dict[int,str] = {} #{id: absolute_path}
        self.images_clusters:list[list[int]] = []

        self.force_recalculate_features:bool = CONFIG_DEFAULT_VALUE_CACHE_FORCE_RECALCULATE_FEATURES
        self.save_calculated_features:bool = CONFIG_DEFAULT_VALUE_CACHE_SAVE_CALCULATED_FEATURES

        self.configFileManager = ConfigFileManager()
        self._read_config_file()
        print("Model created")

    # Read the config file and update the parameters
    def _read_config_file(self) -> None: 
        images_path_in_file = self.configFileManager.get_config_parameter(CONFIG_SECTION_PATHS, CONFIG_PARAMETER_IMAGES_PATH)
        self.images_path = images_path_in_file if images_path_in_file != '' else self.images_path

        cache_file_path_in_file = self.configFileManager.get_config_parameter(CONFIG_SECTION_PATHS, CONFIG_PARAMETER_CACHE_FILE_PATH)
        self.cache_file_path = cache_file_path_in_file if cache_file_path_in_file != '' else self.cache_file_path

        self.selected_feature_extraction_method = self.configFileManager.get_config_parameter(CONFIG_SECTION_FEATURE_EXTRACTION, CONFIG_PARAMETER_SELECTED_FEATURE_EXTRACTION_METHOD)
        self.all_feature_extraction_methods = self.configFileManager.get_config_parameter(CONFIG_SECTION_FEATURE_EXTRACTION, CONFIG_PARAMETER_SUPPORTED_FEATURE_EXTRACTION_METHOD).split(',')

        self.selected_file_types = self.configFileManager.get_config_parameter(CONFIG_SECTION_FILE_TYPES, CONFIG_PARAMETER_SELECTED_FILE_TYPES).split(',')
        self.all_file_types = self.configFileManager.get_config_parameter(CONFIG_SECTION_FILE_TYPES, CONFIG_PARAMETER_SUPPORTED_FILE_TYPES).split(',')

        self.clustering_method = self.configFileManager.get_config_parameter(CONFIG_SECTION_CLUSTERING, CONFIG_PARAMETER_CLUSTERING_METHOD)

        self.force_recalculate_features = True if self.configFileManager.get_config_parameter(CONFIG_SECTION_CACHE, CONFIG_PARAMETER_CACHE_FORCE_RECALCULATE_FEATURES) == 'True' else False
        self.save_calculated_features = True if self.configFileManager.get_config_parameter(CONFIG_SECTION_CACHE, CONFIG_PARAMETER_CACHE_SAVE_CALCULATED_FEATURES) == 'True' else False
        self.cached_features_method = self.configFileManager.get_config_parameter(CONFIG_SECTION_CACHE, CONFIG_PARAMETER_CACHE_FEATURE_EXTRACTION_METHOD)

        self.check_subdirectories = True if self.configFileManager.get_config_parameter(CONFIG_SECTION_MISC, CONFIG_PARAMETER_MISC_CHECK_SUBDIRECTORIES) == 'True' else False     

    # Update the config file with the current parameters
    def update_config_file(self) -> None:
        config_parameters = {}
        
        config_parameters[CONFIG_SECTION_PATHS] = {CONFIG_PARAMETER_IMAGES_PATH: self.images_path, 
                                                   CONFIG_PARAMETER_CACHE_FILE_PATH: self.cache_file_path}
        
        config_parameters[CONFIG_SECTION_FEATURE_EXTRACTION] = {CONFIG_PARAMETER_SELECTED_FEATURE_EXTRACTION_METHOD: self.selected_feature_extraction_method}

        config_parameters[CONFIG_SECTION_FILE_TYPES] = {CONFIG_PARAMETER_SELECTED_FILE_TYPES: ','.join(self.selected_file_types)}

        config_parameters[CONFIG_SECTION_CLUSTERING] = {CONFIG_PARAMETER_CLUSTERING_METHOD: self.clustering_method}

        config_parameters[CONFIG_SECTION_CACHE] = {CONFIG_PARAMETER_CACHE_FORCE_RECALCULATE_FEATURES: str(self.force_recalculate_features), 
        CONFIG_PARAMETER_CACHE_SAVE_CALCULATED_FEATURES: str(self.save_calculated_features), 
        CONFIG_PARAMETER_CACHE_FEATURE_EXTRACTION_METHOD: self.cached_features_method }

        config_parameters[CONFIG_SECTION_MISC] = {CONFIG_PARAMETER_MISC_CHECK_SUBDIRECTORIES: str(self.check_subdirectories)}

        self.configFileManager.set_config_parameters(config_parameters)

    def _set_feature_extraction_parameters(self, parameters:dict[str,any]={}) -> None:
        self.feature_extraction_parameters = parameters

    def set_file_types(self, file_types:list[str]) -> None:
        self.selected_file_types = file_types

    def get_selected_file_types(self) -> list[str]:
        return self.selected_file_types
    
    def get_all_file_types(self) -> list[str]:
        return self.all_file_types

    def set_feature_extraction_method(self, feature_extraction_method:str, parameters:dict[str,any]={}) -> None:
        self.selected_feature_extraction_method = feature_extraction_method
        self._set_feature_extraction_parameters(parameters)

    def get_feature_extraction_method(self) -> str:
        return self.selected_feature_extraction_method
    
    def get_all_feature_extraction_methods(self) -> list[str]:
        return self.all_feature_extraction_methods
    
    def set_clustering_method(self, clustering_method:str) -> None:
        self.clustering_method = clustering_method
    
    def set_images_path(self, images_path:str) -> None:
        self.images_path = images_path

    def get_images_path(self) -> str:
        return self.images_path

    def set_check_subdirectories(self, check_subdirectories:bool) -> None:
        self.check_subdirectories = check_subdirectories

    def get_check_subdirectories(self) -> bool:
        return self.check_subdirectories

    def set_save_calculated_features(self, save_calculated_features:bool, cache_file_path:str=PATH_DEFAULT_CACHE_FILE):
        self.save_calculated_features = save_calculated_features
        self.cache_file_path = cache_file_path

    def get_save_calculated_features(self) -> bool:
        return self.save_calculated_features
    
    def set_force_recalculate_features(self, force_recalculate_features:bool) -> None:
        self.force_recalculate_features = force_recalculate_features

    def get_force_recalculate_features(self) -> bool:
        return self.force_recalculate_features

    def run(self, presenter) -> None:
        
        # Get current thread
        thread = current_thread()

        self.images_ids_paths = {}
        self.images_clusters = []

        presenter.step_started(Steps.search_images)

        # Search for images in path (POSSIBLE UPGRADE give option to search in a group of folders)
        print(f"Searching for images in {self.images_path} with file types ({self.selected_file_types})")
        images_names_paths = file_searcher.file_search(self.images_path, tuple(self.selected_file_types), self.check_subdirectories)

        # If no images were found, stop the execution
        if len(images_names_paths) == 0:
            print(f"No images found in the specified path with file types ({self.selected_file_types})")
            presenter.run_completed()
            return

        # Create dictionary with {id: path} pairs
        for (index, (image_name, image_path)) in enumerate(images_names_paths.items()):
            self.images_ids_paths[index] = f"{image_path}\\{image_name}"

        print("Walk completed")

        presenter.step_completed(Steps.search_images)

        # Load cached features
        # images_cached_features is a dict with {id: features} pairs

        # POSSIBLE UPGRADE: Check if the features were calculated with the same parameters, if not, recalculate them 
        # (Currently it doesn't make sense because the user cannot change the parameters)
        print(f"Selected feature extraction method: {self.selected_feature_extraction_method}")
        print(f"File saved feature extraction method: {self.configFileManager.get_config_parameter('cache', 'method')}")

        feature_extraction_method_changed:bool = self.selected_feature_extraction_method != self.configFileManager.get_config_parameter('cache', 'method')
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

            # Check if thread was stopped while loading images
            if thread.stopped():
                presenter.run_completed(True)
                return
            
            if image_id in images_cached_features:
                continue

            img = image.load_img(image_path, target_size=(224, 224))
            img_data = image.img_to_array(img)
            images_pixel_data[image_id] = img_data

        presenter.step_completed(Steps.load_images)

        print(f"{len(images_pixel_data)} images loaded")
        print(f"{len(images_cached_features)} images did not need to be loaded")

        # Create SimilarityCalculator object
        similarity_calculator = SimilarityCalculator(images_pixel_data, images_cached_features, feature_extraction_method=self.selected_feature_extraction_method)
        # Set feature extraction parameters
        similarity_calculator.set_feature_extraction_parameters(self.feature_extraction_parameters)
        
        # Run similarity calculator
        presenter.step_started(Steps.calculate_features)

        similarity_calculator.run_feature_calculation(thread)

        # Check if thread was stopped while calculating features
        if thread.stopped():
            presenter.run_completed(True)
            return

        presenter.step_completed(Steps.calculate_features)
        presenter.step_started(Steps.calculate_clusters)
        
        self.images_clusters = similarity_calculator.run_cluster_calculation()
        presenter.step_completed(Steps.calculate_clusters)

        # Check if thread was stopped while calculating clusters
        if thread.stopped():
            self.images_clusters = []
            presenter.run_completed(True)
            return
        
        # Save features to cache file
        # If the user has selected to save the calculated features, and there are images to save
        if self.save_calculated_features and len(images_pixel_data) > 0:
            print("Saving calculated features to cache file")
            presenter.step_started(Steps.cache_features)
        
            self.cached_features_method = self.selected_feature_extraction_method
            images_paths_features:dict[str,np.array] = {}
            for (image_id, image_features) in similarity_calculator.get_normalized_features().items():
                images_paths_features[self.images_ids_paths.get(image_id)] = image_features
            
            cached_features_file_manager.save_cached_features(images_paths_features, self.cache_file_path, feature_extraction_method_changed)
            presenter.step_completed(Steps.cache_features)

        # Filter clusters with only one image
        self.images_clusters = list(filter(lambda cluster: len(cluster) > 1, self.images_clusters))

        # Call presenter to show results
        presenter.run_completed()
    
    # Return a list of clusters, each cluster is a list of image paths
    def get_clusters_paths(self) -> list[list[str]]:

        result = []

        for cluster in self.images_clusters:
            cluster_paths = []
            for image_id in cluster:
                cluster_paths.append(self.images_ids_paths[image_id])
            result.append(cluster_paths)

        return result