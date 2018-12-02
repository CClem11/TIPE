# -*- coding:utf8 -*-
"""
Created the 24/11/2018

Clément Hinderer
"""
from car import Car
import numpy as np
from NeuralNetwork.neuralnetwork_class import NeuralNetwork
import time
from genetic_algorithm import *

class Brain():
	def __init__(self, hidden_layers=[], weights_list=None):
		if weights_list != None:
			self.neuralnetwork = NeuralNetwork(weights_list=weights_list)
		else:
			self.neuralnetwork = NeuralNetwork(6, hidden_layers, 3)	#with random weights
			# print(self.neuralnetwork.get_weights_bias())
		#for Genetic Algorithm
		self.score = 1
		self.last_distance = 0
		
	def predict(self, inputs):
		prediction = self.neuralnetwork.propagation(np.array(inputs))
		threshold = 0.4
		right = prediction[1] > threshold 
		left = prediction[2] > threshold
		if right and left:
			right = prediction[1] > prediction[2]
			left = prediction[2] > prediction[1]
		return prediction[0], int(right), int(left)
		
	def update_score(self, new_distance):
		diff = new_distance - self.last_distance
		if abs(diff) < 10:
			self.score += diff
			self.last_distance = new_distance
		else:
			pass
			
	def get_dna(self):
		return self.neuralnetwork.get_weights_bias()
		
	

############### Warning multiple import of car.png	#################

class Population():
	"a group of cars"
	def __init__(self, number=2):
		self.number = number
		self.cars = []
		self.brains = []		#each car has its own neural network
		self.map, self.hidden_layers, self.initial_pos = None, [], np.array([])
		self.scores = []	#score per generation
		self.alive = []		#bool list to know if the cars are still in the road
		self.best_score = 0
		self.time_max_generation = 5 # seconds to wait until next generation	
		self.time_last_best_score = time.time()
		self.generation = 1
		self.average_score = 1
		
	def set_map(self, map):
		self.map = map
		
	def set_initial_pos(self, pos0):
		self.initial_pos = pos0
		
	def set_neuralnetwork_type(self, hidden_layers=[]):
		self.hidden_layers = hidden_layers
		
	def create_random_pop(self):
		if not self.initial_pos.any():
			print("initial position is needed to create the cars")
		else:
			self.cars, self.brains = [], []
			for i in range(self.number):
				self.cars.append(Car(self.initial_pos))
				self.brains.append(Brain(self.hidden_layers))	#with random weights
				self.alive.append(True)
				
			# print(self.brains[0].get_dna())
				
	def next_generation(self):
		"selection and reproduction"
		self.generation += 1
		print("Géneration ", self.generation)
		self.alive = [True]*self.number
		self.best_score = 0
		scores = [brain.score for brain in self.brains]
		self.average_score = np.mean(scores)
		print("scores :", scores)
		print("average score :", self.average_score)
		parents_pair = selection(scores)
		selected = [parent for pair in parents_pair for parent in pair]
		# print("parent :", [selected.count(i) for i in range(self.number)])
		parents_dna = [[self.brains[i].get_dna() for i in pair] for pair in parents_pair]
		self.brains = [Brain(weights_list=crossover(*parents)) for parents in parents_dna]
		self.cars = [Car(self.initial_pos) for _ in range(self.number)]
		self.time_last_best_score = time.time()
		# scores = [brain.score for brain in self.brains]
		# print(scores)
		
		
	def move(self, dt):
	  	#update radars, control car, move the car 
		for i, car in enumerate(self.cars):
			if self.alive[i]:
				radars_coef, road_index = self.map.collision_with_road(car.get_radars(), car.road_index)	#very expensive (high complexity)
				car.set_radars_signal(radars_coef)
				car.road_index = road_index
				radar_coef = car.get_radar_coefficients()
				if min(radar_coef) < 0.08:
					self.alive[i] = False
				else:
					inputs = (radar_coef + [round(car.velocity/car.max_velocity, 2)])
					
					prediction = self.brains[i].predict(inputs)
					car.control_ai(*prediction)
					car.move(dt)
					# print("car {} and index : {}".format(i, road_index))
				
	def score(self):
		"""
		evaluate each car by giving a score in function of distance travelled
		returns the index of the best car
		"""
		maxi, index = 0, 0
		for i, car in enumerate(self.cars):
			distance = car.road_index 
			self.brains[i].update_score(distance)
			s = self.brains[i].score
			if s > maxi:
				maxi, index = s, i
		if maxi > self.best_score:
			self.time_last_best_score = time.time()
			self.best_score = maxi
		return index
				
	def is_generation_over(self):
		next_generation = (time.time() - self.time_last_best_score > self.time_max_generation)
		if next_generation:
			# print("New Generation !")
			self.alive = [False]*self.number
			self.next_generation()
	
	def car_focused(self):
		"returns the position of the best car"
		best_index = self.score()
		return np.array(self.cars[best_index].get_pos())
	
	def show(self, display, center=np.array([])):	
		for car in self.cars:
			car.show(display, radar=False, center=center)
		
		