# match

INCREMENT_MINOR = 2000
INCREMENT_SMALL = 5000
INCREMENT_MEDIUM = 10000
INCREMENT_LARGE = 20000
URI_PENALTY = 15000

POOR = 50000
BELOW_AVERAGE = 60000
AVERAGE = 70000
ABOVE_AVERAGE = 75000
GOOD = 80000
VERY_GOOD = 85000
EXCELLENT = 90000

HIGHEST = 100000


class Match:
    def __init__(self, title, description): #, last_time, icon, score):
        self.title = title
        self.description = description
        #self.last_time = last_time
        #self.icon = icon
        #self.score = score
        # thumbnail_path
