from utils import Utils
from os import path

class SqlParser():
    """ Class used to parse Json files from openstack"""
    __dir_path = path.dirname(path.realpath(__file__))
    __files_directory = __dir_path + '/../files/'


    def __init__(self):
        self.__util = Utils()
        self.__files = self.__util.findfiles(self.__files_directory)
        self.__json_data = dict()
        self.initializejsondata()

    def initializejsondata(self):
        for file in self.__files :
            self.__json_data[file] =  (self.__util.readjsonfile(file))
    #def getDbRequestNumber(self):
    #    print(len(self.__json_data["children"]))

    def getDbRequests(self):
        i = 0

        for (key,item) in self.__json_data.items() :
            for data in item["children"] :
                for children in data["children"] :
                    
                    if "meta.raw_payload.db-start" in children["info"]:
                        i += 1
                        print(children["info"]["meta.raw_payload.db-start"]["info"]["db"]["statement"])
                        # CHERCHER AUSSI DANS CHILDREN
        print(i)

