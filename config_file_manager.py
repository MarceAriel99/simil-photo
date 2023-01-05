import configparser

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

    def _create_config_file(self):
        print("Creating config file...")
        self.config['paths'] = {'images_path': '', 'cache_file_path': ''}
        self.config['feature_extraction'] = {'method': 'vgg16'}
        self.config['similarity'] = {'distance_metric': 'cosine'}
        self.config['clustering'] = {'method': 'affinity_propagation'}
        self.config['cache'] = {'force_recalculate_features': 'False', 'save_calculated_features': 'False'}

        with open(CONFIG_FILE_PATH, 'w') as configfile:
            self.config.write(configfile)