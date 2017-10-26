from dto.request import Request

class DBRequest(Request):
    """ Class encapsuling DB requests """

    def __init__(self, project, host, duration, params, statement, parent_id, trace_id):
        super(DBRequest, self).__init__(parent_id, trace_id)
        self.project = project
        self.host = host
        self.duration = duration
        self.params = params
        self.statement = statement

    def __str__(self):
        result = 'DB_REQUEST\n'
        result += self.project + '\n'
        result += self.host + '\n'
        result += self.duration + '\n{'
        for param in self.params:
            result += param + ', '
        result += '}\n' + self.statement + '\n'
        for child in self.children:
            result += child.__str__() + '\n'
        return result
