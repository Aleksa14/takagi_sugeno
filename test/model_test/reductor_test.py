from model.reductor import Reductor
import pandas as pd


if __name__ == '__main__':
    d = {'fuzzy_red': [0, 0, 0, 0], 'fuzzy_green': [0, 2, 0, 1], 'fuzzy_blue': [0, 2, 0, 1],
         'fuzzy_luminance': [0, 0, 1, 2]}
    df = pd.DataFrame(data=d)
    reductor = Reductor().reduce(df)
    print(reductor)
