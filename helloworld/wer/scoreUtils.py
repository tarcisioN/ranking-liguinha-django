from math import log

PERCENT_DIFF_OVER_5 = 2.35

PERCENT_DIFF_5 = 2.3

PERCENT_DIFF_4 = 2.2

PERCENT_DIFF_3 = 2.0

PERCENT_DIFF_2 = 1.7

PERCENT_DIFF_1 = 1

PERCENT_DIFF_MINUS_1 = 0.50

PERCENT_DIFF_MINUS_2 = 0.45

PERCENT_DIFF_MINUS_2 = 0.35

PERCENT_DIFF_MINUS_3 = 0.20

PERCENT_DIFF_LESS_MINUS_3 = 0.5


class Score:

    def __init__(self, factor, factor2):
        self.factor = factor
        self.factor2 = factor2

    def score_factor(self, x):
        return ((x/10.0) * self.factor2/10.0) + (log(x + 1) / log(x + self.factor))

    def score(self, x):
        return self.score_factor(x) * (self.score_factor(1)**-1)

    def score_v2(self, vw_score):
        if vw_score < -3:
            return PERCENT_DIFF_LESS_MINUS_3
        elif vw_score == -3:
            return PERCENT_DIFF_MINUS_3
        elif vw_score == -2:
            return PERCENT_DIFF_MINUS_2
        elif vw_score == -1:
            return PERCENT_DIFF_MINUS_2
        elif vw_score == 0:
            return PERCENT_DIFF_MINUS_1
        elif vw_score == 1:
            return PERCENT_DIFF_1
        elif vw_score == 2:
            return PERCENT_DIFF_2
        elif vw_score == 3:
            return PERCENT_DIFF_3
        elif vw_score == 4:
            return PERCENT_DIFF_4
        elif vw_score == 5:
            return PERCENT_DIFF_5
        else:
            return PERCENT_DIFF_OVER_5


if __name__ == '__main__':

    s = Score(3,1)

    for x in range(0,30):
        print(s.score(x))
