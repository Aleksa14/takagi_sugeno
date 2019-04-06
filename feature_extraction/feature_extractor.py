import numpy as np
from data_types.features import Features
import cv2
from copy import deepcopy

class FeatureExtractor:

    def __init__(self, image: np.ndarray):
        self.image = image

    def extract_features(self):
        rs = self.image[:, :, 0]
        gs = self.image[:, :, 1]
        bs = self.image[:, :, 2]
        mean_rs = rs.mean()
        mean_gs = gs.mean()
        mean_bs = bs.mean()
        return Features([mean_rs, mean_gs, mean_bs])

    def extract_features_dominant(self):
        pixels = np.float32(self.image.reshape(-1, 3))

        n_colors = 3
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS

        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)
        dominant = palette[np.argmax(counts)]
        img = deepcopy(self.image)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                img[i, j, 1] = dominant[1]
                img[i, j, 2] = dominant[2]
                img[i, j, 0] = dominant[0]

        print(img)
        cv2.imshow("m", img)
        cv2.waitKey(0)
        cv2.imshow("k", self.image)
        cv2.waitKey(0)
        return Features(dominant)

    def filter_img(self):
        img = np.array([])
        for i, row in enumerate(self.image):
            for j, pixel in enumerate(row):
                if pixel[0] != 0 or pixel[1] != 0 or pixel[2] != 0:
                    img = np.append(img, pixel)
        # print(img.reshape((1, -1, 3)), img)
        self.image = img.reshape((1, -1, 3))
        return self
