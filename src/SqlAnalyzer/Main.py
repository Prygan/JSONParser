import sys
from SqlAnalyser.SqlReport import SqlReport
from SqlAnalyser.SqlReportProcessor import SqlReportProcessor

if __name__ == '__main__':
    reporter = SqlReportProcessor()
    report = reporter.reportFromFile(sys.argv[1])

    print(report.generalReport)
