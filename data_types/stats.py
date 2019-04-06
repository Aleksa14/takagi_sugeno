import pandas as pd


class Stats:

    def __init__(self, dataset: pd.DataFrame):
        self.mean = self.initialize_mean(dataset)
        self.variances = self.initialize_variances(dataset)
        self.minimums = self.initialize_min(dataset)
        self.maximums = self.initialize_max(dataset)

    def initialize_mean(self, dataset):
        means = dict()
        for d in dataset:
            means[d] = dataset[d].mean()
        print(means)
        return means

    def initialize_variances(self, dataset):
        variances = dict()
        for d in dataset:
            var = 0.
            for _, row in dataset.iterrows():
                var += (pow(row[d] - self.mean[d], 2) / (len(dataset.index) - 1))
            variances[d] = var
        print(variances)
        return variances

    def initialize_min(self, dataset):
        mini = dict()
        for d in dataset:
            mini[d] = dataset[d].min()
        print(mini)
        return mini

    def initialize_max(self, dataset):
        maxi = dict()
        for d in dataset:
            maxi[d] = dataset[d].max()
        print(maxi)
        return maxi
