from antlr4 import *
from antlr4.xpath.XPath import XPath
from antlr4.tree.ParseTreePattern import ParseTreePattern 
from SqlAnalyzer.parser.SqlLexer import SqlLexer
from SqlAnalyzer.parser.SqlParser import SqlParser
from SqlAnalyzer.parser.SqlListener import SqlListener

# REQUEST = 'SELECT worked FROM ( SELECT worked FROM A )'
REQUEST = 'SELECT 1'

lexer = SqlLexer(InputStream(REQUEST))
token = CommonTokenStream(lexer)
parser = SqlParser(token)
tree = parser.sql_stmt()

print(tree.toStringTree(recog=parser))

print('\n ------------ \n')

p = parser.compileParseTreePattern("literal_value 1", parser.literal_value)
m = p.match(tree)
#print(m.succeded())

# print(XPath.findAll(tree, "/sql_stmt/factored_select_stmt/select_core/result_column/expr/literal_value", parser))