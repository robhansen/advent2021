#!/usr/bin/env python3

import sys
import numpy

SEAFLOOR_DIM = 1000 # could be dynamic based on max dimension seen in the input data, but I am lazy

def clamp(val): 
	return max(-1, min(-1, value))

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

lines = [] # list of 2-element list [start,end] of 2-element numpy arrays [x,y]
with open(sys.argv[1]) as file:
    for line in file:
    	lines.append([numpy.array([int(y) for y in x.split(",")]) for x in line.rstrip().split(" -> ")])

seafloor = numpy.zeros((SEAFLOOR_DIM,SEAFLOOR_DIM))

# horizontal/vertical only
for line in lines:
	if line[0][0] == line[1][0] or line[0][1] == line[1][1]: # is horizontal or vertical
		point = line[0]
		direction = numpy.clip(numpy.subtract(line[1], line[0]), -1, 1)

		while True:
			seafloor[point[1]][point[0]] += 1
			if (point==line[1]).all():
				break
			point = numpy.add(point,direction)

print("Got {} positions with 2+ reading (no diagonals)".format((seafloor > 1).sum()))

seafloor = numpy.zeros((SEAFLOOR_DIM,SEAFLOOR_DIM))

for line in lines:
	point = line[0]
	direction = numpy.clip(numpy.subtract(line[1], line[0]), -1, 1)

	while True:
		seafloor[point[1]][point[0]] += 1
		if (point==line[1]).all():
			break
		point = numpy.add(point,direction)

print("Got {} positions with 2+ reading (with diagonals)".format((seafloor > 1).sum()))



