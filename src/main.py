import argparse
import sys
from JsonParser.utils import is_file, is_readable, find_files

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
