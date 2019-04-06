from train_generator.train__generator import TrainGenerator


if __name__ == "__main__":
    sut = TrainGenerator()
    (r, g, b), v = sut.generate_red_color()
    print(f"{r:x}{g:x}{b:x} {v}")

    print(sut.generate_train_set(5))