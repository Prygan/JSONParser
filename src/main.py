import json_parser

parser = json_parser.JsonParser()

parser.extractfromjson()
for (key, item) in parser.object_data.items():
    print(item)