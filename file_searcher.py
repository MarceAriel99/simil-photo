import os

'''
Receives a string representing the root directory and a tuple of searched extensions
Returns a dictionary with key -> file_name, value -> file_directory
'''
def file_search(root_directory, extensions) -> dict[str, str]:

    result = {}

    for (root,dirs,files) in os.walk(root_directory, topdown=True):
        for file_name in files:
            if file_name.endswith(extensions):
                result[file_name] = root
    
    return result