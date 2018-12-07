from pickle import Unpickler
import numpy as np
import pygame
from collision import collision, distance
from constants import RADAR_LENGTH, MAP_DEFINITION
import time
from multiprocessing.dummy import Pool as ThreadPool 

class Map:
	def __init__(self):
		self.road = []
		self.initial_pos = [0, 0]

		self.index_list = []
		
	def load_map(self, file_name):
		with open(file_name, "rb") as f:
			p = Unpickler(f)
			self.road = p.load()
			# to avoid missing the last segment
			self.road = list(self.road)
			# starting point for the car
			self.initial_pos = (self.road[0][0] + self.road[1][0])/2
			
	def get_map(self):
		return self.road
			
	def get_starting_point(self):
		return self.initial_pos
	
	def show(self, display, center=np.array([]), only_for_collision=False):
		color = (50, 50, 50)
		for side in self.road[0:-1]:
			if only_for_collision:
				side = [side[i] for i in self.index_list]
			if center.any() != False:
				side = [np.array(point)+np.array(center) for point in side ]
			pygame.draw.aalines(display, color, not(only_for_collision), side, 1)
			
	def collision_with_road(self, points, car_road_index, print_details=False):
		"points : radars list [ (p1, p2), ..., (p1, p2)]"
		t0 = time.time()
		result = []
		max_range = RADAR_LENGTH

		#candidates points using the 3rd list of points
		p = points[0][0] 	# car position
		#find the new closest point based on the previous car_road_index
		min_d, min_index = distance(p, self.road[2][0]), 0
		road_length = len(self.road[2])
		for i in range(-10, 10):
			d = distance(p, self.road[2][(car_road_index+i)%road_length])
			if d < min_d:
				min_d = d
				min_index = (car_road_index+i)%road_length

		t1 = time.time()
		#construct the index list (of points that will be checked)
		index_list = []		
		total_point = len(self.road[0])
		nb_points = int(RADAR_LENGTH/MAP_DEFINITION/2)
		a, b = min_index-nb_points, min_index + nb_points
		if a < 0:
			index_list.append([i for i in range(a%total_point, total_point)])
		index_list.append([i for i in range( max(0, a), min(total_point, b) )])
		if b > total_point:
			index_list.append([i for i in range(0, b%total_point)])
		index_list = [i for sublist in index_list for i in sublist]	
		self.index_list = index_list #to show 
		# print(index_list)
		# print("number of points to check:", len(index_list), " max distance : ", len(index_list)*MAP_DEFINITION)
		# build the segments list
		segments_selection = []
		for i in range(len(index_list)-1):
			for side in self.road[0:2]:
				p1, p2 = side[index_list[i]], side[index_list[i+1]]
				segments_selection.append((p1, p2))
		t2 = time.time()
		
		# print("number of segments to check : ", len(segments_selection))
		#"return whether or not the segment defined by [p1, p2] intersects with the side of the road"
		
		"""
		pool = ThreadPool(10) 
		results = pool.map(my_function, my_array)
		"""
		
		for p1, p2 in points:
			mini = max_range
			mid_mini = (0, 0)
			for s in segments_selection:
				# first test to avoir checking with the road too far
				mid = collision((p1, p2), s)
				d = distance(p1, mid) 
				if d < mini:
					mini = d
					mid_mini = mid
			if mini == max_range:
				result.append(False)
			else:
				result.append(mid_mini)
				
		# multi-threading version
		# pool = ThreadPool(1)
		# result = pool.map(lambda radar:self.collision_radar_map(radar, segments_selection), points)
		if print_details:
			print("collision time (ms): ", 10**3*round(time.time()-t2, 4), "only closet point :", 10**3*round(t1-t0, 4), "construction of segments : ", 10**3*round(t2-t1, 4))
			# print("collision time (ms): ", 10**3*round(t1-t0, 4), "only closet point :", 10**3*round(t1-t0, 4), "construction of segments : ", 10**3*round(t2-t1, 4))
		return result, min_index
	
	def collision_radar_map(self, radar, map_segments):
		"return the nearest point of intersection with the car or 0 if no intersection"
		pool = ThreadPool(1)
		#calculate intersection point list
		intersection_list = pool.map(lambda s:collision(radar, s), map_segments)
		#calculate distance with the car
		distance_list = pool.map(lambda p:distance(p, radar[0]) , intersection_list)
		min_d = min(distance_list)
		return intersection_list[distance_list.index(min_d)]
		

if __name__ == "__main__":
	m = Map()
	m.load_map("maps/map")