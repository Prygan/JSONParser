from JsonParser.json_parser import JsonParser
from JsonParser.dto.database_component import DBComponent
from SqlAnalyzer.SqlReport import SqlReport
from collections import Counter
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

FILE = 'files/trace-create-and-delete-image.yaml.json'
# FILE = 'trace-report-boot-and-associate-floating-ip.yaml-f7a3b33f-d2e4-4c6c-8bf0-3782b7b675f8.json' 


# libs
def getHowManyJoinsChildrenIncluded(element):
    res = 0
    if(isinstance(element, DBComponent)):
        res = res + element.sql_stats.nb_join
    if(element.children != []):
        for c in element.children:
            res = res + getHowManyJoinsChildrenIncluded(c)
    return res

def getHowManyX(element, attribute):
    res = 0
    if(isinstance(element, DBComponent)):
            res = res + getattr(element.sql_stats, attribute)
    return res

def getHowManyXForModules(element, attribute):
    res = {}
    if(element.project in res):
        res[element.project] += getHowManyX(element, attribute)
    else:
        res[element.project] = getHowManyX(element, attribute)
    for c in element.children:
        res = dict(Counter(res) + Counter(getHowManyXForModules(c, attribute)))
    return res


init_notebook_mode(connected=True)

parser = JsonParser([FILE])
parsedFile = parser.files[0]
print("--- Fichier analysé : " + parsedFile)
parser.extract_from_json()

# FIG 1

elements = parser.object_data['trace-create-and-delete-image.yaml.json'].children
labels = list(map(lambda x: x.labelForChart[:40],elements))
nb = list(map(getHowManyJoinsChildrenIncluded, elements))

trace = go.Bar(x=labels, y=nb)
plot([trace], filename="bar.html")

# FIG 2

elements = parser.object_data['trace-create-and-delete-image.yaml.json'].children

vals = {}

for e in elements:
    vals = dict(Counter(vals) + Counter(getHowManyXForModules(e, 'nb_join')))

projects = list(vals.keys())
nb = list(vals.values())


trace = go.Pie(labels=projects, values=nb)
plot([trace], filename="pie.html")