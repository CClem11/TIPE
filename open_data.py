from pickle import Unpickler
import numpy as np
import os
from random import shuffle

def load_data(name):
	with open(name, "rb") as f:
		p = Unpickler(f)
		inputs_outputs = p.load()
	shuffle(inputs_outputs)
	inputs, outputs = [], []
	for couple in inputs_outputs:
		inputs.append(couple[0])
		outputs.append(couple[1])
	return inputs, outputs

def split_data(inputs, outputs):
	"inputs : radars + velocity ; outputs : (acc, right, turn)	"
	split_dict = {key:[input for i, input in enumerate(inputs) if outputs[i] == key] for key in set(outputs)}
	split_dict_len = {key:len([input for i, input in enumerate(inputs) if outputs[i] == key]) for key in set(outputs)}
	print("all outputs : len(inputs) : ", split_dict_len)
	#outputs that we don't want : example (0, 0, 0)
	undesirable = [(0, 0, 0)]
	#create class with same length 
	maximum_sample = max([v for k, v in split_dict_len.items()])
	inputs, outputs = [], []
	for k, v in split_dict.items():
		if k not in undesirable:
			outputs = outputs + [k]*maximum_sample
			input_maximum_length = v*(int(maximum_sample/len(v))+1)
			inputs = inputs + input_maximum_length[:maximum_sample]
			# print("longueur de inputs :", len(inputs))

	#Pour shuffle : ne pas mettre les memes classes ensemble
	nb_data = len(outputs)
	data = [(inputs[i], outputs[i]) for i in range(nb_data)]
	shuffle(data)
	#on recreer les deux listes
	inputs, outputs = [data[i][0] for i in range(nb_data)], [data[i][1] for i in range(nb_data)]
	print("len inputs : {} et len outputs : {}".format(len(inputs), len(outputs)))
	return inputs, outputs

def split_data_no_acc(inputs, outputs):
	"inputs : radar + vitesse ; outputs : (acc, right, turn)	"
	combinations = {(1, 1, 0):[], (1, 0, 1):[], (1, 0, 0):[]}	#only useful combination of keys
	keys = list(combinations.keys())
	others = []
	print("keys (useful output): ", keys)
	for i, output in enumerate(outputs):
		if output in keys:
			combinations[ output ].append( inputs[i] )
		else:
			if output not in others:
				others.append(output)
	for k, v in combinations.items():
		print(k, len(v))

	print("other possibilities : ", others)
	sample = min( [len(v) for v in combinations.values()] )
	inputs, outputs = [], []
	for k, v in combinations.items():
		outputs = outputs + [k]*sample
		inputs = inputs + v[:sample]

	# for training purpose we need to shuffle our data
	nb_combi = len(combinations.keys())
	data = [(inputs[i], outputs[i]) for i in range(nb_combi*sample)]
	shuffle(data)
	#recreating the two lists of inputs and outputs
	inputs, outputs = [data[i][0] for i in range(nb_combi*sample)], [data[i][1] for i in range(nb_combi*sample)]
	print("len inputs : {} et len outputs : {}".format(len(inputs), len(outputs)))
	return inputs, outputs
	