# https://lkaihua.github.io/posts/find-similar-images-based-on-locality-sensitive-hashing/

IMAGE_SIZE = 224

from math import sqrt
from PIL import Image
import numpy as np
from scipy import sparse

import keras.utils as image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input

from FeatureExtractors.image_feature_extractor import FeatureExtractor
from file_searcher import file_search
#from k_means import KMeans
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
from sklearn.metrics.pairwise import cosine_similarity

from distance_comparator import compare_distances

from lsh_hyperplanes import calculate_buckets

'''
COSINE DISTANCE CALCULATION
'''
def cosine_distance(a, b):
    if len(a) != len(b):
        return False
    numerator = 0
    denoma = 0
    denomb = 0
    for i in range(len(a)):
        numerator += a[i]*b[i]
        denoma += abs(a[i])**2
        denomb += abs(b[i])**2
    result = 1 - numerator / (sqrt(denoma)*sqrt(denomb))
    return result

'''
PROOF OF CONCEPT IMPLEMENTATION
'''


#..\Images
#E:\Mis_Archivos\Fotos\Lu
print("Searching for files...")
images_names_and_directories = file_search('E:\Mis_Archivos\Fotos\Lu', ('.jpg', '.png'))
print("DONE")

'''
print("Loading images...")
images = {}
for (image_name, image_root) in images_names_and_directories.items():
    img = Image.open(image_root + "\\" + image_name)
    img.draft('RGB',(4,4))
    img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
    px = img.load()
    images[image_name] = px
print("DONE")
'''

print("Extracting features...")

images_features = {}
'''
feature_extractor = FeatureExtractor('color_distribution')
for (image_name, image) in images.items():
    images_features[image_name] = feature_extractor.extract_features(image)
'''

model = VGG16(weights='imagenet', include_top=False)
for (image_name, image_root) in images_names_and_directories.items():
    img = image.load_img(image_root + "\\" + image_name, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    features = np.array(model.predict(img_data))
    images_features[image_name] = features.flatten()
print("DONE")

for (image_name, features) in images_features.items():
    print(image_name, features)

'''
print("Calculating buckets...")
buckets = calculate_buckets(images_signatures, 3)
print("DONE")

for (bucket_id, group) in buckets.items():
    print(bucket_id, group)

print(f"Original number of images is {len(images_names_and_directories)}")
print(f"Number of buckets is {len(buckets)}")
'''
original_list_of_arrays = []
list_of_arrays = []

for (name, features) in images_features.items():
    original_list_of_arrays.append(name)

    array = np.asarray(features)
    list_of_arrays.append(array / np.sqrt(np.sum(array**2)) )

arr = np.array(list_of_arrays)
arr = np.nan_to_num(arr)
#print(arr)
#print(arr.shape)

print("Calculating clusters...")
similarities_matrix = cosine_similarity(arr)
#print(similarities_matrix)
affprop = AffinityPropagation(affinity="precomputed", damping=0.5, max_iter=350 , preference= 0.5).fit(similarities_matrix)
print("DONE")
print(f"Original quantity of images: {len(images_features)}")

final_groups = {}

for (index, group) in enumerate(affprop.labels_):
    final_groups[group] = final_groups.get(group, [])
    final_groups[group].append(original_list_of_arrays[index])
    pass

print(f"Quantity of buckets with more than one image: {len([x for x in final_groups.values() if len(x) > 1])}")

#print final_groups) 
for group in final_groups.values():
    if len(group) > 1:
        print(group)

# for group in final_groups.values():
#     group_dict = {}
#     for image_name in group:
#         group_dict[image_name] = images_features.get(image_name)
#     print("------------------")
#     compare_distances(group_dict)

#compare_distances(images_features, 'cosine')

'''
groups = {}

for (index,group) in enumerate(kmeans.labels_):
    groups[group] = groups.get(group, [])
    groups[group].append(buckets.get(original_list_of_arrays[index]))

for (group, arrays) in groups.items():
    print(group, arrays)

for image_list in groups.get(0):
    for image_name in image_list:
        img = Image.open(images_names_and_directories.get(image_name) + "\\" + image_name)
        img.show()
'''
#Clustering of buckets? Or maybe Hamming distance limit
'''
for (signature1_name, signature1) in images_signatures.items():
    for (signature2_name, signature2) in images_signatures.items():
        print(f"{signature1_name} image with {signature2_name} image have a distance of: {cosine_distance(signature1, signature2)}")'''