import numpy as np
import pickle
import cv2, os
from glob import glob
from keras import optimizers
from tensorflow.keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
from keras import backend as K
K.set_image_data_format('channels_last')

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def get_image_size():
	img = cv2.imread('gestures/1/1.jpeg', 0)
	return img.shape

def get_num_of_classes():
	print("Number of classes: ", glob('gestures/*'))
	return len(glob('gestures/*'))

image_x, image_y = get_image_size()

def cnn_model():
	'''
	num_of_classes = get_num_of_classes()
	model = Sequential()
	model.add(Conv2D(16, (2,2), input_shape=(image_x, image_y, 1), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
	model.add(Conv2D(32, (3,3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(3, 3), strides=(3, 3), padding='same'))
	model.add(Conv2D(64, (5,5), activation='relu'))
	model.add(MaxPooling2D(pool_size=(5, 5), strides=(5, 5), padding='same'))
	model.add(Flatten())
	model.add(Dense(128, activation='relu'))
	model.add(Dropout(0.2))
	model.add(Dense(num_of_classes, activation='softmax'))
	sgd = optimizers.SGD(lr=1e-2)
	model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

	num_of_classes = get_num_of_classes()  # Replace this with the correct number of classes
	model = Sequential()
	model.add(Conv2D(20, (3, 3), strides=(1,1), padding='valid', activation='relu', input_shape=(image_x, image_y, 1)))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Conv2D(20, (3, 3), strides=(1,1), padding='valid', activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Flatten())
	model.add(Dense(100, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(50, activation='relu'))
	model.add(Dense(num_of_classes, activation='softmax'))
	'''
	num_of_classes = get_num_of_classes()
	model = Sequential()
	model.add(Conv2D(16, kernel_size=(5, 5),
					 strides=1, padding='same', activation='relu', input_shape=(image_x, image_y, 1)))
	model.add(MaxPooling2D(pool_size=(3, 3), strides=2, padding='same'))
	model.add(Conv2D(32, kernel_size=(2, 2),
					 strides=1, activation='relu', padding='same'))
	model.add(MaxPooling2D((2, 2), 2, padding='same'))
	model.add(Conv2D(64, kernel_size=(2, 2),
					 strides=1, activation='relu', padding='same'))
	model.add(MaxPooling2D((2, 2), 2, padding='same'))

	model.add(Flatten())
	model.add(Dense(units=128, activation='relu'))
	model.add(Dropout(rate=0.5))
	model.add(Dense(units=num_of_classes, activation='softmax'))
	# Compile the model
	optimizer = optimizers.Adam(learning_rate=0.01)
	model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
	filepath="cnn_model_keras2.h5"
	checkpoint1 = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
	callbacks_list = [checkpoint1]
	#from keras.utils import plot_model
	#plot_model(model, to_file='model.png', show_shapes=True)
	return model, callbacks_list

def train():
	with open("train_images", "rb") as f:
		train_images = np.array(pickle.load(f))
	with open("train_labels", "rb") as f:
		train_labels = np.array(pickle.load(f), dtype=np.int32)

	with open("val_images", "rb") as f:
		val_images = np.array(pickle.load(f))
	with open("val_labels", "rb") as f:
		val_labels = np.array(pickle.load(f), dtype=np.int32)

	train_images = np.reshape(train_images, (train_images.shape[0], image_x, image_y, 1))
	val_images = np.reshape(val_images, (val_images.shape[0], image_x, image_y, 1))
	train_labels = np_utils.to_categorical(train_labels)
	val_labels = np_utils.to_categorical(val_labels)

	print(val_labels.shape)

	model, callbacks_list = cnn_model()
	model.summary()
	model.fit(train_images, train_labels, validation_data=(val_images, val_labels), epochs=5, batch_size=100, callbacks=callbacks_list)
	scores = model.evaluate(val_images, val_labels, verbose=0)
	print("CNN Error: %.2f%%" % (100-scores[1]*100))
	model.save('cnn_model_keras2.h5')

train()
K.clear_session();
