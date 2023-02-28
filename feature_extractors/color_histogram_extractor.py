import numpy as np
import timeit
import logging

class ColorHistogramFeatureExtractor():

    def __init__(self, parameters:dict[str,any]={}) -> None:
        color_bins = parameters['color_bins'] if 'color_bins' in parameters else 16
        self.color_bins = color_bins

    def set_parameters(self, parameters:dict[str,any]) -> None:
        color_bins = parameters['color_bins'] if 'color_bins' in parameters else 16
        self.color_bins = color_bins

    # This is done for all images, maybe we can pass list or set of images, and make some calculation just once (all pre-calculations)
    def extract_features(self, image:np.ndarray) -> np.ndarray:

        signature_length = self.color_bins**3 # The signature will have a length of color_bins^3
        multiplier = 256 / self.color_bins # A multiplier that represents the size of each color bin
        pre_calculated_array_multipliers = {}
        for k in range(3):
            pre_calculated_array_multipliers[k] = self.color_bins**(2-k)

        return self._calculate_features_of_image(image, self.color_bins, signature_length, pre_calculated_array_multipliers)
        
    # Calculates the signature of an image by using color distribution
    # Separates each color in a number of bins 
    def _calculate_features_of_image(self, img: np.ndarray, color_bins: int, signature_length: int, array_multipliers: dict[int, int]) -> np.ndarray:

        # Start the timer
        start = timeit.default_timer()

        r, g, b = img[..., 0], img[..., 1], img[..., 2]

        # Calculate the color bin indices for each pixel
        r_indices = np.clip((r / 256 * color_bins).astype(int), 0, color_bins - 1)
        g_indices = np.clip((g / 256 * color_bins).astype(int), 0, color_bins - 1)
        b_indices = np.clip((b / 256 * color_bins).astype(int), 0, color_bins - 1)

        # Compute the bucket indices and count the number of pixels in each bucket
        bucket_indices = r_indices * array_multipliers[0] + g_indices * array_multipliers[1] + b_indices * array_multipliers[2]
        signature = np.bincount(bucket_indices.flatten(), minlength=signature_length)

        # End the timer and print the elapsed time
        end = timeit.default_timer()
        logging.debug(f"ColorHistogramFeatureExtractor took {int((end - start) * 10 ** 6)} us/step")

        return signature