import csv
import os
import numpy as np
import logging
from constants import PATH_TEMP_FILE


'''
This method loads the cached features from the file
It receives a dictionary with the image ids and paths and the path to the file
It returns a dictionary with the image ids and the features
'''
def load_cached_features(images_ids_paths:dict[int, str], file_path:str) -> dict[int, np.array]:

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
        logging.warning('Cached features file not found')
    except Exception as e:
        logging.error(e)

    return cached_features

'''
This method saves the cached features to the file
It receives a dictionary with the image paths and features and the path to the file
It returns nothing
If force_overwrite is enabled, it will overwrite all the cached features, otherwise it will only overwrite the features that are in the dictionary
'''
def save_cached_features(images_paths_features:dict[str, np.array], file_path:str, force_overwrite:bool = False) -> None:

    if force_overwrite: logging.warning("Force overwrite is enabled, this will overwrite all the cached features")
    
    # This writes the features that are already in the file to the temporary file. If the path is in the dict, then it will override it
    try:
        with open(file_path, 'r', newline='') as csvfile, open(PATH_TEMP_FILE, 'w', newline='') as tempfile:
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
        logging.warning('Cached features file not found')
    except Exception as e:
        logging.error(e)

    # This writes the remaining features to the temporary file (the ones that were not in the original cache file)
    with open(PATH_TEMP_FILE, 'a', newline='') as tempfile:
        writer = csv.writer(tempfile, delimiter=',')
        for (image_path, image_features) in images_paths_features.items():
            row = [image_path]
            row.extend(image_features)
            writer.writerow(row)

    # This deletes the original file and renames the temporary file to the original file
    try:
        os.remove(file_path)
    except Exception as e:
        logging.error(e)

    os.rename(PATH_TEMP_FILE, file_path)