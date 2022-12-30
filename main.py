import sys
import file_searcher
from similarity_calculator import SimilarityCalculator

def main(path):

    # Search for images in path
    images_names_paths = file_searcher.file_search(path, ('.jpg', '.png'))

    for (image_name, image_root) in images_names_paths.items():
        print(image_name, image_root)

    # Create {id: absolute_path} dictionary
    images_ids_paths = {}
    for (index, (image_name, image_path)) in enumerate(images_names_paths.items()):
        images_ids_paths[index] = f"{image_path}\{image_name}"
    
    # Create SimilarityCalculator object
    similarity_calculator = SimilarityCalculator(images_ids_paths)

    # Run similarity calculator
    image_clusters = similarity_calculator.run()

    # Filter clusters with only one image

    # For each cluster, print the images
    for cluster in image_clusters:
        for image_id in cluster:
            print(images_ids_paths.get(image_id).split("\\")[-1])
        print("-------------------------------")

    pass

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python main.py <path to images>")
        sys.exit(1)
    
    main(sys.argv[1])