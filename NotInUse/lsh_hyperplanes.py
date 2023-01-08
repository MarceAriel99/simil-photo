import numpy as np

'''
BUCKET ID CALCULATION (LSH) (MORE GENERIC NAMES)
Receives a dictionary of key -> file_name, value -> signature
Returns a dictionary of key -> bucket, value -> list(file_names)
'''
def calculate_buckets(signatures, number_of_planes):

    dimension = len(list(signatures.values())[0])

    plane_normals = np.random.rand(number_of_planes, dimension) - .5

    buckets = {}

    for (key, signature) in signatures.items():

        bucket_id = [0] * number_of_planes

        for (index, plane_norm) in enumerate(plane_normals):
            result = np.dot(signature, plane_norm)
            bucket_id[index] = int(result > 0)

        bucket_id = ''.join(str(v) for v in bucket_id)

        bucket_value = buckets.get(bucket_id, [])
        bucket_value.append(key)
        buckets[bucket_id] = bucket_value

    return buckets