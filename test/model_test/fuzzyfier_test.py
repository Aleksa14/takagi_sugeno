from model.fuzzifier import Fuzzifier
from data_types.stats import Stats
import pandas as pd

if __name__ == "__main__":
    d = {'red': [-10, 1, 2, 5000], 'green': [-10, 4, 5, 20], 'blue': [-20, 5, 6, 15], 'luminance': [-1, 8, 1, 10], 'value': [3, 5, 4, 3]}
    df = pd.DataFrame(data=d)
    stats = Stats(df)
    fuzzy = Fuzzifier().fuzzify(df, stats)
    print(fuzzy['fuzzy_red'])
