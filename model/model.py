import pandas as pd
from random import random, uniform

from rule.rule_function_buildier import RuleFunctionBuildier
from rule.rule import Rule
from rule.rule_and_function import RuleAndFunction

class Model:

    def __init__(self, dataset: pd.DataFrame, stats, reductors, number_of_functions=200):
        self.stats = stats
        self.number_of_functions = number_of_functions
        self.rule_and_functions = self.create_rule(dataset, reductors, stats)

    def create_rule(self, dataset, reductors, stats):
        differences = self.get_differences(dataset)
        return self.build_rules(dataset, reductors, differences, stats)

    # def build_rules(self, dataset, reductors, differences, stats):
    #     rule_functions = []
    #     key_list = list(reductors.keys())
    #     for i in range(int(pow(2, len(reductors)))):
    #         reductors_copied = deepcopy(reductors)
    #         for j in range(len(reductors_copied)):
    #             if (i & (1 << j)) != 0:
    #                 reductors_copied[key_list[j]] = -reductors_copied[key_list[j]]
    #         rule_functions.append(RuleFunctionBuildier(reductors_copied, stats).build())
    #     function_to_records = dict([(func, []) for func in rule_functions])
    #     for i, row in dataset.iterrows():
    #         function_to_records[self.choose_best_function(row, rule_functions)].append((row, i))
    #     rule_and_function = []
    #     for f in function_to_records:
    #         row = function_to_records[f]
    #         rule_and_function.append(self.build_rule(differences, row, f))
    #     return rule_and_function

    def build_rules(self, dataset, reductors, differences, stats):
        rule_functions = []
        for i in range(self.number_of_functions):
            # rule_functions.append(self.build_random_rule(reductors, dataset, stats))
            rule_functions.append(self.build_function_from_LR(dataset, stats))
        function_to_records = dict([(func, []) for func in rule_functions])
        for i, row in dataset.iterrows():
            function_to_records[self.choose_best_function(row, rule_functions)].append((row, i))
        for func in function_to_records:
            records = function_to_records[func]
            filtered_records = []
            for r in records:
                if not self.is_in_fuzzy(filtered_records, r, dataset):
                    filtered_records.append(r)
            print("len(filtered_records}", len(filtered_records))
            function_to_records[func] = filtered_records
            # if len(records) > 0:
            #     func.fit(records)
        rule_and_function = []
        for f in function_to_records:
            row = function_to_records[f]
            rule = self.build_rule(differences, row, f)
            if rule is not None:
                rule_and_function.append(rule)
        return rule_and_function

    def is_in_fuzzy(self, records_list, record, dataset):
        for list_record in records_list:
            if self.are_fuzzy_same(record[0], list_record[0], dataset):
                return True
        return False

    def are_fuzzy_same(self, record1, record2, dataset):
        for column in dataset:
            if column.startswith('fuzzy') and record1[column] != record2[column]:
                return False
        return True

    def build_random_rule(self, reductors, dataset, stats):
        random_factors = [uniform(-50, 50) for _ in range(len(reductors))]
        random_factors = sorted(random_factors)
        sorted_reductors = sorted(reductors.items(), key=lambda kv: kv[1])
        sorted_features = [x[0] for x in sorted_reductors]
        new_factors = dict(zip(sorted_features, random_factors))
        return RuleFunctionBuildier(new_factors, stats).build()

    def build_function_from_LR(self, dataset, stats):
        func = None
        while func is None:
            records = []
            for record in dataset.iterrows():
                if random() < 0.10:
                    records.append((record[1], record[0]))
            factors = dict([(col, 0.0) for col in dataset if col.startswith('fuzzy')])
            factors["B"] = 0.0
            if len(records) > 0:
                func = RuleFunctionBuildier(factors, stats).build().fit(records)
        return func


    def build_rule(self, differences, records, rule_function):
        alternative = None
        for r, i in records:
            conjunction = self.get_implicants(differences, r, i)
            if alternative is None and conjunction is not None:
                alternative = conjunction
            elif conjunction is not None:
                alternative = ['OR'] + alternative + conjunction
        return None if alternative is None else RuleAndFunction(Rule(alternative), rule_function)

    def get_implicants(self, differences, record, index):
        conjuction = None
        # print(record)
        diff_copy = []
        for df in differences[index]:
            if df not in diff_copy:
                diff_copy.append(df)
        for diff in diff_copy:
            alternative = None
            for a in diff:
                if alternative is None:
                    alternative = [a + "=" + record[a].name]
                elif a + "=" + record[a].name not in alternative:
                    alternative = ['OR'] + alternative + [a + "=" + record[a].name]
            if conjuction is None and alternative is not None:
                conjuction = alternative
            elif alternative is not None:
                conjuction = ['AND'] + conjuction + alternative
        return None if conjuction is None else conjuction

    def get_differences(self, dataset):
        differences = dict()
        for i, row in dataset.iterrows():
            first = row
            differences[i] = []
            for j, row2 in dataset.iterrows():
                second = row2
                if i == j:
                    continue
                difference = [attr for attr in dataset if 'fuzzy' in attr and first[attr] != second[attr]]
                if len(differences) != 0:
                    differences[i].append(difference)
        return differences

    def choose_best_function(self, record, rule_funcs):
        return min(rule_funcs, key= lambda f: abs(f.apply(record) - record['Value']))

    def get_probability_for(self, record):
        pass

    def predict(self, record):
        sum_w = 0
        summ = 0
        context = record, self.stats, self.stats
        for rf in self.rule_and_functions:
            if rf is not None:
                rule_val = rf.rule.evaluate2(context)
                # rule_val = 1.0
                func_val = rf.function.apply(record)
                func_val = 1.0 if func_val > 1.0 else 0.0 if func_val < 0.0 else func_val
                print("function value", func_val)
                print("rule value", rule_val)
                summ += (func_val * rule_val)
                sum_w += rule_val
        return summ / sum_w
