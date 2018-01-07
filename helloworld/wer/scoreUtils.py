from math import log

class Score:

    def __init__(self, factor, factor2):
        self.factor = factor
        self.factor2 = factor2

    def score_factor(self, x):
        return ((x/10.0) * self.factor2/10.0) + (log(x + 1) / log(x + self.factor))

    def score(self, x):
        return self.score_factor(x) * (self.score_factor(1)**-1)

if __name__ == '__main__':

    s = Score(3,1)

    for x in range(0,30):
        print(s.score(x))
