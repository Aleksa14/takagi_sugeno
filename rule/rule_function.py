from copy import deepcopy
import numpy as np
from sklearn.linear_model import LinearRegression

class RuleFunction:

    def __init__(self, factors, representation):
        print("Create rule with factors:", factors)
        self.factors = deepcopy(factors)
        self.representation = representation

    def apply(self, record):
        result = 0.0
        for k in self.factors:
            if k != "B":
                k1 = k.split("_")[1]
                result += self.factors[k] * record[k1]
            else:
                result += self.factors[k]
        return result

    def str(self):
        return self.representation

    def fit(self, records, eta=0.005, n_iterations=1000):
        # print(type(records), type(records[0]), type(records[0][1]))
        x = []
        for record, _ in records:
            x_record = []
            for k in self.factors:
                if k != "B":
                    k1 = k.split("_")[1]
                    x_record.append(record[k1])
                else:
                    x_record.append(1.0)
            x.append(x_record)
        x = np.array(x)
        x = x.reshape((len(records), len(self.factors)))
        y = np.array([record[0]['Value'] for record in records])
        w = np.array([self.factors[k] for k in self.factors])
        lr = LinearRegression()
        lr.fit(x, y)

        # for _ in range(n_iterations):
        #     y_pred = np.dot(x, w)
        #     residuals = y_pred - y
        #     print("residals", residuals)
        #     gradint_vector = np.dot(x.T, residuals)
        #     if 'inf' in gradint_vector:
        #         break
        #     print("gradient vector", gradint_vector)
        #     w -= (eta / x.shape[0]) * gradint_vector
        #     print("w", w)
        for i, k in enumerate(self.factors):
            self.factors[k] = lr.coef_[i]
        self.factors["B"] += lr.intercept_
        print("new factors after fitting =", self.factors)
        return self
