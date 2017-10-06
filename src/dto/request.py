
class Request:
    """ Class representing information about a SQL request"""

    def __init__(self, statement, duration):
        self.__statement = statement
        self.__duration = duration
        print(duration) 
