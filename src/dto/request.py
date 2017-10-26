
class Request:
    """ Parent class representing a HTTP or DB request """

    def __init__(self, parent_id, trace_id):
        self.children = []
        self.trace_id = trace_id
        self.parent_id = parent_id
    
    def add_child(self, child):
        self.children.append(child)
