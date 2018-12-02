import numpy as np
import os, sys
parentdir = os.path.dirname(os.getcwd())
sys.path.insert(0,parentdir) 
from open_data import load_data, split_data
from create_neuralnetwork_keras import *

def select_file():
	dir = os.path.join(parentdir, "data")
	files = os.listdir(dir)
	for i, f in enumerate(files):
		print(i, " :", f)
	i = int(input("Choose the data file : "))
	if not i in range(len(files)):
		i = 0
	file_name = os.path.join(dir, files[i])
	return file_name

file_name = select_file()
print("Selected file : ", file_name)
inputs, outputs = load_data(file_name)
inputs, outputs = split_data(inputs, outputs)
inputs, outputs = np.array(inputs), np.array(outputs)

model = create_neural_network(len(inputs[0]))
number_epochs = 100
number_epochs = int(input("epochs : "))
training(model, number_epochs, inputs, outputs)

#saving the model
if int(input("save (0/1) : ")):
	file_name = "model_len_{}_epochs_{}.h5".format(len(inputs), number_epochs)
	file_name = os.path.join("model", file_name)
	model.save_weights(os.path.join(parentdir, file_name), save_format = "h5")
	print("model saved as : ", file_name)
