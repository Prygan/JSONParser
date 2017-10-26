from dto.component import Component

class HTTPComponent(Component):
    types = ['wsgi']

    def __init__(self, project, host, path, scheme, method, query, name, service, duration, parent_id, trace_id):
        super(HTTPComponent, self).__init__(name, service, duration, parent_id, trace_id)
        self.project = project
        self.host = host
        self.path = path
        self.scheme = scheme
        self.method = method
        self.query = query

    def __str__(self):
        result = ""
        result += 'HTTP_COMPONENT' + '\n'
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
