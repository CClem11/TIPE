#Neural Network 2.0
import random, math, numpy
import os, sys
parentdir = os.path.dirname(os.getcwd())
sys.path.insert(0,parentdir) 
from .neuronlayer import NeuronLayer
from .neuron import Neuron

"""
18/05/2018
Deuxième réseau de neuronnes
-class NeuralNetwork : classe réseau de neuronnes principales
-class NeuralLayer : classe pour chaque couche du réseau
-class Neuron : un neuronne seulement 

"""	
	
class NeuralNetwork:
	def __init__(self, input_layer=1, hidden_layers=[], output_layer=1, weights_list=None):
		"""
		input_layer 	= int 			: number of neurons in input layer
		hidden_layers 	= int list 		: list of number of neurons for each layer
		outpur_layer 	= int 			: number of neurons in output layer
		
		weights_list  = list of int list : optionnal parameter to build a neural network with preset weights
		"""
		self.hidden_layers = []
		if weights_list != None:
			hidden_layers = [len(layer) for layer in weights_list]
			output_layer = len(weights_list[-1])
			nb_input = hidden_layers.pop(0)
		else:	
			nb_input = input_layer	#number of input for next layer = nb_neuron previous layer
		
		for i, nb_neuron in enumerate(hidden_layers):
			if weights_list != None:
				weights = weights_list[i]
			else:
				weights = None
			self.hidden_layers.append( NeuronLayer( nb_input, nb_neuron, weights) ) 
			nb_input = nb_neuron
		#last layer
		if weights_list != None:
			self.output_layer = NeuronLayer(nb_input, output_layer, weights_list[-1])
		else:
			self.output_layer = NeuronLayer(nb_input, output_layer)
		
		self.output = 0
		self.errors = []
		self.mean_error = []
		self.max_error = []
	
	def propagation(self, inputs):
		"feed forward"
		input_previous_layer = inputs
		for hidden_layer in self.hidden_layers:
			# print("inputs : ", inputs)
			input_previous_layer = hidden_layer.propagation( input_previous_layer )
		outputs = self.output_layer.propagation( input_previous_layer )
		self.output = outputs
		# print("out : ", outputs)
		return outputs
		
	def train(self, data, batch_size=1):
		"uses backpropagation algorithm on the data, batch_size is the number of times the algo is used before updating the weights"
		length = len(data)
		e_tot = []
		for i in range(0, length, batch_size):
			batch_data = data[i:i+batch_size]
			e = 0
			for inputs, expected in batch_data:
				self.propagation(inputs)
				self.backpropagation(expected)
				e += self.error(expected)	
			self.update_weights()
			e = e/len(batch_data)
			e_tot.append(e)
			self.errors.append(e)
			out = [round(o, 1) for o in self.output]
			# print("inputs : {} outputs : {} <-> {} : expected and error {}".format(inputs, out, expected, e))
			# print("erreur : ", )
		self.mean_error.append(numpy.mean(e_tot))
		self.max_error.append(max(e_tot))
		# print("last mean_error : ", self.mean_error[-1])
		return self.mean_error[-1]
		
	def backpropagation(self, expected, update_w = False):
		"backpropagation of the error"
		#output layer 
		dE_dnet_output_layer = [ -( ex - self.output[i] ) for i, ex in enumerate(expected) ] 
		dE_dnets = [ neuron.backpropagation([dE_dnet_output_layer[nth]], [1]) for nth, neuron in enumerate(self.output_layer.neurons) ]
		#hidden layers
		previous_layer_weights = self.output_layer.get_weights_bias()
		for hidden in self.hidden_layers[::-1]:
			dE_dnets = [ neuron.backpropagation( dE_dnets, [weights[nth] for weights, bias in previous_layer_weights] ) for nth, neuron in enumerate(hidden.neurons) ]
			previous_layer_weights = hidden.get_weights_bias()
			
		if update_w:
			self.update_weights()
	
	def update_weights(self):
		for layer in self.hidden_layers + [self.output_layer]:
			layer.update_weights()
		
	def error(self, expected):
		"using output pre-calculated values"
		e = 0
		for i, ex in enumerate(expected):
			e += 1/2*( ex - self.output[ i ] )**2
		return e
		
	def get_weights_bias(self):
		return [ layer.get_weights_bias() for layer in self.hidden_layers + [self.output_layer]]
		
	def save(self, file=""):
		"save the weights in a pickle file"
		import pickle
		with open(file+".pickle", "wb") as f:
			pickle.dump(self.get_weights_bias(), f)
		