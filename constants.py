CONFIG_SECTION_PATHS = 'paths'
CONFIG_SECTION_FEATURE_EXTRACTION = 'feature_extraction'
CONFIG_SECTION_FILE_TYPES = 'file_types'
CONFIG_SECTION_CLUSTERING = 'clustering'
CONFIG_SECTION_CACHE = 'cache'
CONFIG_SECTION_MISC = 'misc'

CONFIG_PARAMETER_IMAGES_PATH = 'images_path'
CONFIG_PARAMETER_CACHE_FILE_PATH = 'cache_file_path'
CONFIG_PARAMETER_SELECTED_FEATURE_EXTRACTION_METHOD = 'selected'
CONFIG_PARAMETER_SUPPORTED_FEATURE_EXTRACTION_METHOD = 'supported'
CONFIG_PARAMETER_SELECTED_FILE_TYPES = 'selected'
CONFIG_PARAMETER_SUPPORTED_FILE_TYPES = 'supported'
CONFIG_PARAMETER_CLUSTERING_METHOD = 'method'
CONFIG_PARAMETER_CACHE_FORCE_RECALCULATE_FEATURES = 'force_recalculate_features'
CONFIG_PARAMETER_CACHE_SAVE_CALCULATED_FEATURES = 'save_calculated_features'
CONFIG_PARAMETER_CACHE_FEATURE_EXTRACTION_METHOD = 'method'
CONFIG_PARAMETER_MISC_CHECK_SUBDIRECTORIES = 'check_subdirectories'

CONFIG_DEFAULT_VALUE_IMAGES_PATH = ''
CONFIG_DEFAULT_VALUE_CACHE_FILE_PATH = ''
CONFIG_DEFAULT_VALUE_SUPPORTED_FEATURES = ','.join(['vgg16', 'mobilenet', 'color_histogram'])
CONFIG_DEFAULT_VALUE_SELECTED_FEATURE_EXTRACTION_METHOD = 'vgg16'
CONFIG_DEFAULT_VALUE_SUPPORTED_FILE_TYPES = ','.join(['.jpg', '.jpeg', '.png', '.webp'])
CONFIG_DEFAULT_VALUE_SELECTED_FILE_TYPES = ','.join(['.jpg', '.jpeg', '.png', '.webp'])
CONFIG_DEFAULT_VALUE_CLUSTERING_METHOD = 'affinity_propagation'
CONFIG_DEFAULT_VALUE_CACHE_FORCE_RECALCULATE_FEATURES = 'False'
CONFIG_DEFAULT_VALUE_CACHE_SAVE_CALCULATED_FEATURES = 'True'
CONFIG_DEFAULT_VALUE_CACHE_FEATURE_EXTRACTION_METHOD = 'vgg16'
CONFIG_DEFAULT_VALUE_MISC_CHECK_SUBDIRECTORIES = 'True'

PATH_CONFIG_FILE = 'config.ini'
PATH_DEFAULT_CACHE_FILE = 'cached_features.csv'
PATH_FEATURE_EXTRACTION_METHOD_DESCRIPTIONS_FILE = 'feature_extraction_methods_descriptions.json'