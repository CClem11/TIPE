import pygame
import numpy as np
from pygame import gfxdraw

class CarGui:
	def __init__(self, other_skin = False):
		if other_skin:
			self.img = pygame.image.load("ressources/car2.png")
		else:
			self.img = pygame.image.load("ressources/car3.png")
		w, h = self.img.get_size()
		new_width = 100
		self.img = pygame.transform.scale(self.img, (new_width, int(h*new_width/w)))
		self.img = pygame.transform.rotate(self.img, 180)

	def show(self, display, pos, angle, radar_points, radar_on, center=np.array([])):
		self.show_car(display, pos, angle, center)
		if radar_on:
			for p in radar_points:
				self.show_radar(display, *p, center)
	
	def show_car(self, display, pos, car_angle, center=np.array([])):
		img = pygame.transform.rotate(self.img, -car_angle)
		w, h = img.get_size()
		pos = np.array((int(pos[0]-w/2), int(pos[1]-h/2)))
		if center.any():
			pos = pos + center
		display.blit(img, pos)
	
	def show_car_circle(self, display, pos, angle):
		r = 20
		pos = int(pos[0]), int(pos[1])
		angle = np.radians(angle)
		pygame.gfxdraw.filled_circle(display, pos[0], pos[1], r, (255, 0, 0))
		pygame.draw.aaline(display, (0, 0, 255), pos, pos+r*np.array( (np.cos(angle), np.sin(angle)) ), 1)
		
	def show_radar(self, display, p1, p2, p3, center=np.array([])):
		"p1, p2, p3 = start, intersection, end"
		# print("printing the radar", p1, p2, p3)
		if center.any():
			p1 = np.array(p1) + center
			p2 = np.array(p2) + center
			p3 = np.array(p3) + center
			
		pygame.draw.aaline(display, (255, 0, 0), p3, p2, 1)
		pygame.draw.aaline(display, (0, 255, 0), p1, p3, 1)
		
		