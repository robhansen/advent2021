#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

readings = []
with open(sys.argv[1]) as file:
    for line in file:
        readings.append(int(line.rstrip()))

print("Got {} readings".format(len(readings)))

increments = 0
prev = None
for reading in readings:
    if prev is not None and reading > prev:
        increments += 1
    prev = reading

print("{} increments (individual)".format(increments))

WINDOW_SIZE = 3
increments = 0
prev = 0
for i in range(WINDOW_SIZE):
    prev += readings[i]
for i in range(WINDOW_SIZE, len(readings)):
    value = (prev + readings[i])-readings[i-WINDOW_SIZE]
    if value > prev:
        increments += 1
    prev = value

print("{} increments (window size {})".format(increments, WINDOW_SIZE))