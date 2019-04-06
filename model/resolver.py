import numpy as np

class Resolver:

    def resolve(self, dataset):
        fn = lambda obj: obj.loc[np.random.choice(obj.index, 1), :]
        return dataset.groupby([col for col in dataset if col.startswith('fuzzy')]).apply(fn)

    def are_fuzzy_same(self, record1, record2, dataset):
        for col in dataset:
            if col.startswith('fuzzy') and record1[col] != record2[col]:
                return False
        return True
