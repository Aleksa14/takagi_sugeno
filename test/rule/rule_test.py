from rule.rule import Rule
import pandas as pd
from model.fuzzifier import Fuzzifier
from data_types.stats import Stats

if __name__ == "__main__":
    d = {'red': [-10, 1, 2, 5000], 'green': [-10, 4, 5, 20], 'blue': [-20, 5, 6, 15], 'luminance': [-1, 8, 1, 10],
         'value': [3, 5, 4, 3]}
    df = pd.DataFrame(data=d)
    stats = Stats(df)
    fuzzy = Fuzzifier().fuzzify(df, stats)
    rule = Rule(["AND", "OR", "fuzzy_blue=LOW", "fuzzy_red=HIGH", "OR", "fuzzy_blue=HIGH", "fuzzy_red=MEDIUM"])
    for _, r in df.iterrows():
        print(rule.evaluate2((r, stats, stats)))
