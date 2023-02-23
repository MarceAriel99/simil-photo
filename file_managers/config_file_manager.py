import configparser
from constants import *

CONFIG_FILE_PATH = 'config.ini'

class ConfigFileManager:

    def __init__(self):

        self.config = configparser.ConfigParser()

        try:
            open(CONFIG_FILE_PATH, 'r')
        except FileNotFoundError:
            self._create_config_file()

        self.config.read(CONFIG_FILE_PATH)

    def get_config_parameter(self, section, parameter):
        return self.config[section][parameter]

    def set_config_parameters(self, section_param:dict[str,dict[str,str]]):
        for section, parameters in section_param.items():
            for parameter, value in parameters.items():
                self.config[section][parameter] = value

        with open(CONFIG_FILE_PATH, 'w') as configfile:
            self.config.write(configfile)

    def _create_config_file(self): #TODO: generalize this method
        print("Creating config file...")
        self.config[CONFIG_SECTION_PATHS] = {CONFIG_PARAMETER_IMAGES_PATH: CONFIG_DEFAULT_VALUE_IMAGES_PATH, 
                                             CONFIG_PARAMETER_CACHE_FILE_PATH: CONFIG_DEFAULT_VALUE_CACHE_FILE_PATH}
        
        self.config[CONFIG_SECTION_FEATURE_EXTRACTION] ={
                                            CONFIG_PARAMETER_SUPPORTED_FEATURE_EXTRACTION_METHOD: CONFIG_DEFAULT_VALUE_SUPPORTED_FEATURES, 
                                            CONFIG_PARAMETER_SELECTED_FEATURE_EXTRACTION_METHOD: CONFIG_DEFAULT_VALUE_SELECTED_FEATURE_EXTRACTION_METHOD}
        
        self.config[CONFIG_SECTION_FILE_TYPES] = {CONFIG_PARAMETER_SUPPORTED_FILE_TYPES: CONFIG_DEFAULT_VALUE_SUPPORTED_FILE_TYPES, 
                                                  CONFIG_PARAMETER_SELECTED_FILE_TYPES: CONFIG_DEFAULT_VALUE_SELECTED_FILE_TYPES}
        
        self.config[CONFIG_SECTION_CLUSTERING] = {CONFIG_PARAMETER_CLUSTERING_METHOD: CONFIG_DEFAULT_VALUE_CLUSTERING_METHOD}

        self.config[CONFIG_SECTION_CACHE] = {CONFIG_PARAMETER_CACHE_FORCE_RECALCULATE_FEATURES: CONFIG_DEFAULT_VALUE_CACHE_FORCE_RECALCULATE_FEATURES,
                                            CONFIG_PARAMETER_CACHE_SAVE_CALCULATED_FEATURES: CONFIG_DEFAULT_VALUE_CACHE_SAVE_CALCULATED_FEATURES,
                                            CONFIG_PARAMETER_CACHE_FEATURE_EXTRACTION_METHOD: CONFIG_DEFAULT_VALUE_CACHE_FEATURE_EXTRACTION_METHOD}
        
        self.config[CONFIG_SECTION_MISC] = {CONFIG_PARAMETER_MISC_CHECK_SUBDIRECTORIES: CONFIG_DEFAULT_VALUE_MISC_CHECK_SUBDIRECTORIES}

        with open(CONFIG_FILE_PATH, 'w') as configfile:
            self.config.write(configfile)