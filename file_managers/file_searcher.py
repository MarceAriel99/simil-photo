import os

'''
Receives a string representing the root directory and a tuple of searched extensions
Returns a dictionary {id:file_directory+name} pairs
'''
def file_search(root_directory:str, extensions:tuple[str], search_subdirectories:bool=True) -> dict[int, str]:

    result = {}

    for (root,dirs,files) in os.walk(root_directory, topdown=True):
        root = os.path.normpath(root)
        if not search_subdirectories and root != root_directory:
            break 
        for file_name in files:
            if file_name.endswith(extensions):
                result[root + "\\" + file_name] = root + "\\" + file_name

    # Upadte keys and change to ids
    result = {index: result[key] for index, key in enumerate(result.keys())}
    
    return result