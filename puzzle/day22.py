#!/usr/bin/env python3

import sys
import numpy

USE_CUBOIDS_METHOD = True # False (cubes method) only suitable for small, bounded areas, else matrix is too large to allocate

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

class ReactorCubes: # uses a numpy matrix of cubes
    def __init__(self, min_dim, max_dim):
        self.max_dim = max_dim
        self.min_dim = min_dim ## offset
        self.size = (max_dim-min_dim)+1
        self.cubes = numpy.zeros((self.size,self.size,self.size), dtype=int)

    def range_valid(self, rng):
        return (rng[0] <= self.max_dim and rng[1] >= self.min_dim)

    def limit_to_bounds(self, rng):
        return (max(rng[0], self.min_dim), min(rng[1], self.max_dim))

    def step(self, x_rng, y_rng, z_rng, value): # 2-element lists/tuples, inclusive of each
        if not self.range_valid(x_rng) or not self.range_valid(y_rng) or not self.range_valid(z_rng):
            return
        x_rng = self.limit_to_bounds(x_rng)
        y_rng = self.limit_to_bounds(y_rng)
        z_rng = self.limit_to_bounds(z_rng)
        for x in range(x_rng[0], x_rng[1]+1):
            for y in range(y_rng[0], y_rng[1]+1):
                for z in range(z_rng[0], z_rng[1]+1):
                    self.cubes[z+self.min_dim][y+self.min_dim][x+self.min_dim] = value

    def cubes_on(self):
        return numpy.sum(self.cubes)

class ReactorCuboids: # tracks individual cuboids, subdividing when they intersect
    def __init__(self):
        self.cubes = []

    def intersect(self, to_intersect, intersector):
        for i in range(3):
            if intersector[i][1] < to_intersect[i][0] or intersector[i][0] > to_intersect[i][1]:
                return [to_intersect]
        cubes = []
        if to_intersect[2][1] > intersector[2][1]: # top
            cubes.append((to_intersect[0], to_intersect[1], (intersector[2][1]+1, to_intersect[2][1]), to_intersect[3]))
        if to_intersect[2][0] < intersector[2][0]: # bottom
            cubes.append((to_intersect[0], to_intersect[1], (to_intersect[2][0], intersector[2][0]-1), to_intersect[3]))
        height = (max(to_intersect[2][0], intersector[2][0]),min(to_intersect[2][1], intersector[2][1]))
        if to_intersect[1][1] > intersector[1][1]: # front
            cubes.append((to_intersect[0], (intersector[1][1]+1, to_intersect[1][1]), height, to_intersect[3]))
        if to_intersect[1][0] < intersector[1][0]: # back
            cubes.append((to_intersect[0], (to_intersect[1][0], intersector[1][0]-1), height, to_intersect[3]))
        depth = (max(to_intersect[1][0], intersector[1][0]),min(to_intersect[1][1], intersector[1][1]))
        if to_intersect[0][1] > intersector[0][1]: # right
            cubes.append(((intersector[0][1]+1, to_intersect[0][1]), depth, height, to_intersect[3]))
        if to_intersect[0][0] < intersector[0][0]: # left
            cubes.append(((to_intersect[0][0], intersector[0][0]-1), depth, height, to_intersect[3]))
        return cubes

    def step(self, x_rng, y_rng, z_rng, value): # 2-element lists/tuples, inclusive of each
        updated_cubes = [(x_rng, y_rng, z_rng, value)]
        for cube in self.cubes:
            updated_cubes += self.intersect(cube, updated_cubes[0])
        self.cubes = updated_cubes

    def cubes_on(self):
        on = 0
        for cube in self.cubes:
            if cube[3] == 1:
                on += (cube[0][1]-cube[0][0]+1)*(cube[1][1]-cube[1][0]+1)*(cube[2][1]-cube[2][0]+1)
        return on

def get_range(range_string):
    ranges = range_string.split("..")
    return [int(x) for x in ranges]

reactor = ReactorCuboids() if USE_CUBOIDS_METHOD else ReactorCubes(-50, 50)
with open(sys.argv[1]) as file:
    for line in file:
        tokens = line.rstrip().split(" ")
        dims = tokens[1].split(",")
        reactor.step(get_range(dims[0][2:]), get_range(dims[1][2:]), get_range(dims[2][2:]), 1 if tokens[0]=="on" else 0)
print("{} cubes on".format(reactor.cubes_on()))
