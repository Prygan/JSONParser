import sys
from SqlAnalyzer.SqlReport import SqlReport
from antlr4 import *
from SqlAnalyzer.parser.SqlLexer import SqlLexer
from SqlAnalyzer.parser.SqlParser import SqlParser
from SqlAnalyzer.parser.SqlListener import SqlListener
from SqlAnalyzer.Metrics import Metrics

class SqlReportProcessor:
    generalReport = SqlReport()

    def reportFromFile(self, path):
        with open(path, 'r') as file:
            self.reportFromArray(file)

    def reportFromArray(self, requests):
        report = SqlReport()

        for request in requests:
            report.mergeReport(self.report(request))
        
        return report


    def report(self, request):
        report = SqlReport()

        tree = SqlParser(CommonTokenStream(SqlLexer(InputStream(request)))).sql_stmt()
        walker = ParseTreeWalker()
        metrics = Metrics()
        walker.walk(metrics, tree)

        report.nb_join += metrics.howManyJoins()
        report.nb_transac += metrics.howManyTransactions()
        report.is_compound_select += metrics.isCompoundSelect()
        self.generalReport.mergeReport(report)
        return report

