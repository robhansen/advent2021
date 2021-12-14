#!/usr/bin/env python3

import sys
import numpy

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

vals = []
folds = []
with open(sys.argv[1]) as file:
    for line in file:
        if line[0].isnumeric():
            vals.append([int(x) for x in line.rstrip().split(",")])
        if line[0:11]=="fold along ":
            folds.append((line[11], int(line[13:])))

max_vals = [0,0]
for val_pair in vals:
    if val_pair[0] > max_vals[0]:
        max_vals[0] = val_pair[0]
    if val_pair[1] > max_vals[1]:
        max_vals[1] = val_pair[1]

paper = numpy.zeros((max_vals[1]+1,max_vals[0]+1))
for val_pair in vals:
    paper[val_pair[1]][val_pair[0]] = 1

for fold in folds:
    base = paper.copy()[0:fold[1] if fold[0]=="y" else None,0:fold[1] if fold[0]=="x" else None]
    overlay = paper.copy()[fold[1]+1 if fold[0]=="y" else 0:,fold[1]+1 if fold[0]=="x" else None:]
    overlay = numpy.flip(overlay,0 if fold[0]=="y" else 1)
    paper = numpy.minimum(base + overlay, 1)
    print("Folded {}={}: {} dots visible".format(fold[0], fold[1], numpy.sum(paper)))

for row in paper:
    print("".join(["#" if x>0 else " " for x in row]))





