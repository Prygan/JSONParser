from utils import Utils
from os import path
from datetime import datetime
import re

from dto.general_info import GeneralInfo

from dto.component import Component
from dto.database_component import DBComponent
from dto.function_component import FunctionComponent
from dto.http_component import HTTPComponent

from dto.stats import Stats

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
            self.extractgeneralinfo(path.basename(key), json)

    def extractgeneralinfo(self, file, json):
        general_info = GeneralInfo(file_name = file)

        for (key, item) in json["stats"].items():
            general_info.add_stat(Stats(key, item["count"], item["duration"]), key)
        
        for data in json["children"]:
            self.explorechild(data, general_info)

        self.object_data[file] = general_info


    def explorechild(self, child, parent):
        info = child["info"]
        
        keys = list(info.keys())
        componentkey = ''
        
        for key in keys:
            componentkey = self.extractcomponentfrommeta(key)
            if componentkey:
                break

        if componentkey :
            name = info["name"]

            start_timestamp_str = info["meta.raw_payload."+componentkey+"-start"]["timestamp"]
            stop_timestamp_str = info["meta.raw_payload."+componentkey+"-stop"]["timestamp"]
            duration = self.parsetimestamp(start_timestamp_str, stop_timestamp_str)

            trace_id = child["trace_id"]
            parent_id = child["parent_id"]
            project = info["project"] 

            general = Component(
                name = name,
                project = project,
                duration = duration,
                parent_id = parent_id,
                trace_id =  trace_id
            )

            if componentkey in DBComponent.types:
                component = self.parsedatabasecomponent(general, componentkey, info)
            elif componentkey in FunctionComponent.types:
                component = self.parsefunctioncomponent(general, componentkey, info)
            elif componentkey in HTTPComponent.types:
                component = self.parsehttpcomponent(general, componentkey, info)
            else:
                raise ValueError("Key should exist in types")

            parent.add_child(component)
        
        else:
            raise ValueError("No component found")

        for sub_child in child["children"]:
            self.explorechild(sub_child, component)


    def parsetimestamp(self, start, end):
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
        start_timestamp = datetime.strptime(start, date_format)
        end_timestamp = datetime.strptime(end, date_format)

        return str(end_timestamp - start_timestamp)

    def extractcomponentfrommeta(self, string):
        result = ''
        found = re.search("meta.raw_payload.(.+?)-start", string)
        if found:
            result = found.group(1)

        return result
        
    def parsedatabasecomponent(self, general, key, component):

        db = component["meta.raw_payload." + key + "-start"]
        project = db["project"]
        host = db["info"]["host"]
        params = db["info"]["db"]["params"]
        statement = db["info"]["db"]["statement"]

        db_component = DBComponent(
            name = general.name,
            project = general.project,
            duration = general.duration,
            parent_id = general.parent_id,
            trace_id = general.trace_id,
            host = host,
            params = params,
            statement = statement
        )

        return db_component

    def parsefunctioncomponent(self, general, key, component):

        function = component["meta.raw_payload." + key + "-start"]["info"]["function"]["name"]

        fun_component = FunctionComponent(
            name = general.name,
            project = general.project,
            duration = general.duration,
            parent_id = general.parent_id,
            trace_id = general.trace_id,
            function_call = function
        )

        return fun_component


    def parsehttpcomponent(self, general, key, component):

        host = component["host"]

        request = component["meta.raw_payload." + key + "-start"]["info"]["request"]

        path = request["path"]
        scheme = request["scheme"]
        method = request["method"]
        query = request["query"]

        http_component = HTTPComponent(
            name = general.name,
            project = general.project,
            duration = general.duration,
            parent_id = general.parent_id,
            trace_id = general.trace_id,
            host = host,
            path = path,
            scheme = scheme,
            method = method,
            query = query
        )

        return http_component

    


            