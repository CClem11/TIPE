import numpy as np
import os, sys
parentdir = os.path.dirname(os.getcwd())
sys.path.insert(0,parentdir) 
from open_data import load_data, split_data
from NeuralNetwork.neuralnetwork_class import NeuralNetwork

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

inputs, outputs = map(np.array, split_data(*load_data(file_name)))
data = [(inputs[i], outputs[i]) for i in range(len(inputs))]
# print("len data : ", len(data))

#Neural network parameters
nb_inputs = len(inputs[0])
# hiddens = []
hiddens = [5]
nb_outputs = 3

model = NeuralNetwork(nb_inputs, hiddens, nb_outputs)

number_epochs = int(input("epochs : "))
for i in range(number_epochs):
	error = model.train(data, batch_size=30)
	print("epoch {} average error : {}".format(i+1, round(float(error), 3)))
	
# print("example : inputs {} outputs {} and nn_output {}".format(inputs[0], outputs[0], model.propagation(inputs[0])))
	
#saving the model
if int(input("save (0/1) : ")):
	nb_neurons_layers = [nb_inputs] + hiddens + [nb_outputs]
	file_name = "model_len_{}_epochs_{}_layers_{}_nn_class".format(len(inputs), number_epochs, "".join(map(str, nb_neurons_layers)))
	file_name = os.path.join("model", file_name)
	file_name = os.path.join(parentdir, file_name)
	model.save(file_name)
	print("model saved as ", file_name)