from os import listdir
from os.path import isfile, join
import cv2 as cv
from feature_extraction.feature_extractor import FeatureExtractor

class TestGenerator:

    IMAGE_PATH = 'C:\\Users\\olaor\\Desktop\\red_flowers'

    def chose_images(self):
        images = [cv.imread(join(self.IMAGE_PATH, f)) for f in listdir(self.IMAGE_PATH) if isfile(join(self.IMAGE_PATH, f)) and f.endswith('.png')]
        images = [img for img in images if img is not None]
        print(len(images))
        features = [(im, FeatureExtractor(im).extract_features_dominant()) for im in images]
        return features
