
class Request:
    """ Parent class representing a HTTP or DB request """

    def __init__(self):
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
