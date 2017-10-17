from dto.request import Request

class HTTPRequest(Request):
    """ Class encapsuling HTTP requests """

    def __init__(self, project, host, path, scheme, method, query, duration):
        super(HTTPRequest, self).__init__()
        self.project = project
        self.host = host
        self.path = path
        self.scheme = scheme
        self.method = method
        self.query = query
        self.duration = duration

    def __str__(self):
        result = ""
        result += 'HTTP_REQUEST' + '\n'
        result += self.project + '\n'
        result += self.host + '\n'
        result += self.path + '\n'
        result += self.scheme + '\n'
        result += self.method + '\n'
        result += self.query + '\n'
        result += self.duration + '\n'
        for child in self.children:
            result += str(child) + '\n'
        return result
