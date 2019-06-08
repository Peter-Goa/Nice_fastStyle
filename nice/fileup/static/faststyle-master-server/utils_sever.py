import os

model_path = './models/'
model_name_set = ['candy_final','starry_final']

#decide the exist of a file
def is_file_exist(file_path):
	isExist = False
	isExist = os.path.isfile(file_path)
	return isExist

#delete a file
def delet_file(file_path):
	if is_file_exist(file_path):
		os.remove(file_path)

#read the style file and get the new style being drawn
def read_style(file_path):
	model_name = 'Default' # if there isn't a valid model name, the default value will return, which won't change the style
	if is_file_exist(file_path):
		try:
			file = open(file_path, 'r')
			model_name_temp = file.readline()
			file.close()
		except IOError:
			print('Err, when read from file.')
			delet_file(file_path)
			return model_name
	if model_name_temp in model_name_set:
		model_name = model_name_temp
	delet_file(file_path)
	return model_name

#make a new file
def new_file(file_path):
	if not is_file_exist(file_path):
		try:
			file = open(file_path,'w')
			file.close
		except Exception as e:
			print('a error: can not make a new file.')


		
		


