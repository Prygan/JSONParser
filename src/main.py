import argparse
import sys
from JsonParser.utils import is_file, is_readable, find_files

def useFiles(files):
    ok = True
    for f in files:
        if not is_file(f):
            print("This is not a file : " + f)
            ok = False
        elif not is_readable(f):
            print("File is not readable : " + f)
            ok = False
            
    if not ok:
        sys.exit(1)
    else:
        parseFiles(files)

def useDirectory(directory):
    parseFiles(find_files(directory))

def parseFiles(files):
    from JsonParser.json_parser import JsonParser
    parser = JsonParser(files)
    print('--- Analyzing : \n - ' + '\n - '.join(parser.files) + '\n')
    parser.extract_from_json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--directory", help="select directory of which you want to use all files")
    group.add_argument("-f", "--files", nargs='+', help="use JSON stacktrace files")
    # parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1], help="increase output verbosity")
    args = parser.parse_args()

    if args.directory:
        useDirectory(args.directory)
    elif args.files:
        useFiles(args.files)
    else:
        print("No files or directory given, process exits")
        sys.exit(0)