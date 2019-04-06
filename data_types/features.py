import numpy as np
from pandas import DataFrame


class Features:

    RED_INDEX = 0
    GREEN_INDEX = 1
    BLUE_INDEX = 2

    def __init__(self, rgb: list):
        assert len(rgb) == 3, "RGB must have 3 values."
        self.red = rgb[self.RED_INDEX]
        self.green = rgb[self. GREEN_INDEX]
        self.blue = rgb[self.BLUE_INDEX]
        self.luminance, self.saturation, self.hue = self.__calculate_hsl(np.array(rgb))
        self.intensity = np.array(rgb).mean()

    # def __init__(self, red, green, blue, luminance, saturation, hue, intensity):
    #     self.red = red
    #     self.green = green
    #     self.blue = blue
    #     self.luminance = luminance
    #     self.saturation = saturation
    #     self.hue = hue
    #     self.intensity = intensity

    def __calculate_hsl(self, rgb: np.array):
        assert rgb.size == 3, "RGB must have 3 values."
        normalized_rgb = rgb / 255
        normalized_red = normalized_rgb[self.RED_INDEX]
        normalized_green = normalized_rgb[self.GREEN_INDEX]
        normalized_blue = normalized_rgb[self.BLUE_INDEX]

        min_rgb = normalized_rgb.min()
        max_rgb = normalized_rgb.max()
        luminance = (min_rgb + max_rgb) / 2

        if min_rgb == max_rgb:
            return luminance, 0., 0.

        saturation = (max_rgb - min_rgb) / (max_rgb + min_rgb) if luminance < .5 else \
            (max_rgb - min_rgb) / (2. - max_rgb - min_rgb)

        max_rgb_arg = rgb.argmax()
        if max_rgb_arg == self.RED_INDEX:
            hue = (normalized_green - normalized_blue) / (max_rgb - min_rgb)
        elif max_rgb_arg == self.GREEN_INDEX:
            hue = 2. + (normalized_blue - normalized_red) / (max_rgb - min_rgb)
        elif max_rgb_arg == self.BLUE_INDEX:
            hue = 4. + (normalized_red - normalized_green) / (max_rgb - min_rgb)
        else:
            assert False, "Index of max_arg should be in [RED_INDEX, BLUE_INDEX]"

        hue *= 60
        hue = hue + 360 if hue < 0 else hue

        return luminance, saturation, hue

    def to_series(self):
        return DataFrame(
            data=[[self.red, self.green, self.blue, self.hue, self.luminance, self.saturation, self.intensity]],
            columns=list(["Red", "Green", "Blue", "Hue", "Luminance", "Saturation", "Intensity"]))
