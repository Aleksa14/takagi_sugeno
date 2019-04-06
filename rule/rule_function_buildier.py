from rule.rule_function import RuleFunction
from random import randrange, uniform


class RuleFunctionBuildier:

    def __init__(self, factors, stats):
        self.factors = factors
        self.stats = stats

    def build(self):
        minimum = 0
        maximum = 0
        for key in self.factors:
            if key == 'B':
                continue
            key1 = key.split("_")[1]
            if self.factors[key] >= 0:
                maximum += self.factors[key] * self.stats.maximums[key1]
                minimum += self.factors[key] * self.stats.minimums[key1]
            else:
                maximum += self.factors[key] * self.stats.minimums[key1]
                minimum += self.factors[key] * self.stats.maximums[key1]
        f_min = minimum
        f_max = maximum

        b_max = -f_min+1
        b_min = -f_max
        b = uniform(b_min, b_max)
        self.factors["B"] = b

        representation = "f(attr) = "
        for key in self.factors:
            if key == 'B':
                continue
            print(key)
            key1 = key.split("_")[1]
            representation += str(self.factors[key]) + " * " + key1 + " + "
        representation += str(b)
        return RuleFunction(self.factors, representation)
