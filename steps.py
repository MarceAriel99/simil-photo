from enum import Enum

class Steps(Enum):
    search_images = 0
    load_cached_features = 1
    load_images = 2
    calculate_features = 3
    calculate_clusters = 4
    cache_features = 5