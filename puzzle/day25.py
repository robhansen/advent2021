#!/usr/bin/env python3

import sys
import numpy

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

with open(sys.argv[1]) as file:
    lines = file.readlines()

cucumbers = numpy.array([0 if x=="." else (1 if x==">" else 3) for x in lines[0].rstrip()], dtype=numpy.uint8)
for line in lines[1:]:
    cucumbers = numpy.vstack([cucumbers,numpy.array([0 if x=="." else (1 if x==">" else 3) for x in line.rstrip()])])

def step(cucumbers):
    dirty = False
    for right in [True,False]:
        advance = numpy.zeros(cucumbers.shape, dtype=numpy.int8)
        for i in range(cucumbers.shape[1]):
            for j in range(cucumbers.shape[0]):
                i_next = (i+1)%cucumbers.shape[1] if right else i
                j_next = (j+1)%cucumbers.shape[0] if not right else j
                if cucumbers[j][i] == (1 if right else 3) and cucumbers[j_next][i_next] == 0:
                    dirty = True
                    advance[j_next][i_next] = 1 if right else 3
                    advance[j][i] = 0 - (1 if right else 3)
        cucumbers += advance
    return dirty

steps = 1
while step(cucumbers):
    steps+=1

print("{} steps until it stalls".format(steps))
