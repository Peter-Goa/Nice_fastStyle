import cv2
import tensorflow as tf
from im_transf_net import create_net
import numpy as np
from utils_sever import *
import os
import utils
import time

#File addressed
base_path = '../image/' #the root direction
Image_file = os.path.join(base_path,'fore.png')
Image_check = os.path.join(base_path,'row')
Genered_file = os.path.join(base_path,'after.png')
Genered_check = os.path.join(base_path,'gen')
Style_file = os.path.join(base_path,'style')
Style_new_file = os.path.join(base_path,'style_new')

#Model
Model_1 = os.path.join(model_path,model_name_set[0]+'.ckpt')
print(Model_1)
Model_2 = os.path.join(model_path,model_name_set[1]+'.ckpt')

upsample_method = 'resize'
resolution = (640,480)
content_target_resize = 1

#the resolution of the picture
x_length, y_length = resolution

#Graph
Graph_1 = tf.Graph() # for Model_1: candy_final
Graph_2 = tf.Graph() # for Model_2: starry_final

#Session
sess_1 = tf.Session(graph=Graph_1)
sess_2 = tf.Session(graph=Graph_2)

shape = [1, y_length, x_length, 3]

#First model
with sess_1.as_default():
	with Graph_1.as_default():
		with tf.variable_scope('img_t_net'):
			X_1 = tf.placeholder(tf.float32, shape=shape, name='input')
			Y_1 = create_net(X_1, upsample_method)
		saver_1 = tf.train.Saver(tf.global_variables())
		print('Loading up model_1...')
		saver_1.restore(sess_1, Model_1)
#Second model
with sess_2.as_default():
	with Graph_2.as_default():
		with tf.variable_scope('img_t_net'):
			X_2 = tf.placeholder(tf.float32, shape=shape, name='input')
			Y_2 = create_net(X_2, upsample_method)
		saver_2 = tf.train.Saver(tf.global_variables())
		print('Loading up model_2...')
		saver_2.restore(sess_2, Model_2)

#Model_1 as Default
current_model = model_name_set[0]

while(True):
	if is_file_exist(Style_new_file):
		style_new = read_style(Style_new_file)
		print(style_new)
		if style_new != 'Default':
			print('Change a new style!')
			current_model = style_new
		delet_file(Style_new_file)
	if is_file_exist(Image_check):
		delet_file(Image_check)
		img = utils.imread(Image_file)
		img = utils.imresize(img, content_target_resize)
		img_4d = img[np.newaxis, :]
		if current_model == model_name_set[1]:
			with sess_2.as_default():
				with sess_2.graph.as_default():
					img_out = sess_2.run(Y_2, feed_dict={X_2: img_4d})
		else:
			with sess_1.as_default():
				with sess_1.graph.as_default():
					img_out = sess_1.run(Y_1, feed_dict={X_1: img_4d})
		img_out = np.squeeze(img_out).astype(np.uint8)
		img_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)		
		utils.imwrite(Genered_file, img_out)
		print('Write a new img!\n')
		new_file(Genered_check)
	else:
		time.sleep(0.1)

sess_1.close()
sess_2.close()
