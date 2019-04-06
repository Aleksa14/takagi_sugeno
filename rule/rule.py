from model.fuzzifier import Fuzzifier
from copy import deepcopy


class Rule:

    # def __init__(self, left, right, operand):
    #     self.left = left
    #     self.right = right
    #     self.operand = operand

    def __init__(self, operands_list: list):
        self.operations = operands_list

    # def evaluate(self, context, i=0):
    #     leftValue = self.getValue(self.left, context, i)
    #     rightValue = self.getValue(self.right, context, i)
    #     if self.operand == "OR":
    #         return max(leftValue, rightValue)
    #     elif self.operand == "AND":
    #         return min(leftValue, rightValue)
    #     assert False, "Operation operand not supported."

    def getValue(self, operation, context):
        if isinstance(operation, str):
            record, stats, invertedStats = context
            entry = operation.split("=")
            attribute = entry[0].split("_")[1]
            fuzzySet = Fuzzifier.fuzzyset[entry[1]]
            value = record[attribute]
            return Fuzzifier().get_pdf_for_fuzzyset(
                fuzzySet, stats.mean[attribute], stats.variances[attribute],
                invertedStats.variances[attribute], value)
        # if isinstance(operation, Rule):
        #     return operation.evaluate(context, i+1)
        elif isinstance(operation, float):
            return operation
        assert False, "Operation type not supported " + type(operation).__name__

    def last(self, ls, value_list):
        for i in range(len(ls) - 1, -1, -1):
            if ls[i] in value_list:
                return i
        raise ValueError(str(value_list), ' any not found.')

    def evaluate2(self, context):
        op = deepcopy(self.operations)
        # ['OR', 'AND', 'f1=HIGH', 'f2=LOW', 'AND', 'f1=LOW', 'f2=MEDIUM']
        while len(op) > 1:
            # print(op)
            # print("operation lengths", len(op))
            operations_idx = self.last(op, ["AND", "OR"])
            # print("i", op[operations_idx])
            # print("i+1", op[operations_idx+1])
            # print("i+2", op[operations_idx+2])
            left_value = self.getValue(op[operations_idx + 1], context)
            right_value = self.getValue(op[operations_idx + 2], context)
            if op[operations_idx] == "AND":
                value = min(left_value, right_value)
            elif op[operations_idx] == "OR":
                value = max(left_value, right_value)
            else:
                assert False, "Operation operand not supported " + oparands_copy[operations_idx]
            # print(op)
            op = op[:operations_idx] + [value] + op[operations_idx+3:]
            # print(op)
        # print(self.operations)
        return op[0]

