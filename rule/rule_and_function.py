class RuleAndFunction:

    def __init__(self, rule, function):
        self.rule = rule
        self.function = function

    def fit_function(self, *args, **kwargs):
        self.function.fit(*args, **kwargs)
