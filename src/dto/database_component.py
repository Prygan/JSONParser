from dto.component import Component

class DBComponent(Component):
    types = ['db', 'neutron.db']

    def __init__(self, project, host, params, statement, name, service, duration, parent_id, trace_id):
        super(DBComponent, self).__init__(name, service, duration, parent_id, trace_id)
        self.project = project
        self.host = host
        self.params = params
        self.statement = statement

    def __str__(self):
        result = 'DB_COMPONENT\n'
        result += self.project + '\n'
        result += self.host + '\n'
        result += self.duration + '\n{'
        for param in self.params:
            result += param + ', '
        result += '}\n' + self.statement + '\n'
        for child in self.children:
            result += child.__str__() + '\n'
        return result
