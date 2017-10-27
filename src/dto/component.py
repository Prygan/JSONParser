class Component:
    def __init__(self, name, project, duration, parent_id, trace_id):
        self.name = name
        self.project = project
        self.duration = duration
        self.children = []
        self.trace_id = trace_id
        self.parent_id = parent_id
    
    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        result = ""
        result += "Name : " + self.name + "\n"
        result += "Project : " + self.project + "\n"
        result += "Duration : " + self.duration + "\n"
        result += "Trace id : " + self.trace_id + "\n"
        result += "Parent id : " + self.parent_id + "\n"

        return result