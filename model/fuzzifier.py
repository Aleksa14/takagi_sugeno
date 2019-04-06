from enum import Enum
from math import exp, pow
import pandas as pd
from data_types.features import Features

class Fuzzifier:

    class fuzzyset(Enum):
        def __lt__(self, other):
            return self.value < other.value
        def __le__(self, other):
            return self.value <= other.value

        LOW = 'LOW'
        MEDIUM = 'MEDIUM'
        HIGH = 'HIGH'

    def __init__(self):
        pass

    def get_pdf_for_fuzzyset(self, fuzzyset, mean, first_variance, second_variance, value):
        if fuzzyset == self.fuzzyset.LOW:
            result = 0. if value > mean else 1. - self.get_pdf(mean, second_variance, value)
            # print(value, " ", fuzzyset, " ", result)
            return result
        elif fuzzyset == self.fuzzyset.MEDIUM:
            result = self.get_pdf(mean, first_variance, value)
            # print(value, " ", fuzzyset, " ", result)
            return result
        elif fuzzyset == self.fuzzyset.HIGH:
            result = 0. if value < mean else 1. - self.get_pdf(mean, second_variance, value)
            # print(value, " ", fuzzyset, " ", result)
            return result
        else:
            return "Set does not exist"

    def get_pdf(self, mean, variance, value):
        return exp(-(pow(value - mean, 2)) / (2 * variance))

    def get_best_fuzzy_value(self, stats, col_name, col_val):
        return max(list(self.fuzzyset), key=lambda fuzzy_val: self.get_pdf_for_fuzzyset(fuzzy_val, stats.mean[col_name], stats.variances[col_name], stats.variances[col_name], col_val))

    def fuzzify(self, dataset: pd.DataFrame, stats):
        for f in dataset:
            if f == 'value':
                continue
            dataset['fuzzy_' + f] = self.fuzzyset.LOW.name
        for i, row in dataset.iterrows():
            for f in dataset:
                if 'fuzzy' in f or f == 'Value':
                    continue
                # print(f)
                dataset.at[i, 'fuzzy_' + f] = self.get_best_fuzzy_value(stats, f, row[f])
                # dataset.at[i, 'fuzzy_' + f] = "HIGH"
                # print("elelelele")
                # print("i", i)
                # print(dataset)
                # return dataset
        return dataset

    @staticmethod
    def get_fuzzy_features(dataset: pd.DataFrame):
        return dataset[['fuzzy' in dataset.columns]]
