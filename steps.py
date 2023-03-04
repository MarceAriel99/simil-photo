from enum import Enum

class Steps(str, Enum):
    search_images = "Searching images..."
    verify_images = "Verifying images..."
    load_cached_features = "Loading cached features..."
    load_images = "Loading images..."
    calculate_features = "Calculating features..."
    calculate_clusters = "Calculating clusters..."
    cache_features = "Caching features..."