import numpy as np

from keras.applications.vgg16 import VGG16, preprocess_input
from keras.layers import Flatten, Dense
from keras.models import Model

class VGG16FeatureExtractor():

    def __init__(self, parameters:dict[str,any]={}) -> None:

        weights = parameters['weights'] if 'weights' in parameters else 'imagenet'
        include_top = parameters['include_top'] if 'include_top' in parameters else False
        # Create the base pre-trained model with an output of 4096 features
        vgg16 = VGG16(include_top, weights, input_shape=(224, 224, 3))
        x = Flatten()(vgg16.output)
        x = Dense(4096, activation='relu')(x)
        self.model = Model(inputs=vgg16.input, outputs=x)

    def set_parameters(self, parameters:dict[str,any]={}) -> None:

        weights = parameters['weights'] if 'weights' in parameters else 'imagenet'
        include_top = parameters['include_top'] if 'include_top' in parameters else False
        vgg16 = VGG16(include_top, weights, input_shape=(224, 224, 3))
        x = Flatten()(vgg16.output)
        x = Dense(4096, activation='relu')(x)
        self.model = Model(inputs=vgg16.input, outputs=x)

    # This is done for all images, maybe we can pass list or set of images, and make some calculation just once (all pre-calculations)
    def extract_features(self, img:np.ndarray) -> np.ndarray: # Should accept more parameters

        return self._calculate_features_of_image(img)
    
    # Predicts the features of an image by using vgg16
    def _calculate_features_of_image(self, img:np.ndarray) -> np.ndarray:
        
        img_data = np.expand_dims(img, axis=0)
        img_data = preprocess_input(img_data)
        features = self.model.predict(img_data)

        return features[0]