import numpy as np

def distance(p1, p2):
	return np.linalg.norm( np.array(p1) - np.array(p2) )

def line_equation(p1, p2):
	"give cartesian equation (ax+by=c) of the line defined by the two points p1 and p2"
	slope = np.array(p2)-np.array(p1)
	a, b = slope
	a, b = b, -a
	# print(a, b)
	c = a*p1[0] + b*p1[1]
	return a, b, c
	
def line_equation2(p1, p2):								
	"give the perpendicular line of the line defined by (p1, p2)"
	p2, p1 = np.array(p2), np.array(p1)
	slope = p2 - p1
	middle = (p2+p1)/2
	print(p1, p2, middle)
	a, b = slope
	if a:
		a, b = 1, b/a
	else:
		print("ici a est nul")
		a, b = 0, 1
	# print(a, b)
	c = a*middle[0] + b*middle[1]
	return a, b, c

def collision2(segment1, segment2):	#less efficient
	"vector : ( (x1, y1), (x2, y2) )"
	p1, p2 = segment1
	q1, q2 = segment2
	r, s = p2-p1, q2-q1
	s_r = np.cross(s, r)
	if s_r != 0:	# not parrallel
		diff = q1-p1
		t = np.cross(diff, s)/s_r
		u = np.cross(diff, r)/s_r
		if 0 <= t <= 1 and 0 <= u <= 1:
			return p1 + t*r
	return False
	
	
def collision(segment1, segment2):
# def collision_cartesian_equations(segment1, segment2):
	"return the intersection point if it exist anf if not return (0, 0)"
	p1, p2 = segment1
	p3, p4 = segment2
	a1, b1, c1 = line_equation(p1, p2)
	a2, b2, c2 = line_equation(p3, p4)
	# print(a1, b1, c1)
	# print(a2, b2, c2)
	#denominator calculation
	denom = a1*b2 - b1*a2
	if denom == 0:
		# segments // : cannot intersect if c1 != c2
		return (c1 == c2)
	else:
		#intersection point calculation
		x = (c1*b2-b1*c2) / denom
		y = (a1*c2-c1*a2) / denom
		# (x, y) should belong to the two segments:
		if min(p1[0], p2[0]) <= x <= max(p1[0], p2[0]) and min(p3[0], p4[0]) <= x <= max(p3[0], p4[0]):				# conditions sur x
			if min(p1[1], p2[1]) <= y <= max(p1[1], p2[1]) and min(p3[1], p4[1]) <= y <= max(p3[1], p4[1]):			# conditions sur y
				return x, y
		return (0, 0)
	

if __name__ == "__main__":
	from random import randrange
	from matplotlib import pyplot as plt
	
	while True:
		m = False
		while not m:
			points = [(randrange(0, 5), randrange(0, 5)) for i in range(4)]
			m = collision((points[0], points[1]), (points[2], points[3]))
			
		#let's test some functions
		
		color = ('green', 'blue')
		for i in range(2):
			xs, ys = (points[2*i][0], points[2*i+1][0]), (points[2*i][1], points[2*i+1][1])
			plt.plot(xs, ys, color=color[i])
			
		#show the perpendicular line
		a, b, c = line_equation2(points[0], points[1])
		print("a, b, c =", a, b, c)
		if b:
			x1, x2 = points[0][0], points[1][0]
			y1 = (c-a*x1)/b
			y2 = (c-a*x2)/b
		else:
			print("b is null")
			y1, y2 = points[0][1], points[1][1]
			x1 = (c-b*y1)/a
			x2 = (c-b*y2)/a
		print("perpedicular : ", (x1, y1), (x2, y2))
		plt.plot((x1, x2), (y1, y2), color="red")

		if m:
			plt.scatter(m[0], m[1])
		plt.axis("equal")
		plt.show()