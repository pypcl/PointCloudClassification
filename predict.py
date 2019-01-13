# -*- coding:utf-8 -*-
# author:XueWang
# 用测试集来对训练的模型进行测试，计算识别准确率
import tensorflow as tf
import numpy as np
import sys
import os
import math
import provider
import keras
from keras.models import load_model
from keras.utils import plot_model

#load model
model1 = load_model('model/modelK17.h5') #load model

predict_data, predict_label = provider.load_h5('data/modelnet40_ply_hdf5_2048/ply_data_test1.h5')
predict_data = predict_data[:, 0:2048, :]
# predict_data, predict_label, _ = provider.shuffle_data(test_data, np.squeeze(test_label))
predict_data = predict_data[:, :, :, np.newaxis]  #(2048,2048,3)->(2048,2048,3,1)
predict_label = np.squeeze(predict_label)  #[[[0,1]]]->[0,1]
predict_label = keras.utils.to_categorical(predict_label, num_classes=40) #40*40 identity matrix
pre = model1.predict(predict_data, batch_size=32, verbose=1)
# print(pre)
# print("----\n",predict_label)
max_probability = 0.0
index1 = 0
index2 = 0
accuracy = 0

pre_objects = predict_data.shape[0]   #number of predict_data
for i in range(pre_objects):
	for j in range(40):
		if(pre[i][j] > max_probability):
			max_probability = pre[i][j]
			index1 = j
		if(predict_label[i][j] == 1):
			index2 = j
	print("i:",i," index1:",index1," index2:",index2,"max_probability: ",max_probability)
	if(index1 == index2):
		accuracy += 1
	max_probability = 0

print("\n\n",accuracy/predict_data.shape[0])