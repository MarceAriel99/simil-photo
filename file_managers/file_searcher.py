import os

'''
Receives a string representing the root directory and a tuple of searched extensions
Returns a dictionary with key -> file_name, value -> file_directory
'''

def file_search(root_directory:str, extensions:tuple[str], search_subdirectories:bool=True) -> dict[str, str]:

    result = {}

    for (root,dirs,files) in os.walk(root_directory, topdown=True):
        root = os.path.normpath(root)
        #print(f"Root: {root}")
        #print(f"Dirs: {dirs}")
        #print(f"Files: {files}")
        if not search_subdirectories and root != root_directory:
            break 
        for file_name in files:
            if file_name.endswith(extensions):
                result[file_name] = root
    
    return result