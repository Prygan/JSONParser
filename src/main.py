import json_parser


def main():
    parser = json_parser.JsonParser()

    parser.extractfromjson()

    for (key, item) in parser.object_data.items():
        print(item)

if __name__ == "__main__":
    main()
