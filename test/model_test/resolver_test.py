from model.resolver import Resolver
import pandas as pd

if __name__ == '__main__':
    d = {'fuzzy_col1': [1, 1, 2, 2], 'fuzzy_col2': [2, 2, 3, 3], 'col3': [1, 2, 3, 4]}
    df = pd.DataFrame(data=d)
    print(Resolver().resolve(df))
