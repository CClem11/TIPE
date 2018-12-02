import pygame
pygame.init()
import numpy as np
from collision import *
from pickle import Pickler
from constants import MAP_DEFINITION, ROAD_RADIUS
#MAP_DEFINITION : 1 points every MAP_DEFINITION pixels
	
def map_points(points):
	"return the lists of points that define the side1, the side2 and the road itself"
	sides = [[], []]
	road_radius = ROAD_RADIUS
	for i in range(len(points)-1):
		p1, p2 = np.array(points[i]), np.array(points[i+1])
		u = p2-p1 # directional coefficient 
		
		if u[0] == 0 or u[1] == 0:
			n = np.array([u[1]!=0, u[0]==0])
		else:
			n = np.array( 1, u[1]/u[0] )
			
		n = np.array( (-u[1], u[0]) )
		# print(n)
		n = n/np.linalg.norm(n)
		
		mid = (p1 + p2)/2
		A = mid + road_radius * n
		B = mid - road_radius * n
		side_points = [A, B]
		#test smooth curve
		coef_smooth = 4
		for i, side in enumerate(sides):
			if side:
				condition = True
				for last_point in side[-min(10, len(side))::]:
					if distance(side_points[i], last_point) < MAP_DEFINITION*coef_smooth:
						condition = False
						break
				if condition:
					side.append(side_points[i])
				else:
					side.append(side[-1]) #this way sides have the same length
			else:
				side.append(side_points[i])
	
	return sides[0], sides[1], points[1:]
			

# fenetre = (800, 450)
fenetre = (1600, 900)
if fenetre == (1600, 900):
	game_display = pygame.display.set_mode(fenetre, pygame.FULLSCREEN)
else:
	game_display = pygame.display.set_mode(fenetre)

clock = pygame.time.Clock()
fps = 50

points = [(0, 0)]

finished = False
souris_on = False
loop_state = True
while loop_state:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			loop_state = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			loop_state = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				points = [(0, 0)]
				finished = False
			if event.key == pygame.K_s:
				with open("maps/map", "wb") as f:
					p = Pickler(f)
					sides = map_points(points[1:])
					zoom_coef = 2
					sides = [[zoom_coef*np.array(point) for point in side] for side in sides]
					print("lists length : ", [len(i) for i in sides])
					p.dump(sides)
				print("saved as \"map\"")
			
			if event.key == pygame.K_f:
				finished = not finished
				
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				souris_on = True
				
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				souris_on = False
		
	if souris_on:	
		pos = pygame.mouse.get_pos()
		if distance(pos, points[-1]) > MAP_DEFINITION:			# road precision
			points.append(pos)
	
	if len(points) > 3:
		pygame.draw.lines(game_display, (255, 255, 255), finished, points[1:], 10)
		sides = map_points(points[1:])[0:-1]
		for s in sides:
			if len(s) > 2:
				pygame.draw.lines(game_display, (0, 255, 0), finished, s, 10)
		
	clock.tick(fps)
	pygame.display.flip()
	game_display.fill((0, 0, 0))

pygame.quit()
points.pop(0)
print("number of points :", len(points)-1)


