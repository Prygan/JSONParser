

class Stats(object):
    """Class containing stats information about """

    def __init__(self, name, count, duration):
        self.name = name
        self.count = count
        self.duration = duration

    def __str__(self):
        result = "Name : " + self.name + "\n"
        result += "Count : " + str(self.count) + "\n"
        result += "Duration : " + str(self.duration) + "\n"

        return result
