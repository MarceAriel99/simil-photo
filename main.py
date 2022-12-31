import sys

import numpy as np
import file_searcher
from similarity_calculator import SimilarityCalculator

import numpy as np
import keras.utils as image
import cv2

def main(path):

    # Search for images in path
    images_names_paths = file_searcher.file_search(path, ('.jpg', '.png'))

    for (image_name, image_root) in images_names_paths.items():
        print(image_name, image_root)

    # Create {id: absolute_path} dictionary
    images_ids_paths = {}
    for (index, (image_name, image_path)) in enumerate(images_names_paths.items()):
        images_ids_paths[index] = f"{image_path}\{image_name}"

    # Load images
    images_pixel_data = {}
    for (image_id, image_path) in images_ids_paths.items():
        img = image.load_img(image_path, target_size=(224, 224)) #TODO try other sizes
        img_data = image.img_to_array(img)
        images_pixel_data[image_id] = img_data
    
    # Create SimilarityCalculator object
    similarity_calculator = SimilarityCalculator(images_pixel_data, feature_extraction_method='color_distribution')
    similarity_calculator.set_feature_extraction_parameters({'color_bins': 32})
    #similarity_calculator = SimilarityCalculator(images_pixel_data, feature_extraction_method='vgg16')
    #similarity_calculator.set_feature_extraction_parameters({'weights': 'imagenet', 'include_top': False})

    # Run similarity calculator
    image_clusters = similarity_calculator.run()

    # Filter clusters with only one image
    image_clusters = filter(lambda cluster: len(cluster) > 1, image_clusters)

    # For each cluster, print the images
    for cluster in image_clusters:
        cluster_list = []
        for image_id in cluster:
            img = cv2.imread(images_ids_paths.get(image_id))
            img = cv2.resize(img, (img.shape[1] // 5, img.shape[0] // 5))
            cluster_list.append(img)
            print(images_ids_paths.get(image_id).split("\\")[-1])
        try:
            Hori = np.concatenate(cluster_list, axis=1)
            cv2.imshow('HORIZONTAL', Hori)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print("-------------------------------")
        except ValueError:
            print("Error concatenating images")
            continue

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python main.py <path to images>")
        sys.exit(1)
    
    main(sys.argv[1])