from __future__ import annotations

import logging
logging.basicConfig(filename='run.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s')

import numpy as np
from file_managers.config_file_manager import ConfigFileManager
import file_managers.file_searcher as file_searcher
import file_managers.cached_features_file_manager as cached_features_file_manager
from model_components.similarity_calculator import SimilarityCalculator

import numpy as np
import keras.utils as image
from PIL import Image

from view_components.stoppable_thread import StoppableThread, current_thread

from steps import Steps
from constants import *

import psutil

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from presenter_components.presenter import Presenter

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
        
        self.memory_usage_limit:int = int(CONFIG_DEFAULT_VALUE_MISC_MEMORY_USAGE_LIMIT)

        self.configFileManager = ConfigFileManager()
        try:
            self._read_config_file()
        except Exception as e:
            logging.error('Error reading config file: ' + str(e))
            logging.info('Creating new config file')
            self.configFileManager.create_config_file()
            
        logging.debug('Model initialized')

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
        self.memory_usage_limit = int(self.configFileManager.get_config_parameter(CONFIG_SECTION_MISC, CONFIG_PARAMETER_MISC_MEMORY_USAGE_LIMIT))

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
        config_parameters[CONFIG_SECTION_MISC] = {CONFIG_PARAMETER_MISC_MEMORY_USAGE_LIMIT: str(self.memory_usage_limit)}

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

    def run(self, presenter:Presenter) -> None:

        logging.info("Starting execution")
        
        # Get current thread
        thread:StoppableThread = current_thread()
        self.presenter = presenter

        self.images_ids_paths = {}
        self.images_clusters = []

        self.presenter.step_started(Steps.search_images)

        # Search for images in path (POSSIBLE UPGRADE give option to search in a group of folders)
        logging.info(f"Searching for images in {self.images_path} with file types ({self.selected_file_types})")
        self.images_ids_paths = file_searcher.file_search(self.images_path, tuple(self.selected_file_types), self.check_subdirectories)

        # If no images were found, stop the execution
        if len(self.images_ids_paths) == 0:
            logging.info(f"No images found in the specified path with file types ({self.selected_file_types}), stopping execution")
            self.presenter.run_completed(False, "No images found")
            return
        
        self.presenter.step_completed(Steps.search_images)

        logging.info(f"Found {len(self.images_ids_paths)} images")

        # Ignore images that cannot be opened from images_ids_paths
        self.presenter.step_started(Steps.verify_images)
        ignored_images_count = len(self.images_ids_paths)
        self.images_ids_paths = self._delete_unverified_images(self.images_ids_paths, thread)
        ignored_images_count -= len(self.images_ids_paths)
        self.presenter.step_completed(Steps.verify_images)
        
        # Load cached features
        # images_cached_features is a dict with {id: features} pairs

        # POSSIBLE UPGRADE: Check if the features were calculated with the same parameters, if not, recalculate them 
        # (Currently it doesn't make sense because the user cannot change the parameters)
        logging.info(f"Currently selected feature extraction method: {self.selected_feature_extraction_method}")
        logging.info(f"File saved feature extraction method: {self.configFileManager.get_config_parameter('cache', 'method')}")

        feature_extraction_method_changed:bool = self.selected_feature_extraction_method != self.configFileManager.get_config_parameter('cache', 'method')
        if self.force_recalculate_features or feature_extraction_method_changed:
            logging.info("Forcing recalculation of features")
            images_cached_features = {}       
        else:
            self.presenter.step_started(Steps.load_cached_features)
            images_cached_features = cached_features_file_manager.load_cached_features(self.images_ids_paths, self.cache_file_path)
            self.presenter.step_completed(Steps.load_cached_features)

        # Load images
        # images_pixel_data is a dict with {id: pixel_data} pairs (without cached features)
        self.presenter.step_started(Steps.load_images)

        images_pixel_data = {}
        for (image_id, image_path) in self.images_ids_paths.items():

            # Check if thread was stopped while loading images
            if thread.stopped():
                if not thread.close_window:
                    self.presenter.run_completed(True)
                return
            
            # Check memory usage
            if self.memory_usage_over_limit(thread):
                return

            if image_id in images_cached_features:
                continue

            img = image.load_img(image_path, target_size=(224, 224))

            img_data = image.img_to_array(img)
            images_pixel_data[image_id] = img_data

            self.step_progress(Steps.load_images, len(images_pixel_data), len(self.images_ids_paths))

        self.presenter.step_completed(Steps.load_images)

        logging.info(f"{len(images_pixel_data)} images loaded")
        logging.info(f"{len(images_cached_features)} images features loaded from cache")

        # Create SimilarityCalculator object
        similarity_calculator = SimilarityCalculator(images_pixel_data, images_cached_features, feature_extraction_method=self.selected_feature_extraction_method)
        # Set feature extraction parameters
        similarity_calculator.set_feature_extraction_parameters(self.feature_extraction_parameters)
        
        # Run similarity calculator
        self.presenter.step_started(Steps.calculate_features)

        similarity_calculator.run_feature_calculation(thread, self.step_progress, self.memory_usage_over_limit)

        # Check if thread was stopped while calculating features
        if thread.stopped():
            if not thread.close_window:
                self.presenter.run_completed(True)
            return

        self.presenter.step_completed(Steps.calculate_features)
        self.presenter.step_started(Steps.calculate_clusters)
        
        self.images_clusters = similarity_calculator.run_cluster_calculation()
        self.presenter.step_completed(Steps.calculate_clusters)

        # Check if the clustering algorithm converged
        if similarity_calculator.has_converged == False:
            self.presenter.run_completed(False, "Clustering algorithm didn't converge")
            return

        # Check if thread was stopped while calculating clusters
        if thread.stopped():
            self.images_clusters = []
            if not thread.close_window:
                self.presenter.run_completed(True)
            return
        
        # Save features to cache file
        # If the user has selected to save the calculated features, and there are images to save
        if self.save_calculated_features and len(images_pixel_data) > 0:
            logging.info("Saving calculated features to cache file")
            self.presenter.step_started(Steps.cache_features)
        
            self.cached_features_method = self.selected_feature_extraction_method
            images_paths_features:dict[str,np.array] = {}
            for (image_id, image_features) in similarity_calculator.get_normalized_features().items():
                images_paths_features[self.images_ids_paths.get(image_id)] = image_features
            
            cached_features_file_manager.save_cached_features(images_paths_features, self.cache_file_path, feature_extraction_method_changed)
            self.presenter.step_completed(Steps.cache_features)

        # Filter clusters with only one image
        self.images_clusters = list(filter(lambda cluster: len(cluster) > 1, self.images_clusters))

        # Create ignored images message
        ignored_images_message = ""
        if ignored_images_count > 0:
            ignored_images_message = f"{ignored_images_count} image" + ("s" if ignored_images_count > 1 else "") + " ignored"

        # Call presenter to show results
        self.presenter.run_completed(False, ignored_images_message)
    
    # Return a list of clusters, each cluster is a list of image paths
    def get_clusters_paths(self) -> list[list[str]]:

        result = []

        for cluster in self.images_clusters:
            cluster_paths = []
            for image_id in cluster:
                cluster_paths.append(self.images_ids_paths[image_id])
            result.append(cluster_paths)

        return result
    
    def step_progress(self, current_step:Steps, current_substep:int, total_substeps:int) -> None:
        self.presenter.step_progress(current_substep, total_substeps, current_step)

    def _delete_unverified_images(self, images_paths:dict[int,str], thread:StoppableThread) -> dict[int,str]:
        images_paths_copy = images_paths.copy()
        for (image_id, image_path) in images_paths.items():

            # Check if thread was stopped while loading images
            if thread.stopped():
                if not thread.close_window:
                    self.presenter.run_completed(True)
                return {}
            
            # Chek if the image can be opened
            try:
                im = Image.open(image_path)
            except Exception as e:
                logging.error(f"Error opening image {image_path}: {e}")
                del images_paths_copy[image_id]
                continue
                
            # Check if image passes verification
            try:
                im.verify()
            except Exception as e:
                logging.error(f"Error opening image {image_path}: {e}")
                del images_paths_copy[image_id]
                continue

            # Check if image can be loaded
            try:
                im = Image.open(image_path)
                im.draft('RGB',(1,1)) # This is for performance reasons, we don't need to load the whole image
                im.load()
            except Exception as e:
                im.close()
                logging.error(f"Error opening image {image_path}: {e}")
                del images_paths_copy[image_id]
                continue

            self.step_progress(Steps.verify_images, image_id, len(images_paths))

        # Make ids consecutive
        images_paths_copy = {index: image_path for (index, image_path) in enumerate(images_paths_copy.values())}

        return images_paths_copy
    
    def memory_usage_over_limit(self, thread:StoppableThread) -> bool:
        memory_usage = psutil.virtual_memory().percent
        if memory_usage > self.memory_usage_limit:
            logging.error(f"Memory usage is {memory_usage}%, stopping execution")
            if not thread.close_window:
                self.presenter.run_completed(True, "Memory usage is too high")
            return True
        return False 