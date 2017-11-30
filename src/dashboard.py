from JsonParser.json_parser import JsonParser
from JsonParser.dto.database_component import DBComponent
from SqlAnalyzer.SqlReport import SqlReport
from collections import Counter
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

# libs
def get_how_many_joins_children_included(element):
    res = 0
    if isinstance(element, DBComponent):
        res = res + element.sql_stats.nb_join
    if len(element.children) > 0:
        for c in element.children:
            res = res + get_how_many_joins_children_included(c)
    return res

def get_how_many_x(element, attribute):
    res = 0
    if(isinstance(element, DBComponent)):
        res = res + getattr(element.sql_stats, attribute)
    return res

def get_how_many_x_for_modules(element, attribute):
    res = {}
    if(element.project in res):
        res[element.project] += get_how_many_x(element, attribute)
    else:
        res[element.project] = get_how_many_x(element, attribute)
    
    for c in element.children:
        res = dict(Counter(res) + Counter(get_how_many_x_for_modules(c, attribute)))
    return res

def generate_dashboard(element):
    # FIG 1
    elements = element.children
    labels = list(map(lambda x: x.labelForChart[:40],elements))
    nb = list(map(get_how_many_joins_children_included, elements))

    trace = go.Bar(x=labels, y=nb)
    plot([trace], filename="bar.html")

    # FIG 2
    elements = element.children
    vals = {}
    for e in elements:
        vals = dict(Counter(vals) + Counter(get_how_many_x_for_modules(e, 'nb_join')))

    projects = list(vals.keys())
    nb = list(vals.values())

    trace = go.Pie(labels=projects, values=nb)
    plot([trace], filename="pie.html")