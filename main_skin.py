import pandas as pd
from model.fuzzifier import Fuzzifier
from data_types.stats import Stats
from model.reductor import Reductor
from model.model import Model
from model.resolver import Resolver
from loader_skin_cancer.loader import Loader
import cv2
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score
import sys

if __name__ == '__main__':
    # data = Loader().load_data()
    # dataset = data[0].to_series()
    # for t in range(1, len(data)):
    #     dataset = pd.concat([dataset, data[t].to_series()], ignore_index=True)
    # dataset.reindex()
    # print(dataset)
    # dataset.to_csv("skin_cancer_data.csv")
    dataset = pd.read_csv('skin_cancer_data.csv')
    dataset = dataset.drop("Index", axis=1)
    print(dataset)
    print("recursion limit", sys.getrecursionlimit())
    sys.setrecursionlimit(2000)
    kf = KFold(10)
    acc = []
    # train, validation = train_test_split(dataset, test_size=0.8)
    train = dataset
    for train_index, test_index in kf.split(train):
        cross_train = train.iloc[train_index]
        cross_test = train.iloc[test_index]
        stats = Stats(cross_train)
        dataset = Fuzzifier().fuzzify(cross_train, stats)
        cross_train = Resolver().resolve(cross_train)
        reductor = Reductor()
        cross_train = reductor.reduce(cross_train)
        print(reductor.reduct)
        model = Model(cross_train, stats, reductor.reduct, number_of_functions=100)
        test_fuzzified = Fuzzifier().fuzzify(cross_test, stats)
        # validation_fuzzified = Fuzzifier().fuzzify(validation, stats)
        truth = []
        # truth_val = []
        predicted = []
        # predicted_val = []
        for i, test_r in test_fuzzified.iterrows():
            print(test_r['Value'], "=", model.predict(test_r))
            truth.append(test_r['Value'])
            if model.predict(test_r) >= 0.5:
                predicted.append(1)
            else:
                predicted.append(0)
        print("Test acc", accuracy_score(truth, predicted))
        # for i, test_r in validation_fuzzified.iterrows():
        #     print(test_r['Value'], "=", model_test.predict(test_r))
        #     truth_val.append(test_r['Value'])
        #     if model_test.predict(test_r) >= 0.5:
        #         predicted_val.append(1)
        #     else:
        #         predicted_val.append(0)
        # print("Validation acc", accuracy_score(truth_val, predicted_val))
        # predicted = predicted + predicted_val
        # truth = truth + truth_val
        acc.append(accuracy_score(truth, predicted))
    print("Accuracy: ", acc)
    print(sum(acc) / len(acc))
