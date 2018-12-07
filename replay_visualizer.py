# -*- coding:utf8 -*-
"""
Created the 06/12/2018

Clément Hinderer
"""
# -*- coding:utf8 -*-
"""
Created the 24/11/2018

Clément Hinderer
"""

import pygame
pygame.init()
from cargui import CarGui
from map import Map
import time, os
import numpy as np
import sys
from pickle import Unpickler


def show_text(message, x, y, size=34, color=(100, 100, 100)):
	font = pygame.font.SysFont("Arial Black", size)
	text_image = font.render(message, 1, color)
	game_display.blit(text_image, (x, y))
	
def select_file():
	files = os.listdir("replay")
	for i, f in enumerate(files):
		print(i, " :", f)
	i = int(input("Choose the replay file : "))
	if not i in range(len(files)):
		i = 0
	# print(files)
	file_name = os.path.join("replay", files[i])
	return file_name
	
def load_replay():
	with open(select_file(), "rb") as file:
		p = Unpickler(file)
		data = p.load()
		map = p.load()
	return data, map
	
	
class ReplayReader():
	def __init__(self):
		self.data, self.map = load_replay()
		self.generation = 0
		self.max_generation = len(self.data)
		self.frame = 0
		self.max_frame = len(self.data[0])
		self.cargui = CarGui()
		self.center = [0, 0]
		
	def get_map(self):
		return self.map
		
	def show(self, display, window_center):
		self.get_center()
		for pos, angle in self.data[self.generation][self.frame][0]:
			self.cargui.show(display, pos, angle, [], False, center=window_center-self.center)
			
	def iteration(self):
		"frame += 1 and return if the next frame exist"
		self.frame += 1
		if self.frame == self.max_frame:
			self.generation += 1
			self.frame = 0
			if self.generation != self.max_generation:
				self.max_frame = len(self.data[self.generation])
			else:
				return False
		return True
		
	def get_center(self):
		self.center = self.data[self.generation][self.frame][1]
		return self.center
	
	def change_generation(self, n=1):
		self.generation = (self.generation+n)%self.max_generation
		self.frame = 0
		self.max_frame = len(self.data[self.generation])
	
#load replay data	
replayreader = ReplayReader()
	
#Create the graphical interface
window = (800, 450)
# window = (1000, 500)
window = (1600, 900)
window_center = np.array(window)/2
if window == (1600, 900):
	game_display = pygame.display.set_mode(window, pygame.FULLSCREEN)
else:
	game_display = pygame.display.set_mode(window)

#Initialization of some classes
map = Map()
map.load_map("maps/map")
map.road = replayreader.get_map()


#################################	Main Loop 	####################################
clock = pygame.time.Clock()
fps = 30

loop_state = True
while loop_state:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			loop_state = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			loop_state = False
			
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_h:
				show_details = not show_details
			# print(event, event.type, event.key)
			if event.key == pygame.K_RIGHT:
				replayreader.change_generation(1)
			elif event.key == pygame.K_LEFT:
				replayreader.change_generation(-1)
				
	#	Physics
	time_move = clock.get_time()
	time_factor = 1
	fixed_time = 1/20

	replayreader.show(game_display, window_center)
	
	if not replayreader.iteration():
		# loop_state = False
		replayreader.generation = 0
	else:
		center = replayreader.get_center()
		center = window_center-center
	
	#details
	show_text("Generation {}".format(replayreader.generation), 20, 30)
	
	#	Show functions
	map.show(game_display, center=center)

	# 	display update 
	clock.tick(fps)
	pygame.display.update()
	game_display.fill((255, 255, 255))

	
#to close properly pygame
pygame.quit()


