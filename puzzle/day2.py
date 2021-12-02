#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

instructions = []
with open(sys.argv[1]) as file:
    for line in file:
        instructions.append(line.rstrip().split())

print("Got {} instructions".format(len(instructions)))

hoz = 0
depth = 0
print("Calculating simple position")
for instruction in instructions:
    if instruction[0] == "forward":
        hoz += int(instruction[1])
    elif instruction[0] == "down":
        depth += int(instruction[1])
    elif instruction[0] == "up":
        depth -= int(instruction[1])
    else:
        print("Error: Unknown instruction {}".format(instruction[0]))
        sys.exit(0)

    if depth < 0:
        print("Warning: negative depth {}, submarine is airborne".format(depth))

print("Position {} forward, {} down (multiply to {})".format(hoz, depth, hoz*depth))

hoz = 0
depth = 0
aim = 0
print("Calculating more complex position")
for instruction in instructions:
    if instruction[0] == "forward":
        hoz += int(instruction[1])
        depth += int(instruction[1])*aim
    elif instruction[0] == "down":
        aim += int(instruction[1])
    elif instruction[0] == "up":
        aim -= int(instruction[1])
    else:
        print("Error: Unknown instruction {}".format(instruction[0]))
        sys.exit(0)

    if depth < 0:
        print("Warning: negative depth {}, submarine is airborne".format(depth))

print("Position {} forward, {} down (multiply to {})".format(hoz, depth, hoz*depth))
