from dto.component import Component


class DBComponent(Component):
    types = ['db', 'neutron.db']

    def __init__(self, name, project, duration, parent_id, trace_id,
                 host, params, statement,):
        super(DBComponent, self).__init__(name, project, duration,
                                          parent_id, trace_id)
        self.host = host
        self.params = params
        self.statement = statement

    def __str__(self):
        result = "DB_COMPONENT\n"

        result += super(DBComponent, self).__str__()

        result += "Host : " + self.host + "\n"
        result += "Statement : " + self.statement + "\n"
        result += "{"
        for param in self.params:
            result += param + ", "
        result += "}\n"
        for child in self.children:
            result += child.__str__() + '\n'
        return result
