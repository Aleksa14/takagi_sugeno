from random import randint
from data_types.features import Features
from data_types.record import Record


class TrainGenerator:

    RED_PALLET = [[0xff, 0x99, 0xcc], [0xff, 0x66, 0x99], [0xff, 0x33, 0x99], [0xff, 0x00, 0x66], [0xff, 0x50, 0x50],
                  [0xff, 0x33, 0x00], [0xff, 0x00, 0x00], [0xcc, 0x00, 0x00]]

    def generate_red_color(self):
        color_intensity = 0.0
        color_chosen = [0.0, 0.0, 0.0]
        for _ in range(10):
            index = randint(0, len(self.RED_PALLET) - 1)
            color_chosen[0] += self.RED_PALLET[index][0]
            color_chosen[1] += self.RED_PALLET[index][1]
            color_chosen[2] += self.RED_PALLET[index][2]
            color_intensity += index / len(self.RED_PALLET)
        color_chosen[0] /= 10
        color_chosen[1] /= 10
        color_chosen[2] /= 10
        color_intensity /= 10
        color_chosen[0] = int(color_chosen[0])
        color_chosen[1] = int(color_chosen[1])
        color_chosen[2] = int(color_chosen[2])
        return color_chosen, color_intensity

    def generate_train_set(self, set_size):
        generated = [self.generate_red_color() for _ in range(set_size)]
        return [Record(Features(rgb), val) for (rgb, val) in generated]

