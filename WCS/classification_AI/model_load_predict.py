import numpy as np
from keras.models import load_model
from keras.datasets import  mnist
MDOEL_PATH = "model.h5"



print("------------Loading_model---------------")
model = load_model(MDOEL_PATH)
print("------------Loading_data---------------")

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(x_train.shape[0],-1)/255.0
x_test = x_test.reshape(x_test.shape[0], -1) / 255.0


print(model.predict(x_test[:]))