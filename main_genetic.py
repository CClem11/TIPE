# -*- coding:utf8 -*-
"""
Created the 24/11/2018

Clément Hinderer
"""

import pygame
pygame.init()
from car import Car
from map import Map
import time
import numpy as np
import sys
from population import Population
from matplotlib import pyplot as plt

def show_text(message, x, y, size=34, color=(100, 100, 100)):
	font = pygame.font.SysFont("Arial Black", size)
	text_image = font.render(message, 1, color)
	game_display.blit(text_image, (x, y))
	
	
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

number_car = 25
hiddens = [3]

pop = Population(number_car)
pop.set_neuralnetwork_type(hiddens)
pop.set_initial_pos(map.get_starting_point())
pop.set_map(map)
pop.create_random_pop()

#sysargv
show_timelist = "time" in sys.argv
console_mode = "console" in sys.argv
#graph
average_score = [1]

#################################	Main Loop 	####################################
clock = pygame.time.Clock()
fps = 100

#default arg
loop_state = True
while loop_state:
	time_list = []
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			loop_state = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			loop_state = False
			
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_h:
				show_details = not show_details
		
	#	Physics
	time_move = clock.get_time()
	time_factor = 1
	fixed_time = 1/20
	# pop.move(time_move*10**(-3)*time_factor)
	pop.move(fixed_time)
	pop.record_replay_data()
	if pop.is_generation_over():
		average_score.append(pop.average_score)
		
	if not console_mode:
		#	details 
		show_text("Generation {}".format(pop.generation), 20, 30)
		show_text("Average score :{}".format(pop.average_score), 20, 70)
		#	Show functions
		best_car_pos = pop.car_focused()
		center = window_center-best_car_pos
		map.show(game_display, center=center)
		pop.show(game_display, center)
		# 	display update 
		clock.tick(fps)
		pygame.display.update()
		game_display.fill((255, 255, 255))
		time_list.append(time.time())
		if show_timelist:
			msg = "{} "*(len(time_list)-1)
			print(msg.format(*[10**3*round(time_list[i+1]-time_list[i], 4) for i in range(len(time_list)-1)]))
		
		

pop.save_best()
pop.save_replay(map.get_map())
#to close properly pygame
pygame.quit()

#plot the average_score
plt.plot(average_score)
plt.title("Average score")
plt.xlabel("generation")
plt.show()

