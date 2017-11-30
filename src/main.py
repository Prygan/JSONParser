import argparse
import sys
from JsonParser.json_parser import JsonParser 
from JsonParser.utils import is_file, is_readable, find_files
from dashboard import generate_dashboard

def get_files(files): 
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
    return files
 
def get_directory(directory): 
    return find_files(directory)
 
def parse_files(files): 
    parser = JsonParser(files) 
    print('--- Analyzing : \n - ' + '\n - '.join(parser.files) + '\n') 
    parser.extract_from_json() 
    return parser



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--directory", help="select directory of which you want to use all files")
    group.add_argument("-f", "--files", nargs='+', help="use JSON stacktrace files")
    parser.add_argument("--no-dashboard", help="Don't show dashboard, just parse", action="store_true")
    args = parser.parse_args()

    files = None
    if args.directory:
        files = get_directory(args.directory)
    elif args.files:
        files = get_files(args.files)
    else:
        print("No files or directory given, process exits")
        sys.exit(0)

    parser = parse_files(files)
    if not args.no_dashboard:
        for key in parser.object_data.keys():
            print('--- Dashboard for file ' + key + ' ---\n')
            generate_dashboard(parser.object_data[key])