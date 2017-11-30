import argparse
import sys
from JsonParser.json_parser import JsonParser 
from JsonParser.utils import is_file, is_readable, find_files

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





def show_dashboard(parser_object_data):
    # FIG 1
    elements = parser_object_data.children
    labels = list(map(lambda x: x.labelForChart,elements))
    nb = list(map(getHowManyJoinsChildrenIncluded, elements))

    elements = parser_object_data.children
    labels = list(map(lambda x: x.labelForChart[:40],elements))
    nb = list(map(getHowManyJoinsChildrenIncluded, elements))

    trace1 = go.Pie(labels=labels, values=nb)

    # FIG 2
    elements = parser_object_data.children
    vals = {}
    for e in elements:
        vals = dict(Counter(vals) + Counter(getHowManyJoinsForModules(e)))

    projects = list(vals.keys())
    nb = list(vals.values())

    trace2 = go.Pie(labels=projects, values=nb)

    fig = tools.make_subplots(rows=1, cols=2)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    plot(fig, filename='dashboard.html')
    
def getHowManyJoinsChildrenIncluded(element):
    res = 0
    if(isinstance(element, DBComponent)):
        res = res + element.sql_stats.nb_join
    if(element.children != []):
        for c in element.children:
            res = res + getHowManyJoinsChildrenIncluded(c)
    return res

def getHowManyJoins(element):
    res = 0
    if(isinstance(element, DBComponent)):
        res = res + element.sql_stats.nb_join
    return res

def getHowManyJoinsForModules(element):
    res = {}
    if(element.project in res):
        res[element.project] += getHowManyJoins(element)
    else:
        res[element.project] = getHowManyJoins(element)
    for c in element.children:
        res = dict(Counter(res) + Counter(getHowManyJoinsForModules(c)))
    return res
 





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
            show_dashboard(parser.object_data[key])