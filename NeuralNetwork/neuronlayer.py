import os, sys
parentdir = os.path.dirname(os.getcwd())
sys.path.insert(0,parentdir) 
from .neuron import Neuron

class NeuronLayer:
	def __init__(self, nb_inputs, nb_neurons, weights_list = None):
		if weights_list:
			"List of something like this : [weights], bias (for each neuron)"
			self.neurons = [Neuron(nb_inputs, weights=weights) for weights in weights_list]
		else:
			self.neurons = [Neuron(nb_inputs) for _ in range(nb_neurons)]
		
	def propagation(self, inputs):
		# print("new layer, nb_neurons = ", len(self.neurons))
		outputs = [ self.neurons[i].propagation( inputs ) for i in range(len(self.neurons)) ]
		# print("output : ", outputs)
		return outputs
		
	def get_weights_bias(self):
		return [neuron.get_weights_bias() for neuron in self.neurons]
		
	def update_weights(self):
		for neuron in self.neurons:
			neuron.update_delta_weight()
