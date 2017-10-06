from utils import Utils
from os import path
from dto.request import Request
from datetime import datetime

class SqlParser:
    """ Class used to parse Json files from openstack"""
    __dir_path = path.dirname(path.realpath(__file__))
    __files_directory = __dir_path + '/../files/'

    def __init__(self):
        self.__util = Utils()
        self.__files = self.__util.findfiles(self.__files_directory)
        self.__json_data = dict()
        self.__requests = []
        self.initializejsondata()


    def initializejsondata(self):
        for file in self.__files :
            self.__json_data[file] =  (self.__util.readjsonfile(file))

    #def getDbRequestNumber(self):
    #    print(len(self.__json_data["children"]))

    def extractdbrequests(self):

        for (key,item) in self.__json_data.items() :
            for data in item["children"] :
                for children in data["children"] :
                    self.explorechild(children)

        #print(len(self.__requests))            

    def explorechild(self, child):
        if "meta.raw_payload.db-start" in child["info"]:
            statement = child["info"]["meta.raw_payload.db-start"]["info"]["db"]["statement"]
            start_timestamp_str = child["info"]["meta.raw_payload.db-start"]["timestamp"]
            stop_timestamp_str = child["info"]["meta.raw_payload.db-stop"]["timestamp"]
            
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
            start_timestamp = datetime.strptime(start_timestamp_str, date_format)
            stop_timestamp = datetime.strptime(stop_timestamp_str, date_format)

            self.__requests.append(Request(
                statement = statement,
                duration = str(stop_timestamp - start_timestamp)
            ))

        for sub_child in child["children"]:
            self.explorechild(sub_child)

            