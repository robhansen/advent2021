#!/usr/bin/env python3

import sys

iterations = []
with open("day24_input.txt") as file:
    itera = None
    for line in file:
        if line[0:3]=="inp":
            if itera is not None:
                iterations.append(itera)
            itera = []
        itera.append(line.rstrip())
iterations.append(itera)

for i in range(16):
    print("\nLine {}".format(i))
    for itera in iterations:
        print(itera[i])
