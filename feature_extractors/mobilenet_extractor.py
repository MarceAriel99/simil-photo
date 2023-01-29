import numpy as np

from keras.applications.mobilenet_v2 import MobileNetV2
from keras.applications.mobilenet_v2 import preprocess_input

class MobileNetFeatureExtractor():

    def __init__(self, parameters:dict={}):
        weights = parameters['weights'] if 'weights' in parameters else 'imagenet'
        include_top = parameters['include_top'] if 'include_top' in parameters else False
        self.model = MobileNetV2(include_top=include_top, weights=weights)

    def set_parameters(self, parameters:dict={}):
        weights = parameters['weights'] if 'weights' in parameters else 'imagenet'
        include_top = parameters['include_top'] if 'include_top' in parameters else False
        self.model = MobileNetV2(include_top=include_top, weights=weights)

    # This is done for all images, maybe we can pass list or set of images, and make some calculation just once (all pre-calculations)
    def extract_features(self, img): # Should accept more parameters
        return self._calculate_features_of_image(img)
    
    # Predicts the features of an image by using vgg16
    def _calculate_features_of_image(self, img):
        img_data = np.expand_dims(img, axis=0)
        img_data = preprocess_input(img_data)
        return np.array(self.model.predict(img_data)).flatten()