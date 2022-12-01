#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

import itertools as it
  
def backward(A, B, C, z2, w):
    """The possible values of z before a single block
    if the final value of z is z2 and w is w"""
    zs = []
    x = z2 - w - B
    if x % 26 == 0:
        zs.append(x//26 * C)
    if 0 <= w-A < 26:
        z0 = z2 * C
        zs.append(w-A+z0)
        
    return zs

def solve(forward,diffs):
    zs = {0}
    result = {}
    for A,B,C in zip(diffs[1][::-1],diffs[2][::-1],diffs[0][::-1]):
        newzs = set()
        for z in zs:
            for w in range(1 if forward else 9, 10 if forward else 0, 1 if forward else -1):
                #print(w,z)
                z0s = backward(A,B,C,z,w)
                for z0 in z0s:
                    newzs.add(z0)
                    result[z0] = (w,) + result.get(z, ())
        zs = newzs
    return ''.join(str(digit) for digit in result[0])

iterations = []
itera = None
with open(sys.argv[1]) as file:
    for line in file:
        if line[0:3]=="inp":
            if itera is not None:
                iterations.append(itera)
            itera = []
        itera.append(line.rstrip().split(" "))
iterations.append(itera)

diffs = [[],[],[]]
for itera in iterations:
    diffs[0].append(int(itera[4][2]))  # div z <val>
    diffs[1].append(int(itera[5][2]))  # add x <val>
    diffs[2].append(int(itera[15][2])) # add y <val>

print("Max value forward: {}".format(solve(True, diffs)))
print("Max value backward: {}".format(solve(False, diffs)))
#print(solve(2, diffs[2],))