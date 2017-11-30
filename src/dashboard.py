from JsonParser.json_parser import JsonParser
from JsonParser.dto.database_component import DBComponent
from SqlAnalyser.SqlReport import SqlReport
from collections import Counter
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

FILE = 'trace-create-and-delete-image.yaml.json'
# FILE = 'trace-report-boot-and-associate-floating-ip.yaml-f7a3b33f-d2e4-4c6c-8bf0-3782b7b675f8.json' 


init_notebook_mode(connected=True)

parser = JsonParser()
parsedFile = parser.files[0]
print("--- Fichier analysé : " + parsedFile)
parser.extract_from_json()

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

# FIG 1

elements = parser.object_data[FILE].children
labels = list(map(lambda x: x.labelForChart,elements))
nb = list(map(getHowManyJoinsChildrenIncluded, elements))

elements = parser.object_data[FILE].children
labels = list(map(lambda x: x.labelForChart[:40],elements))
nb = list(map(getHowManyJoinsChildrenIncluded, elements))

trace1 = go.Pie(labels=labels, values=nb)

# FIG 2

elements = parser.object_data[FILE].children

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