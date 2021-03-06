import os
print("cwd :", os.getcwd())
from NeuralNetwork.neuralnetwork_class import NeuralNetwork
from pickle import Unpickler
import numpy as np

class ArtificialIntelligence:
	def __init__(self):
		self.initialized = False
		
	def load_model(self):
		dir = os.getcwd()
		dir = os.path.join(dir, "model")
		files = os.listdir(dir)
		files = [f for f in files if f.endswith((".pickle"))]
		if not files:
			print("no model available !")
			return False
		else:
			self.initialized = True
			#at least one model available
			for k, f in enumerate(files):
				print(k, " :", f)
			i = int(input("Choose the file : "))
			if not i in range(len(files)):
				i = 0
			file_name = os.path.join("model", files[i])
			print("model found :", file_name)
			
			with open(file_name, 'br') as file:
				p = Unpickler(file)
				weights = p.load()
				
			model = NeuralNetwork(weights_list = weights)
			self.model = model
			print("Good choice you are using the python coded NeuralNetwork !")
	
	def predict(self, input):
		"return a tuple for control keys : (acc, left, right)"
		if not self.initialized:
			print("No model loaded !")
			return False
		else:
			prediction = self.model.propagation(np.array(input))
			threshold = 0.4
			right = prediction[1] > threshold #prediction[2]
			left = prediction[2] > threshold #prediction[1]
			if right and left:
				right = prediction[1] > prediction[2]
				left = prediction[2] > prediction[1]
			return prediction[0], int(right), int(left)
			# return prediction
	
	

	
	
	