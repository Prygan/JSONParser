from json_parser import JsonParser


def main():
    parser = JsonParser()
    parser.extract_from_json()

    for (key, item) in parser.object_data.items():
        print(item)

if __name__ == "__main__":
    main()
