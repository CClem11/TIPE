import math, random
import numpy as np
import os, sys
print("cwd :", os.getcwd())

class Neuron:
	learning_rate = 0.1
	
	def __init__(self, nb_inputs, weights=None, activation_function="sigmoid"):
	# def __init__(self, nb_inputs, weights=None, activation_function="relu"):
	# def __init__(self, nb_inputs, weights=None, activation_function="tanh"):
		"weights = [ [weights], bias ]  : to set the weights and the bias"
		if weights == None:
			# self.weights = np.array([2*random.random()-1 for _ in range(nb_inputs)], dtype="int64")
			self.weights = np.array([2*random.random()-1 for _ in range(nb_inputs)])
			self.bias = 2*random.random() - 1
		else:
			self.weights = weights[0]
			self.bias = weights[1]
		
		self.activation_function = activation_function
		self.inputs = []
		self.net = 0
		self.out = 0
		self.error_out_net = 0
		self.delta_weights = [0]*nb_inputs
		self.delta_bias = 0
		
		#store de "delta node" for back propagation algorithm
		self.dE_dnet = 0 		# dE(total)/dnet (of the neuron)
		
	def propagation(self, inputs):
		"calculates net output, output using activation function and return the output"
		self.update_inputs(inputs)
		if self.activation_function == "sigmoid":
			self.update_output_sigmoid()
			self.update_error_out_net_sigmoid()
		elif self.activation_function == "relu":
			self.update_output_relu()
			self.update_error_out_net_relu()
		return self.out
 		
	def update_inputs(self, inputs):
		self.inputs = inputs
		self.net = self.bias
		# print("\n", self.inputs, self.weights)
		for i, input in enumerate(inputs):
			self.net += input * self.weights[i]
			# if self.net == np.nan:
				# print("input * self.weights[i] : {} * {}".format(input, self.weights[i]))
				
	def update_output_sigmoid(self):
		self.out = 1/(1+math.exp(-self.net))
	def update_output_relu(self):
		if self.net < 0:
			self.out = 0
		else:
			self.out = self.net
			
	#fonction pour calculer l'erreur de la sortie par rapport à l'entrée
	def update_error_out_net_sigmoid(self):
		self.error_out_net = self.out * (1 - self.out)
	def update_error_out_net_relu(self):
		if self.out >= 0:
			self.error_out_net = 1
		else:	# i may be useful to set a value different than 0 like 0.01
				# not real relu but -> leaky relu to avoid the dying relu problem
			self.error_out_net = 0.01
		
	def backpropagation(self, dE_dnets, weights_to_next_layer):
		"returns the neuron dE_dnet in function of the dE_dnets and the weights (of previous layer)"
		dE_dout = 0
		for i, w in enumerate(weights_to_next_layer):
			dE_dout += w * dE_dnets[ i ]
			
		self.dE_dnet = dE_dout * self.error_out_net
		self.calculate_delta_weights()
		return self.dE_dnet
		
	def calculate_delta_weights(self):
		"in function of the d(total error)/d(neuron net) = self.dE_dnet"
		for i in range(len(self.weights)):
			delta = -self.learning_rate * self.dE_dnet * self.inputs[ i ]
			# if delta == np.nan:
				# print("self.dE_dnet * self.inputs[ i ] : {} * {}".format(self.dE_dnet, self.inputs[i]))
			self.delta_weights[i] += delta
		self.delta_bias += -self.learning_rate * self.dE_dnet
	
	def update_delta_weight(self):
		for i, delta_weight in enumerate(self.delta_weights):
			self.weights[i] += delta_weight
		self.bias += self.delta_bias
		#reset des delta
		self.delta_weights = [0]*len(self.weights)
		self.delta_bias = 0
		
	def get_weights_bias(self):
		return [self.weights, self.bias]