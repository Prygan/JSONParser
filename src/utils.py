import json
from os import listdir, path
from os.path import isfile, join

class Utils():
    """ Utility class """


    def readjsonfile(self, file_path):
        with open(file_path) as file:
            json_data = json.load(file)
            file.close
            return json_data
            
    def findfiles(self, directory_path):
        return [join(directory_path,file) for file in listdir(directory_path) if isfile(join(directory_path, file))]

