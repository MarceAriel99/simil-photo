import numpy as np

from keras.applications.mobilenet_v2 import preprocess_input
from keras.models import load_model

import logging
from constants import PATH_MOBILENET

class MobileNetFeatureExtractor():

    def __init__(self, parameters:dict[str,any]={}) -> None:
        '''
        If you want to make a new model with specific parameters, you can use this code:

        weights = parameters['weights'] if 'weights' in parameters else 'imagenet'
        include_top = parameters['include_top'] if 'include_top' in parameters else False
        mobilenet = MobileNetV2(include_top=include_top, weights=weights, input_shape=(224, 224, 3))
        x = GlobalAveragePooling2D()(mobilenet.output)
        x = Dense(4096, activation='relu')(x)
        self.model = Model(inputs=mobilenet.input, outputs=x)

        Then you can save the model with:
        self.model.save('resources/models/mobilenet_custom.h5')
        '''
        # Load the model from the file
        self.model = load_model(PATH_MOBILENET)

    def set_parameters(self, parameters:dict[str,any]={}) -> None:
        # POSSIBLE UPGRADE: Implement variable parameters
        logging.info("Changing parameters of MobileNetFeatureExtractor is not supported")

    # This is done for all images, maybe we can pass list or set of images, and make some calculation just once (all pre-calculations)
    def extract_features(self, img:np.ndarray) -> np.ndarray: # Should accept more parameters
        
        return self._calculate_features_of_image(img)
    
    # Predicts the features of an image by using mobilenet
    def _calculate_features_of_image(self, img:np.ndarray) -> np.ndarray:
        
        img_data = np.expand_dims(img, axis=0)
        img_data = preprocess_input(img_data)
        try:
            features = self.model.predict(img_data, verbose=0)
        except Exception as e:
            logging.error(f"Error while extracting features {e}")
            raise e

        return features[0]