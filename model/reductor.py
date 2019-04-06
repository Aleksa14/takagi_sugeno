import pandas as pd
from model.fuzzifier import Fuzzifier
import operator


class Reductor:

    def __init__(self):
        self.reduct = None

    def reduce(self, dataset: pd.DataFrame):
        differences = self.get_differences(dataset)
        self.reduct = self.get_reducts(differences)
        new_attributes = self.get_new_attributes(differences)
        for d in dataset:
            if 'fuzzy' in d and d not in new_attributes:
                dataset = dataset.drop([d], axis=1)
        return dataset

    def get_differences(self, dataset: pd.DataFrame):
        differences = []
        for i, row in dataset.iterrows():
            for j, row2 in dataset.iterrows():
                if j <= i:
                    continue
                difference = [col_name for col_name in dataset if 'fuzzy' in col_name and row[col_name] != row2[col_name]]
                if len(difference) != 0:
                    differences.append(difference)
        return differences

    def get_reducts(self, differences):
        counts = {}
        for row in differences:
            for feature in row:
                if feature not in counts:
                    counts[feature] = 1
                else:
                    counts[feature] += 1
        return counts

    def get_new_attributes(self, differences):
        new_attributes = []
        while len(differences) != 0:
            attribute = max(self.get_reducts(differences).items(), key=operator.itemgetter(1))[0]
            new_attributes.append(attribute)
            differences = [diff for diff in differences if attribute not in diff]
        print("new attributes", new_attributes)
        return new_attributes
