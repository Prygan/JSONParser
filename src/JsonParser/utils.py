import json
from os import listdir, access, R_OK
from os.path import isfile
from os.path import join

def read_jsonfile(file_path):
    with open(file_path) as file:
        json_data = json.load(file)
        file.close
        return json_data

def find_files(directory_path):
    return [join(directory_path, file)
            for file in listdir(directory_path)
            if isfile(join(directory_path, file))
        ]

def is_file(file_path):
    return isfile(file_path)

def is_readable(file_path):
    return access(file_path, R_OK)