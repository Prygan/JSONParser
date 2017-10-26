
class Component:
    def __init__(self, name, service, duration, parent_id, trace_id):
        self.name = name
        self.service = service
        self.duration = duration
        self.children = []
        self.trace_id = trace_id
        self.parent_id = parent_id
    
    def add_child(self, child):
        self.children.append(child)
