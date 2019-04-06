import pandas as pd
from train_generator.train__generator import TrainGenerator
from test_generrator.test_generator import TestGenerator
from model.fuzzifier import Fuzzifier
from data_types.stats import Stats
from model.reductor import Reductor
from model.model import Model
import cv2

if __name__ == '__main__':
    train_gen = TrainGenerator()
    train = train_gen.generate_train_set(80)
    dataset = train[0].to_series()
    for t in range(1, len(train)):
        dataset = pd.concat([dataset, train[t].to_series()], ignore_index=True)
    dataset.reindex()
    stats = Stats(dataset)
    dataset = Fuzzifier().fuzzify(dataset, stats)
    reductor = Reductor()
    dataset = reductor.reduce(dataset)
    print(reductor.reduct)
    model = Model(dataset, stats, reductor.reduct)
    test = TestGenerator().chose_images()
    records = []
    for img, t in test:
        df = t.to_series()
        df = Fuzzifier().fuzzify(df, stats)

        for _, r in df.iterrows():
            records.append((model.predict(r), img))
    records = sorted(records, key=lambda r: r[0])
    for pred, img in records:
        cv2.imshow(str(pred), img)
        cv2.waitKey(0)
