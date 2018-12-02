import numpy as np	
		
class Radar:
	def __init__(self, length=350, angle=0):
		self.max_length = length
		self.angle = np.radians(angle)		# with respect to the car
		
	def get_vector(self, start_pos, car_angle):
		start_pos = np.array(start_pos)
		angle = self.angle + np.radians(car_angle)
		angle_vect = np.array( (np.cos(angle), np.sin(angle)) )
		return (start_pos, self.max_length * angle_vect)
		
	def get_segment(self, start_pos, car_angle):
		start_pos = np.array(start_pos)
		angle = self.angle + np.radians(car_angle)
		angle_vect = np.array( (np.cos(angle), np.sin(angle)) )
		return (start_pos, start_pos + self.max_length * angle_vect)
		
	
		
		