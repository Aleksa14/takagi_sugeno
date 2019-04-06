from data_types.features import Features
from data_types.record import Record

if __name__ == "__main__":
    sut = Features([24, 98, 118])
    luminance = round(sut.luminance, 2)
    saturation = round(sut.saturation, 2)
    hue = round(sut.hue)
    assert luminance == .28, "Luminance calculated badly, val = " + str(luminance)
    assert saturation == .66, "Saturation calculated badly, val = " + str(saturation)
    assert hue == 193., "Hue calculated badly, val = " + str(hue)
    assert sut.red == 24, "Red assert, val = " + str(sut.red)
    assert sut.green == 98, "Green assert, val = " + str(sut.green)
    assert sut.blue == 118, "Blue assert, val = " + str(sut.blue)
    assert sut.intensity == 80, "Blue assert, val = " + str(sut.intensity)
    record = Record(sut, 1.0)
    print(record.to_series())
