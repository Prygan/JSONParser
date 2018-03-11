from JsonParser.dto.general_info import GeneralInfo
from JsonParser.dto.component import Component
from JsonParser.dto.database_component import DBComponent
from JsonParser.dto.function_component import FunctionComponent
from JsonParser.dto.http_component import HTTPComponent
from JsonParser.dto.stats import Stats
from SqlAnalyzer.SqlReport import SqlReport

import json


class DTOEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, GeneralInfo):
            return {
                "_type"      : "GeneralInfo",
                "file_name " : obj.file_name, 
                "stats"      : obj.stats, 
                "children"   : obj.children
            }
        if isinstance(obj, DBComponent):
            return {
                "_type"     : "DBComponent",
                "module"    : obj.module,
                "project"   : obj.project,
                "duration"  : obj.duration,
                "children"  : obj.children,
                "trace_id"  : obj.trace_id,
                "parent_id" : obj.parent_id,
                "host"      : obj.host,
                "params"    : obj.params,
                "statement" : obj.statement,
                "sql_stats" : DTOEncoder.default(self, obj.sql_stats)
            }
        if isinstance(obj, FunctionComponent):
            return {
                "_type"         : "FunctionComponent",
                "module"        : obj.module,
                "project"       : obj.project,
                "duration"      : obj.duration,
                "children"      : obj.children,
                "trace_id"      : obj.trace_id,
                "parent_id"     : obj.parent_id,
                "function_call" : obj.function_call
            }
        if isinstance(obj, HTTPComponent):
            return {
                "_type"         : "HTTPComponent",
                "module"        : obj.module,
                "project"       : obj.project,
                "duration"      : obj.duration,
                "children"      : obj.children,
                "trace_id"      : obj.trace_id,
                "parent_id"     : obj.parent_id,
                "host"          : obj.host,
                "path"          : obj.path,
                "scheme"        : obj.scheme,
                "method"        : obj.method,
                "query"         : obj.query,
                "labelForChart" : obj.labelForChart
            }
        if isinstance(obj, Stats):
            return {
                "_type"    : "Stats",
                "name"     : obj.name,
                "count"    : obj.count,
                "duration" : obj.duration
            }
        if isinstance(obj, Component):
            return {
                "_type"     : "Component",
                "module"    : obj.module,
                "project"   : obj.project,
                "duration"  : obj.duration,
                "children"  : obj.children,
                "trace_id"  : obj.trace_id,
                "parent_id" : obj.parent_id
            }
        if isinstance(obj, SqlReport):
            return {
                "_type"              : "SqlReport",
                "nb_join"            : obj.nb_join,
                "nb_transac"         : obj.nb_transac,
                "is_compound_select" : obj.is_compound_select 
            }
        return json.JSONEncoder.default(self, obj)