
class Stats:
    """ Class containing stats information about """

    def __init__(self, count, duration):
        self.count = count
        self.duration = duration

    def __str__(self):
        result = 'STATS\n'
        result += 'count : ' + str(self.count) + '\n'
        result += 'duration : ' + str(self.duration) + '\n'

        return result
