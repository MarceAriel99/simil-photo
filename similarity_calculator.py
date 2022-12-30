import numpy as np
import keras.utils as image

from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input

from sklearn.cluster import AffinityPropagation
from sklearn.metrics.pairwise import cosine_similarity

class SimilarityCalculator():

    def __init__(self, images_ids_paths, feature_extraction_method='vgg16', distance_metric='cosine', clustering_method='affinity_propagation') -> None:

        #TODO: Change this to a class 'FeatureExtractor' or interface because implementing more methods will make this class too big
        self.feature_extraction_method = feature_extraction_method # Could be 'color_distribution', 'vgg16', 'vgg19', 'resnet50'... Implement more methods

        #TODO: Change this to a class 'DistanceCalculator' or interface because implementing more methods will make this class too big
        self.distance_metric = distance_metric # Could be 'euclidean', 'cosine', 'manhattan'... Implement more methods

        #TODO: Change this to a class 'ClusteringCalculator' or interface because implementing more methods will make this class too big
        self.clustering_method = clustering_method # Could be 'affinity_propagation', 'kmeans', 'dbscan'... Implement more methods

        #TODO: Think if this should be received here or in the run method
        self.images_ids_paths = images_ids_paths # Dictionary with {id: path} pairs

        self.image_features = None # Dictionary with {id: features} pairs
        self.image_clusters = None # List of lists with id's of similar images ordered by similarity

    def set_feature_extraction_method(self, feature_extraction_method: str) -> None:
        self.feature_extraction_method = feature_extraction_method

    def set_distance_metric(self, distance_metric: str) -> None:
        self.distance_metric = distance_metric

    def set_clustering_method(self, clustering_method: str) -> None:
        self.clustering_method = clustering_method

    def run(self) -> list[list[int]]: # Each list inside contains a group of id's of similar images ordered by similarity
        
        # Check if there are images to compare
        # Check if features had already been extracted
        #TODO Make a file with the extracted features and check if it exists, if it does, load it and skip the feature extraction. (Check if the method is the same as selected)

        # Load images and extract features
        self.image_features = self._load_images_and_extract_features(self.images_ids_paths)

        # Normalize features
        self.image_features = self._normalize_features(self.image_features)

        # Calculate similarity matrix
        similarity_matrix = self._calculate_similarity_matrix(self.image_features)

        #TODO: Reduce dimensionality of features

        # Calculate clusters
        self.image_clusters = self._calculate_clusters(similarity_matrix)

        return self.image_clusters
    
    #TODO If the feature extraction is independent from the image loading, extract the loading to outside of this class
    #TODO Separate this method in two 'load_images' and 'extract_features'
    #TODO Change return type to use numpy arrays
    def _load_images_and_extract_features(self, images_ids_paths: dict[int, str]) -> dict[int, np.ndarray]:

        images_features = {}

        if self.feature_extraction_method != 'vgg16':
            raise Exception(f"Feature extraction method '{self.feature_extraction_method}' not implemented")
        
        #TODO extract this to a method or class
        model = VGG16(weights='imagenet', include_top=False)
        for (image_id, image_path) in images_ids_paths.items():
            img = image.load_img(image_path, target_size=(224, 224))
            img_data = image.img_to_array(img)
            img_data = np.expand_dims(img_data, axis=0)
            img_data = preprocess_input(img_data)
            features = np.array(model.predict(img_data))
            images_features[image_id] = features.flatten()

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

        print("IDS PATHS")
        for (image_id, image_path) in self.images_ids_paths.items():
            print(image_id, image_path)
        print("LABELS")
        print(affprop.labels_)
        print(max(affprop.labels_) + 1)

        clusters = [[] for _ in range(max(affprop.labels_) + 1)]

        for (index, group) in enumerate(affprop.labels_):
            clusters[group].append(index)
        
        return clusters