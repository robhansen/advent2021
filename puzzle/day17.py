#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

with open(sys.argv[1]) as file:
    segments = file.readline().rstrip().split(", ")
    target = ([int(x) for x in segments[0][15:].split("..")], [int(x) for x in segments[1][2:].split("..")])

def eval(vel):
    max_y = 0
    pos = [0,0]
    while pos[1]>=target[1][0]:
        pos[0] += vel[0]
        pos[1] += vel[1]
        if vel[0]>0:
            vel[0]-=1
        elif vel[0]<0:
            vel[0]+=1
        vel[1]-=1
        if pos[1] > max_y:
            max_y = pos[1]
        if pos[0]>=target[0][0] and pos[0]<=target[0][1] and pos[1]>=target[1][0] and pos[1]<=target[1][1]:
            return True,max_y
    return False,None

best_max_y = target[1][0]-1
pos_for_max_y = [None,None]
within_target = 0
for x in range(0, target[0][1]+1):
    for y in range(target[1][0], 400):# not really a great way to set the maximum y-velocity
        in_target,max_y = eval([x,y])
        if in_target:
            within_target+=1
            if max_y > best_max_y:
                best_max_y = max_y
                pos_for_max_y = [x,y]

print("Max y={} at {}".format(best_max_y,pos_for_max_y))
print("{} valid initial velocities".format(within_target))
