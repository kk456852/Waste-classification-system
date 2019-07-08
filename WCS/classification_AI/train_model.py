import numpy as np
from load_data import load_data
#from keras.datasets import  mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
 

# 载入数据
(x_train,y_train),(x_test,y_test) = load_data()

print(x_train)
print('x_shape:', x_train.shape,x_test.shape)

print('y_shape:',y_train.shape)

x_train = x_train.reshape(x_train.shape[0],-1)/255.0
x_test = x_test.reshape(x_test.shape[0],-1)/255.0
# 换one hot格式
y_train = np_utils.to_categorical(y_train,num_classes=2)
y_test = np_utils.to_categorical(y_test,num_classes=2)
 
'''
model = Sequential([ Dense(units=2,input_dim=2352,bias_initializer='one',activation='softmax') ]) 
'''
model = Sequential()
model.add(Dense(512, input_shape=(2352,)))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(2))
model.add(Activation('softmax'))

# 定义优化器
sgd = SGD(lr=0.2)
 
# 定义优化器，loss function，训练过程中计算准确率
model.compile(
    optimizer = sgd,
    loss = 'mse',
    metrics=['accuracy'],
)
 
# 训练模型
model.fit(x_train,y_train,batch_size=20,epochs=100)
 
# 评估模型
loss,accuracy = model.evaluate(x_test,y_test)
 
print('\ntest loss',loss)
print('accuracy',accuracy)
 
# 保存模型
model.save('model.h5') 
