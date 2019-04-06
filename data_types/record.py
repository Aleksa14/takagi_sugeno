from data_types.features import Features
from pandas import Series


class Record:

    def __init__(self, featurs: Features, value = None):
        self.features = featurs
        self.value = value

    def to_series(self):
        frame = self.features.to_series()
        frame["Value"] = Series(self.value)
        return frame
