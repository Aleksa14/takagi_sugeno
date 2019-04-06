import pandas as pd
from data_types.stats import Stats

if __name__ == "__main__":
    d = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
    df = pd.DataFrame(data=d)
    print(df)
    stats = Stats(df)
    print(stats.mean)
    print(stats.variances)
    print(stats.minimums)
    print(stats.maximums)
