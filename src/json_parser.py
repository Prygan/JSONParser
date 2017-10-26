from utils import Utils
from dto.db_request import DBRequest
from dto.general_info import GeneralInfo
from dto.http_request import HTTPRequest
from dto.request import Request
from dto.stats import Stats
from os import path
from datetime import datetime

class JsonParser:
    """ Class used to parse Json files from openstack"""
    dir_path = path.dirname(path.realpath(__file__))
    files_directory = dir_path + '/../files/'

    def __init__(self):
        self.util = Utils()
        self.files = self.util.findfiles(self.files_directory)
        self.json_data = dict()
        self.object_data = dict()
        self.requests = []
        self.initializejsondata()


    def initializejsondata(self):
        for file in self.files :
            self.json_data[file] =  (self.util.readjsonfile(file))

    def extractfromjson(self):
        for (key,json) in self.json_data.items() :
            self.extractgeneralinfo(key, json)

    def extractgeneralinfo(self, key, json):
        general_info = GeneralInfo(file_name = key)
        for (key, item) in json["stats"].items():
            general_info.add_stat(Stats(item["count"], item["duration"]), key)
        
        for data in json["children"]:
            self.explorechild(data, general_info)

        self.object_data[key] = general_info


    def explorechild(self, child, request):
        info = child["info"]
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
        if "meta.raw_payload.db-start" in info:
            host = info["meta.raw_payload.db-start"]["info"]["host"]
            project = info["meta.raw_payload.db-start"]["project"]
            params = info["meta.raw_payload.db-start"]["info"]["db"]["params"]
            statement = info["meta.raw_payload.db-start"]["info"]["db"]["statement"]
            start_timestamp_str = info["meta.raw_payload.db-start"]["timestamp"]
            stop_timestamp_str = info["meta.raw_payload.db-stop"]["timestamp"]
            start_timestamp = datetime.strptime(start_timestamp_str, date_format)
            stop_timestamp = datetime.strptime(stop_timestamp_str, date_format)

            db_request = DBRequest(
                project = project,
                host = host,
                duration = str(stop_timestamp - start_timestamp),
                params = params,
                statement = statement,
                parent_id = child["parent_id"],
                trace_id = child["trace_id"]
            )
            request.add_child(db_request)

            for sub_child in child["children"]:
                self.explorechild(sub_child, db_request)
        else:
            start_time_str = info["meta.raw_payload.wsgi-start"]["timestamp"] 
            stop_time_str = info["meta.raw_payload.wsgi-stop"]["timestamp"]
            start_timestamp = datetime.strptime(start_time_str, date_format)
            stop_timestamp = datetime.strptime(stop_time_str, date_format)
            http_request = HTTPRequest( project = info["project"],
                                        host = info["host"],
                                        path = info["meta.raw_payload.wsgi-start"]["info"]["request"]["path"],
                                        scheme = info["meta.raw_payload.wsgi-start"]["info"]["request"]["scheme"],
                                        method = info["meta.raw_payload.wsgi-start"]["info"]["request"]["method"],
                                        query = info["meta.raw_payload.wsgi-start"]["info"]["request"]["query"],
                                        duration = str(stop_timestamp - start_timestamp),
                                        parent_id = child["parent_id"],
                                        trace_id = child["trace_id"])

            for sub_child in child["children"]:
                self.explorechild(sub_child, http_request)
            request.add_child(http_request)

            