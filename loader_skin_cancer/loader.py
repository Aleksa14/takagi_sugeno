import cv2 as cv
import os
from feature_extraction.feature_extractor import FeatureExtractor
from data_types.record import Record

class Loader:

    PATH = 'F:\\images_preprocessed'

    def load_data(self):
        records = []
        for file in os.listdir(self.PATH):
            if file.endswith(".jpeg"):
                image = cv.imread(self.PATH + '\\' + file)
                is_cancer = file.startswith('xx')
                value = 1 if is_cancer else 0
                records.append(Record(FeatureExtractor(image).filter_img().extract_features(), value))
        return records
