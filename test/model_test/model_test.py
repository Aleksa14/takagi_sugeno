from model.model import Model
from data_types.stats import Stats
from model.reductor import Reductor
from rule.rule_function_buildier import RuleFunctionBuildier
import pandas as pd

if __name__ == '__main__':
    d = {'red': [-10], 'green': [-10, 4, 5], 'blue': [-20], 'luminance': [-1],
         'value': [3]}
    df = pd.DataFrame(data=d)
    stats = Stats(df)
    # reductor = Reductor()
    # df = reductor.reduce(d
    # rule_functions = [RuleFunctionBuildier(reductor.reduct, )]
    # model_test = Model(df, stats, reductor)
    # for _, row in df.iterrows():
    #     print(model_test.choose_best_function(row, reductor, ))