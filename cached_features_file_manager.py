import csv
import numpy as np

# TODO manage exceptions
def load_cached_features(images_ids_paths:dict[int, str], file_path) -> dict[int, np.array]:

    cached_features = {}

    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                image_path = row[0]
                if image_path not in images_ids_paths.values():
                    continue
                image_features = np.array(row[1:])
                image_id = list(images_ids_paths.keys())[list(images_ids_paths.values()).index(image_path)]
                cached_features[image_id] = image_features
    except FileNotFoundError:
        print('Cached features file not found')

    return cached_features

# TODO manage exceptions
# TODO don't overwrite existing features, if they exist, override, otherwise append
def save_cached_features(images_paths_features:dict[str, np.array], file_path): 

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for (image_path, image_features) in images_paths_features.items():
            row = [image_path]
            row.extend(image_features)
            writer.writerow(row)