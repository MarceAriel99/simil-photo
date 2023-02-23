import numpy as np

class ColorHistogramFeatureExtractor():

    def __init__(self, parameters:dict[str,any]={}) -> None:
        color_bins = parameters['color_bins'] if 'color_bins' in parameters else 16
        self.color_bins = color_bins

    def set_parameters(self, parameters:dict[str,any]) -> None:
        color_bins = parameters['color_bins'] if 'color_bins' in parameters else 16
        self.color_bins = color_bins

    # This is done for all images, maybe we can pass list or set of images, and make some calculation just once (all pre-calculations)
    # TODO: All pre-calculations should be done in this method
    def extract_features(self, image:np.ndarray) -> np.ndarray:
        return self._calculate_features_of_image(image, self.color_bins)
        
    # Calculates the signature of an image by using color distribution
    # Separates each color in a number of bins
    def _calculate_features_of_image(self, img:np.ndarray, color_bins:int) -> np.ndarray: #POSSIBLE UPGRADE: Optimize speed with numpy (If possible)

        signature_length = color_bins**3 # The signature will have a length of color_bins^3
        signature = [0] * signature_length # The signature is a vector representing color distribution

        multiplier = 256 / color_bins # A multiplier that represents the size of each color bin

        pre_calculated_array_multipliers = {}
        for k in range(3):
            pre_calculated_array_multipliers[k] = color_bins**(2-k)

        #For each pixel, see which bucket should we increase
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                    
                pixel = img[i,j]

                key = [0,0,0] # The key representing the index in which the signature will be increased by one

                for channel_index in range(3): # For each color (R,G,B), calculate in which color bin the number falls
                    counter = pixel[channel_index]
                    for k in range(color_bins): # For each color bin, substract the multiplier. 
                        # The ammount of times the multiplier was substracted before reaching 0 indicates the color bin in which the number falls
                        counter -= multiplier
                        if counter <= 0:
                            key[channel_index] = k
                            break

                # Transforms the key to an index in the signature vector
                bucket = 0
                for k in range(3):
                    bucket += key[k] * pre_calculated_array_multipliers.get(k)
                
                # Increase the numebr in that index of the vector by one
                signature[bucket] += 1
        
        #TODO: print step time duration
        return np.array(signature)