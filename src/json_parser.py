
from datetime import datetime
from os import path
from re import search
from utils import Utils

from dto.component import Component
from dto.database_component import DBComponent
from dto.function_component import FunctionComponent
from dto.general_info import GeneralInfo
from dto.http_component import HTTPComponent
from dto.stats import Stats


class JsonParser(object):
    """Class used to parse Json files from openstack"""
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
        for file in self.files:
            self.json_data[file] = (self.util.readjsonfile(file))

    def extractfromjson(self):
        for (key, json) in self.json_data.items():
            self.extractgeneralinfo(path.basename(key), json)

    def extractgeneralinfo(self, file, json):
        general_info = GeneralInfo(file_name=file)

        for (key, item) in json["stats"].items():
            general_info.add_stat(Stats(name=key,
                                        count=item["count"],
                                        duration=item["duration"]
                                        )
                                  )

        for data in json["children"]:
            self.explorechild(data, general_info)

        self.object_data[file] = general_info

    def explorechild(self, child, parent):
        info = child["info"]

        keys = list(info.keys())
        service = ''

        for key in keys:
            service = self.extractcomponentfrommeta(key)
            if service:
                break

        if service:
            name = info["name"]

            start = info["meta.raw_payload."+service+"-start"]["timestamp"]
            end = info["meta.raw_payload."+service+"-stop"]["timestamp"]
            duration = self.parsetimestamp(start, end)

            trace_id = child["trace_id"]
            parent_id = child["parent_id"]
            project = info["project"]

            general = Component(
                name=name,
                project=project,
                duration=duration,
                parent_id=parent_id,
                trace_id=trace_id
            )

            if service in DBComponent.types:
                component = self.parsedatabasecomponent(general, service, info)
            elif service in FunctionComponent.types:
                component = self.parsefunctioncomponent(general, service, info)
            elif service in HTTPComponent.types:
                component = self.parsehttpcomponent(general, service, info)
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
        found = search("meta.raw_payload.(.+?)-start", string)
        if found:
            result = found.group(1)

        return result

    def parsedatabasecomponent(self, general, key, component):
        db = component["meta.raw_payload." + key + "-start"]
        host = db["info"]["host"]
        params = db["info"]["db"]["params"]
        statement = db["info"]["db"]["statement"]

        db_component = DBComponent(
            name=general.name,
            project=general.project,
            duration=general.duration,
            parent_id=general.parent_id,
            trace_id=general.trace_id,
            host=host,
            params=params,
            statement=statement
        )

        return db_component

    def parsefunctioncomponent(self, general, key, component):

        function = component["meta.raw_payload." + key + "-start"]["info"]\
                            ["function"]["name"]

        fun_component = FunctionComponent(
            name=general.name,
            project=general.project,
            duration=general.duration,
            parent_id=general.parent_id,
            trace_id=general.trace_id,
            function_call=function
        )

        return fun_component

    def parsehttpcomponent(self, general, key, component):
        host = component["host"]

        request = component["meta.raw_payload." + key + "-start"]\
                           ["info"]["request"]

        path = request["path"]
        scheme = request["scheme"]
        method = request["method"]
        query = request["query"]

        http_component = HTTPComponent(
            name=general.name,
            project=general.project,
            duration=general.duration,
            parent_id=general.parent_id,
            trace_id=general.trace_id,
            host=host,
            path=path,
            scheme=scheme,
            method=method,
            query=query
        )

        return http_component
