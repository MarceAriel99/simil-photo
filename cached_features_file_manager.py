import csv
import numpy as np

# TODO put these in a config file
FILE_PATH = 'cached_features.csv'

# TODO manage exceptions
def load_cached_features(images_ids_paths:dict[int, str]) -> dict[int, np.array]:
    cached_features = {}
    with open(FILE_PATH, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            image_path = row[0]
            image_features = np.array(row[1:])
            if image_path not in images_ids_paths.values():
                continue
            image_id = list(images_ids_paths.keys())[list(images_ids_paths.values()).index(image_path)]
            cached_features[image_id] = image_features
    return cached_features

# TODO manage exceptions
# TODO don't overwrite existing features, if they exist, override, otherwise append
def save_cached_features(images_paths_features:dict[str, np.array]): 

    with open(FILE_PATH, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for (image_path, image_features) in images_paths_features.items():
            row = [image_path]
            row.extend(image_features)
            writer.writerow(row)