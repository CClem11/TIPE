import numpy as np
from radar import Radar
from cargui import CarGui
from collision import distance
from constants import RADAR_LENGTH

def constrain(mini, maxi, value):
	if value < mini:
		return mini
	elif value > maxi:
		return maxi
	return value

class Car():
	def __init__(self, initial_pos, other_skin=False):
		self.pos = np.array(initial_pos)
		self.velocity = 0
		self.angle = -90
		
		#parameters
		#last max velocity = 400
		self.max_velocity = 500		# pxl / sec
		self.acc_values = [-300, -300, 150] 			# pxl / sec^2		[no acc (resistance), break, real acc]
		self.angle_velocity = 120 	# degrees / sec
		
		#controls
		self.controls_keys = []
		self.controls_type = []
		self.keys_values = [0, 0, 0, 0]
		
		#for collision efficiency
		self.road_index = 0
		
		#radar
		radar_angle = 25
		self.radar_length = RADAR_LENGTH
		self.radars = []
		#adding 5 radars
		self.radars.append(Radar(self.radar_length, -2*radar_angle))
		self.radars.append(Radar(self.radar_length, -1*radar_angle))
		self.radars.append(Radar(self.radar_length, 0*radar_angle))
		self.radars.append(Radar(self.radar_length, 1*radar_angle))
		self.radars.append(Radar(self.radar_length, 2*radar_angle))
		
		self.radar_points = [[0, 0] for r in self.radars]
		#GUI
		self.gui = CarGui(other_skin)
		
	def get_pos(self):
		return self.pos
	def get_angle(self):
		return self.angle
		
	def set_controls(self, controls, on_type, off_type):
		"controls is a list of pygame variable like pygame.K_UP. on/off type are for KEYDOWN or KEYUP"
		self.controls_keys = controls						# order : up, down, right, left
		self.controls_type = [on_type, off_type]
		for i in range(len(self.controls_keys)):
			self.keys_values.append(0)
		
	def update_controls(self, event):
		if event.type in self.controls_type and event.key in self.controls_keys:
			value = int( not (self.controls_type.index(event.type) ) )
			self.keys_values[ self.controls_keys.index(event.key) ] = value		# 0 or 1
			
	def control_ai(self, acc, right, left):
		self.keys_values[2] = right
		self.keys_values[3] = left
		if acc != None:
			self.keys_values[0] = acc>0.58
			
	def move(self, dt):
		"simple physic model"
		acc = self.acc_values[0]
		if self.keys_values[0]:
			acc = self.acc_values[2]
		elif self.keys_values[1]:
			acc = self.acc_values[1]

		self.velocity += acc * dt	
		self.velocity = constrain(0, self.max_velocity, self.velocity)
		
		angle_velocity = self.angle_velocity * (self.keys_values[3] - self.keys_values[2])
		self.angle += angle_velocity * dt
		
		angle_vector = np.array( (np.cos(np.radians(self.angle)), np.sin(np.radians(self.angle))) )
		self.pos = self.pos + self.velocity * angle_vector * dt	
		
	def get_radars(self):
		return [ r.get_segment(self.pos, self.angle) for r in self.radars ]
		
	def set_radars_signal(self, points):
		for i, r in enumerate(self.radars):
			if type(points[i]) != bool:
				self.radar_points[i] = points[i]
			else:
				self.radar_points[i] = r.get_segment(self.pos, self.angle)[1]
				
	def get_radar_coefficients(self):
		"return number between 0 and 1 that represents where the intersection is"
		pos = self.pos
		return [round(distance(pos, self.radar_points[i])/self.radar_length, 2) for i in range(len(self.radars))]
		
	def get_car_inputs(self):
		"return the value of acceleration and turn"
		return (self.keys_values[0], self.keys_values[2], self.keys_values[3])
		
	def show(self, display, radar=True, center=np.array([])):
		liste = [ list(r.get_segment(self.pos, self.angle)) + [self.radar_points[i]] for i, r in enumerate(self.radars)]
		self.gui.show(display, self.pos, self.angle, liste, radar, center)
		

		