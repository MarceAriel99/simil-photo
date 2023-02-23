import csv
import os
import numpy as np

TEMP_FILE_NAME = 'TEMP.csv'

def load_cached_features(images_ids_paths:dict[int, str], file_path) -> dict[int, np.array]:

    cached_features = {}

    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                image_path = row[0]
                if image_path not in images_ids_paths.values():
                    continue
                image_features = np.array([float(x) for x in row[1:]])
                image_id = list(images_ids_paths.keys())[list(images_ids_paths.values()).index(image_path)]
                cached_features[image_id] = image_features
    except FileNotFoundError:
        print('Cached features file not found')
    except Exception as e:
        print(e)

    return cached_features

def save_cached_features(images_paths_features:dict[str, np.array], file_path, force_overwrite:bool = False):

    if force_overwrite: print("Force overwrite is enabled, this will overwrite all the cached features")

    try:
        with open(file_path, 'r', newline='') as csvfile, open(TEMP_FILE_NAME, 'w', newline='') as tempfile:
            reader = csv.reader(csvfile, delimiter=',')
            writer = csv.writer(tempfile, delimiter=',')
            for index, row in enumerate(reader):
                image_path = row[0]
                if image_path in images_paths_features.keys() or force_overwrite: #If the path in the file is in the dict, then override it
                    row = [image_path]
                    row.extend(images_paths_features[image_path])
                    writer.writerow(row)
                    del images_paths_features[image_path]
                else: #If the path in the file is not in the dict, then just copy it
                    writer.writerow(row)
    except FileNotFoundError:
        print('Cached features file not found')
    except Exception as e:
        print(e)

    with open(TEMP_FILE_NAME, 'a', newline='') as tempfile:
        writer = csv.writer(tempfile, delimiter=',')
        for (image_path, image_features) in images_paths_features.items():
            row = [image_path]
            row.extend(image_features)
            writer.writerow(row)

    try:
        os.remove(file_path)
    except Exception as e:
        print(e)

    os.rename(TEMP_FILE_NAME, file_path)