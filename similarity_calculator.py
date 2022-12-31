import numpy as np
import keras.utils as image

from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input

from sklearn.cluster import AffinityPropagation
from sklearn.metrics.pairwise import cosine_similarity

from FeatureExtractors.color_distribution_extractor import ColorDistributionFeatureExtractor
from FeatureExtractors.vgg16_extractor import VGG16FeatureExtractor

class SimilarityCalculator():

    def __init__(self, images_pixel_data, feature_extraction_method='vgg16', distance_metric='cosine', clustering_method='affinity_propagation') -> None:

        #TODO: Change this to a class 'FeatureExtractor' or interface because implementing more methods will make this class too big
        self.feature_extraction_method = feature_extraction_method # Could be 'color_distribution', 'vgg16', 'vgg19', 'resnet50'... Implement more methods

        #TODO: Change this to a class 'DistanceCalculator' or interface because implementing more methods will make this class too big
        self.distance_metric = distance_metric # Could be 'euclidean', 'cosine', 'manhattan'... Implement more methods

        #TODO: Change this to a class 'ClusteringCalculator' or interface because implementing more methods will make this class too big
        self.clustering_method = clustering_method # Could be 'affinity_propagation', 'kmeans', 'dbscan'... Implement more methods

        self.images_pixel_data = images_pixel_data # Dictionary with {id: path} pairs

        self.image_features = None # Dictionary with {id: features} pairs
        self.image_clusters = None # List of lists with id's of similar images ordered by similarity

    def set_feature_extraction_method(self, feature_extraction_method: str, parameters: dict=None) -> None:
        self.feature_extraction_method = feature_extraction_method
        self.set_feature_extraction_parameters(parameters)

    def set_feature_extraction_parameters(self, parameters: dict) -> None:
        self.feature_extraction_parameters = parameters

    def set_distance_metric(self, distance_metric: str) -> None:
        self.distance_metric = distance_metric

    def set_clustering_method(self, clustering_method: str) -> None:
        self.clustering_method = clustering_method

    def run(self) -> list[list[int]]: # Each list inside contains a group of id's of similar images ordered by similarity
        
        # Check if there are images to compare
        # Check if features had already been extracted
        #TODO Make a file with the extracted features and check if it exists, if it does, load it and skip the feature extraction. (Check if the method is the same as selected)

        # Load images and extract features
        self.image_features = self._extract_features(self.images_pixel_data)

        # Normalize features
        self.image_features = self._normalize_features(self.image_features)

        # Calculate similarity matrix
        similarity_matrix = self._calculate_similarity_matrix(self.image_features)

        #TODO: Reduce dimensionality of features

        # Calculate clusters
        self.image_clusters = self._calculate_clusters(similarity_matrix)

        return self.image_clusters
    
    def _extract_features(self, images_pixel_data: dict[int, np.array]) -> dict[int, np.ndarray]:
   
        match self.feature_extraction_method:
            case 'vgg16':
                feature_extractor = VGG16FeatureExtractor(self.feature_extraction_parameters)
            case 'color_distribution':
                feature_extractor = ColorDistributionFeatureExtractor(self.feature_extraction_parameters)
            case _:
                raise Exception(f"Feature extraction method '{self.feature_extraction_method}' not implemented")

        images_features = {}
        for (image_id, img) in images_pixel_data.items():
            images_features[image_id] = feature_extractor.extract_features(img)

        return images_features

    def _normalize_features(self, images_features: dict[int, np.ndarray]) -> dict[int, np.ndarray]:

        for (image_id, image_features) in images_features.items():
            images_features[image_id] = image_features / np.linalg.norm(image_features)

        return images_features

    def _calculate_similarity_matrix(self, images_features) -> np.ndarray:

        if self.distance_metric != 'cosine':
            raise Exception(f"Distance metric '{self.distance_metric}' not implemented")

        features_array = np.array(list(images_features.values()))

        return cosine_similarity(features_array)

    def _calculate_clusters(self, similarity_matrix: np.ndarray) -> list[list[int]]:

        if self.clustering_method != 'affinity_propagation':
            raise Exception(f"Clustering method '{self.clustering_method}' not implemented")

        #TODO: Give the option to use different parameters
        affprop = AffinityPropagation(affinity="precomputed", damping=0.5, max_iter=350 , preference= 0.5).fit(similarity_matrix)

        clusters = [[] for _ in range(max(affprop.labels_) + 1)]

        for (index, group) in enumerate(affprop.labels_):
            clusters[group].append(index)
        
        return clusters