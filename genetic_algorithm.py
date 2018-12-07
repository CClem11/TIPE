# -*- coding:utf8 -*-
"""
Created the 25/11/2018

Clément Hinderer
"""
import random
import numpy as np
from NeuralNetwork.neuralnetwork_class import NeuralNetwork

def selection(scores_list):
	"returns a list of (index1, index2) corresponding to the selected parents"
	# scores_list = np.array(scores_list)**2
	scores_list = np.exp(np.array(scores_list))
	s = sum(scores_list)
	prop = scores_list/s
	# print(prop)
	parents_list = []
	for _ in range(len(scores_list)):
		#choose a parent with a probability proportionnal to its score
		pair = []
		for _ in range(2):	# to choose 2 parents		
			i, r = 0, random.random() # between 0 and 1
			while prop[i] < r:
				r -= prop[i]
				i += 1
			pair.append(i)
		parents_list.append(pair)
	
	return parents_list
	
	
def crossover(parentA, parentB):
	"returns a child_dna = weights in function of parentA and parentB dna ie neural network weights"
	parents = (parentA, parentB)
	neurons_per_layers = [len(layer) for layer in parentA]
	# print("layers :", neurons_per_layers)
	neurons_input, neurons_output = len(parentA[0][0][0]), neurons_per_layers[-1]
	# print("layers : input {} hiddens {} output {}".format(neurons_input, neurons_per_layers[1:-1], neurons_output))
	offspring = NeuralNetwork(neurons_input, neurons_per_layers[1:-1], neurons_output)	# the "child" brain (or dna)
	dna = offspring.get_weights_bias()
	# print("parent and child:", parentA, "\n", dna)
	prob_mutation = 0.1
	for layer in range(len(dna)):
		for neuron in range(len(dna[layer])):
			#neuron[0=weights list and neuron[1] = bias of the neuron
			
			for w in range(len(dna[layer][neuron][0])):
				r = random.randrange(0, 2)	# 0 or 1 for parent A or B
				dna[layer][neuron][0][w] = parents[r][layer][neuron][0][w]
				#mutation
				if random.random() > 1-prob_mutation:
					dna[layer][neuron][0][w] = random.random()*4-2	#between -2 and 2
			#and for the bias
			dna[layer][neuron][1] = parents[random.randrange(0, 2)][layer][neuron][1]
			if random.random() > 1-prob_mutation:
					dna[layer][neuron][1] = random.random()*4-2	#between -2 and 2
	return dna
	
	
def mutate(neuralnetwork, prop=0.1):
	"mutate weights of the neural network with a certain probability"
	
	return neuralnetwork