class SqlReport:

    def __init__(self, nb_join = 0, nb_transac = 0, is_compound_select = False):
        self.nb_join = nb_join
        self.nb_transac = nb_transac
        self.is_compound_select = is_compound_select

    def mergeReport(self, report):
        self.nb_join = report.nb_join
        self.nb_transac = report.nb_transac
        self.is_compound_select = report.is_compound_select

    def __str__(self):
        result = "DB_Stats\n"
        result += "Nb join : " + str(self.nb_join) + "\n"
        result += "Nb transactions : " + str(self.nb_transac) + "\n"
        result += "Is compound select : " + str(self.is_compound_select) + "\n"
        return result
