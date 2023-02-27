import numpy as np
import keras.utils as image

from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input

from sklearn.cluster import AffinityPropagation
from sklearn.metrics.pairwise import cosine_similarity

from feature_extractors.color_histogram_extractor import ColorHistogramFeatureExtractor
from feature_extractors.vgg16_extractor import VGG16FeatureExtractor
from feature_extractors.mobilenet_extractor import MobileNetFeatureExtractor

from view_components.stoppable_thread import StoppableThread

class SimilarityCalculator():

    def __init__(self, images_pixel_data:dict[int,np.array]={}, images_cached_features:dict[int,np.array]={}, feature_extraction_method:str='vgg16', clustering_method:str='affinity_propagation') -> None:

        self.feature_extraction_method = feature_extraction_method # Could be 'color_histogram', 'vgg16', 'vgg19', 'resnet50'... Implement more methods

        #POSSIBLE UPGRADE: Change this to a class 'ClusteringCalculator' or interface because implementing more methods will make this class too big
        self.clustering_method = clustering_method # Could be 'affinity_propagation', 'kmeans', 'dbscan'... Implement more methods

        self.images_pixel_data = images_pixel_data # Dictionary with {id: data} pairs

        self.image_features = images_cached_features # Dictionary with {id: features} pairs

        self.image_clusters = None # List of lists with id's of similar images ordered by similarity

        self.similarity_matrix = None # Matrix with similarity values between images

    def set_feature_extraction_method(self, feature_extraction_method: str, parameters: dict=None) -> None:
        self.feature_extraction_method = feature_extraction_method
        self.set_feature_extraction_parameters(parameters)

    def set_feature_extraction_parameters(self, parameters: dict[str, any]) -> None:
        self.feature_extraction_parameters = parameters

    def set_clustering_method(self, clustering_method: str) -> None:
        self.clustering_method = clustering_method

    def get_normalized_features(self) -> dict[int, np.ndarray]:
        return self.image_features

    def run_feature_calculation(self, thread:StoppableThread) -> None:
                
        # Extract features
        extracted_features = self._extract_features(self.images_pixel_data, thread)

        # Normalize features
        self.image_features.update(self._normalize_features(extracted_features))

        if self.image_features == {}: return # If there are no features to calculate similarity, return

        # Calculate similarity matrix
        self.similarity_matrix = self._calculate_similarity_matrix(self.image_features)

    def run_cluster_calculation(self) -> list[list[int]]: # Each list inside contains a group of id's of similar images ordered by similarity

        # Calculate clusters
        self.image_clusters = self._calculate_clusters(self.similarity_matrix)

        #Sort images in each cluster by similarity
        self.image_clusters = self._sort_images_by_similarity(self.image_clusters)

        return self.image_clusters
    
    def _extract_features(self, images_pixel_data: dict[int, np.array], thread:StoppableThread) -> dict[int, np.ndarray]:

        if not images_pixel_data: return {} # If there are no images to extract features from, return an empty dictionary
            
        match self.feature_extraction_method:
            case 'vgg16':
                feature_extractor = VGG16FeatureExtractor(self.feature_extraction_parameters)
            case 'mobilenet':
                feature_extractor = MobileNetFeatureExtractor(self.feature_extraction_parameters)
            case 'color_histogram':
                feature_extractor = ColorHistogramFeatureExtractor(self.feature_extraction_parameters)
            case _:
                raise Exception(f"Feature extraction method '{self.feature_extraction_method}' not implemented")

        images_features = {}
        for (image_id, img) in images_pixel_data.items():
            
            if thread.stopped():
                return {}

            images_features[image_id] = feature_extractor.extract_features(img)

        return images_features

    def _normalize_features(self, images_features: dict[int, np.ndarray]) -> dict[int, np.ndarray]:

        if not images_features: return {} # If there are no images to normalize features from, return an empty dictionary

        for (image_id, image_features) in images_features.items():
            images_features[image_id] = image_features / np.linalg.norm(image_features)

        return images_features

    def _calculate_similarity_matrix(self, images_features) -> np.ndarray:

        # The array has to be ordered by id, because the cluster uses the index of the array as the id of the image
        features_array = [[] for _ in range(len(images_features))]

        for id, features in images_features.items():
            features_array[id] = features

        return cosine_similarity(np.array(features_array))
        
    def _calculate_clusters(self, similarity_matrix: np.ndarray) -> list[list[int]]:

        if self.clustering_method != 'affinity_propagation':
            raise Exception(f"Clustering method '{self.clustering_method}' not implemented")

        affprop = AffinityPropagation(affinity="precomputed", damping=0.5, max_iter=350 , preference= 0.5).fit(similarity_matrix)

        clusters = [[] for _ in range(max(affprop.labels_) + 1)]

        for (index, group) in enumerate(affprop.labels_):
            clusters[group].append(index)
        
        return clusters
    
    # Receives a list of lists with id's of similar images and returns the same list but ordered by similarity inside each cluster
    def _sort_images_by_similarity(self, clusters: list[list[int]]) -> list[list[int]]:

        ordered_clusters = []
        cluster_centers = []

        #Find the center of each cluster
        for cluster in clusters:
            array_of_features = np.array([self.image_features[image_id] for image_id in cluster])
            center = np.mean(array_of_features, axis=0)

            #Get the index of the image that is closest to the center
            most_central_image_index = np.argmin(np.linalg.norm(array_of_features - center, axis=1))

            #Get the id of the image that is closest to the center
            most_central_image_id = cluster[most_central_image_index]

            #print(f"All cluster images: {cluster}")
            #print(f"Cluster center image id: {most_central_image_id}")

            cluster_centers.append(most_central_image_id)

        #Sort each cluster by similarity to the center, starting with the most similar image
        for (index, cluster) in enumerate(clusters):
            ordered_clusters.append(sorted(cluster, key=lambda x: self.similarity_matrix[cluster_centers[index]][x], reverse=True))

        return ordered_clusters
