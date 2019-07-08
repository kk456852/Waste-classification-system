from PIL import Image
import csv
import numpy as np
def load_data():
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    with open("data.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            line = list(map(eval, line))
            y_train.append(line[0])
            x_train.append([line[i: i + 84] for i in range(1, len(line), 84)])
        x_test = x_train[0:20]
        y_test = y_train[0:20]
        x_train = np.array(x_train)
        x_test = np.array(x_test)
        y_train = np.array(y_train)
        y_test = np.array(y_test)
    return (x_train,y_train),(x_test,y_test)

def load_pic(path):
    image_test = Image.open(path)
    image_test = image_test.resize((28, 28), Image.ANTIALIAS)
    matrix = np.asarray(image_test)
    matrix = matrix.reshape(-1) / 255.0
    return matrix

    

        