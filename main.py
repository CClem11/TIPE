import pygame
pygame.init()
from car import Car
from map import Map
from pickle import Pickler
import time
import numpy as np
import sys

def show_text(message, x, y, size=34, color=(100, 100, 100)):
	font = pygame.font.SysFont("Arial Black", size)
	text_image = font.render(message, 1, color)
	game_display.blit(text_image, (x, y))
	
#enable ai
# ai_enable = False
ai_enable = int(input("Use AI (0/1) : "))
if ai_enable:
	if not int(input("Keras or python_class (0/1) : ")):
		from artificial_intelligence_keras import ArtificialIntelligence
	else:
		from artificial_intelligence import ArtificialIntelligence
	bot = ArtificialIntelligence()
	bot.load_model()	
	
#Create the graphical interface
# window = (800, 450)
window = (1600, 900)
window_center = np.array(window)/2
if window == (1600, 900):
	game_display = pygame.display.set_mode(window, pygame.FULLSCREEN)
else:
	game_display = pygame.display.set_mode(window)

#Initilization of some classes
map = Map()
map.load_map("maps/map")
car = Car(map.get_starting_point())
car.set_controls([pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d], pygame.KEYDOWN, pygame.KEYUP)
# cars = []
# for i in range(25):
# 	car2 = Car(map.get_starting_point(), True)
# 	car2.set_controls([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], pygame.KEYDOWN, pygame.KEYUP)
# 	cars.append(car2)

# varaible to store the inputs/ouputs to train the neural network later
data = []		#list of (inputs, outputs)
record = False
centered_view = True	

#################################	Main Loop 	####################################
clock = pygame.time.Clock()
fps = 100

#default arg
self_driving, self_driving_acc = False, False
show_details = "guidetails" in sys.argv
show_timelist = "time" in sys.argv
show_close_road = False
loop_state = True
while loop_state:
	time_list = []
	time_list.append(time.time())
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			loop_state = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			loop_state = False
			
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				record = not record
			elif event.key == pygame.K_c: # bot control (right, left)
				self_driving = not self_driving
				if not self_driving:
					self_driving_acc = False
			elif event.key == pygame.K_v: # bot control also acc 
				self_driving_acc = not self_driving_acc

			elif event.key == pygame.K_k:
				centered_view = not centered_view

			elif event.key == pygame.K_h:
				show_details = not show_details
				
			elif event.key == pygame.K_n:
				show_close_road = not show_close_road

			elif event.key == pygame.K_i:
				#reset car position
				car.pos = map.get_starting_point()
				
		car.update_controls(event)
	

	time_move = clock.get_time()
	#inputs/outputs	
	radar_coef = car.get_radar_coefficients()
	inputs = (radar_coef + [round(car.velocity/car.max_velocity, 2)])
	outputs = car.get_car_inputs()
	if ai_enable:
		prediction = bot.predict(inputs)
		if self_driving:
			if self_driving_acc:
				car.control_ai(*prediction)
			else:
				car.control_ai(None, *prediction[1:])

	time_list.append(time.time())
	time_factor = 1
	car.move(time_move*10**(-3)*time_factor)
	time_list.append(time.time())
	radars_coef, road_index = map.collision_with_road(car.get_radars(), car.road_index, print_details=show_timelist)	#very expensive (high complexity)
	car.set_radars_signal(radars_coef)
	car.road_index = road_index
	time_list.append(time.time())

	
	if record:
		show_text("record: ", window[0]-220, 50, 30)
		data.append((inputs, outputs))
		show_text("ON", window[0]-100, 50, 30, (0, 255, 0))
	# else:
		# show_text("OFF", window[0]-100, 50, 30, (255, 0, 0))
	time_list.append(time.time())
	#	SHOW
	car_pos =np.array(car.get_pos())
	if centered_view:	
		map.show(game_display, center=window_center-car_pos, only_for_collision=show_close_road)
		car.show(game_display, radar=True, center=window_center-car_pos)	#translation of window_center - car_pos
	else:
		map.show(game_display, only_for_collision=show_close_road)
		car.show(game_display, radar=True)
	
	time_list.append(time.time())
	# car2.show(game_display ,radar=False)
	if show_details:
		show_text("velocity/vmax : {}".format(round(car.velocity/car.max_velocity, 2)), 50, 20)
		show_text("fps : {}".format(int(clock.get_fps())), 50, 60) 
		show_text("radars : {}".format(radar_coef), 50, 110, 25)
		show_text("acc, turn :"+str(outputs), 50, 140, 25)
		show_text("position :"+str(car_pos), 50, 180, 20)
	# else:
		# print("fps : ", round(clock.get_fps(), 2))
	time_list.append(time.time())
	if ai_enable:
		show_text(str([round(i, 2) for i in prediction]), window[0]-500, window[1]-100, 25)
		show_text(str([round(i, 2) for i in prediction]), window[0]-500, window[1]-100, 25)
		#comparaison avec utilisateur :
		bon = prediction[1:] == outputs[1:]
		# if bon:
			# show_text("Valid", window[0]-500, window[1]-60, 25, (0, 255, 0))
		# else:	
			# show_text("Nope", window[0]-500, window[1]-60, 25, (255, 0, 0))
	if len(data) != 0:
		inputs, outputs = [data[i][0] for i in range(len(data))], [data[i][1] for i in range(len(data))]
		split_dict_len = {key:len([input for i, input in enumerate(inputs) if outputs[i] == key]) for key in set(outputs)}
		for i, (k, v) in enumerate(split_dict_len.items()):
			show_text("{} :{}".format(k, v), window[0]-250, 100+20*i, 15)

	# 	UPDATE
	clock.tick(fps)
	pygame.display.update()
	game_display.fill((255, 255, 255))
	time_list.append(time.time())
	if show_timelist:
		msg = "{} "*(len(time_list)-1)
		print(msg.format(*[10**3*round(time_list[i+1]-time_list[i], 4) for i in range(len(time_list)-1)]))
	
	# game_display.fill((0, 0, 0))
	# print("time with show functions : ", time.time() - t1)

#to close properly pygame
pygame.quit()

#save the data if enough to train the neural network
if len(data) > 500:
	with open("data/inputs_outputs{}".format(len(data)), "wb") as f:
		p = Pickler(f)
		p.dump(data)
		print("data saved as inputs_outpus{}".format(len(data)))

