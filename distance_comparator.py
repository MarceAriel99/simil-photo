import numpy as np

def compare_distances(vectors, distance_type='cosine', distance_function=None):

    try:
        vectors = _convert_vectors_to_dict(vectors)
    except TypeError as e:
        raise e

    if distance_type == 'cosine':
        distance_function = _cosine_distance
    elif distance_type == 'euclidean':
        distance_function = _euclidean_distance
    elif distance_type == 'manhattan':
        distance_function = _manhattan_distance
    elif distance_type == 'hamming':
        distance_function = _hamming_distance
    elif distance_type == 'jaccard':
        distance_function = _jaccard_distance
    elif distance_function is not None:
        pass
    else:
        raise ValueError("Invalid distance type")

    for (vector1_name, vector1) in vectors.items():
        for (vector2_name, vector2) in vectors.items():
            if vector1_name == vector2_name:
                continue
            print(f"Distance between {vector1_name} and {vector2_name} is {distance_function(vector1, vector2)}")

def _convert_vectors_to_dict(vectors):

    if isinstance(vectors, dict):
        return vectors

    if not isinstance(vectors, list) :
        raise TypeError("Vectors mut be a dict or a list")

    result = {}

    for (index,vector) in enumerate(vectors):
        result[f"vector_{index+1}"] = vector

    return result

def _cosine_distance(vector1, vector2):
    return 1 - np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

def _euclidean_distance(vector1, vector2):
    return np.linalg.norm(np.array(vector1) - np.array(vector2))

def _manhattan_distance(vector1, vector2):
    return np.sum(np.abs(vector1 - vector2))

def _hamming_distance(vector1, vector2):
    return np.sum(vector1 != vector2)

def _jaccard_distance(vector1, vector2):
    return np.sum(np.minimum(vector1, vector2)) / np.sum(np.maximum(vector1, vector2))