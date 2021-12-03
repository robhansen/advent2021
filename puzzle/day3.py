#!/usr/bin/env python3

import sys

def reduce_to_one(candidates, num_bits, match_greater):
    bitmask = 1 << (num_bits-1)
    while len(candidates) > 1:
        count = 0.0
        for candidate in candidates:
            if candidate & bitmask:
                count += 1.0
        match = 0
        if (count / len(candidates) >= 0.5) and match_greater:
            match = bitmask
        elif (count / len(candidates) < 0.5) and not match_greater:
            match = bitmask
        new_candidates = []
        for candidate in candidates:
            if (candidate & bitmask) == match:
                new_candidates.append(candidate)
        candidates = new_candidates
        bitmask = bitmask >> 1
    return candidates[0]

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

codes = []
with open(sys.argv[1]) as file:
    for line in file:
        codes.append(int(line.rstrip(), 2))
        NUMBER_OF_BITS = len(line.rstrip())

bitmask = 1 << (NUMBER_OF_BITS-1)
gamma = 0
for i in range(NUMBER_OF_BITS):
    count = 0.0
    for code in codes:
        if code & bitmask:
            count += 1.0
    gamma = gamma << 1
    bitmask = bitmask >> 1
    if count / len(codes) >= 0.5:
        gamma += 1

epsilon = ((2 ** NUMBER_OF_BITS)-1) ^ gamma
print("gamma = {}, epsilon = {}, combined = {}".format(gamma, epsilon, gamma*epsilon))

oxygen = reduce_to_one(codes.copy(), NUMBER_OF_BITS, True)
co2 = reduce_to_one(codes.copy(), NUMBER_OF_BITS, False)
print("oxygen = {}, co2 = {}, combined = {}".format(oxygen, co2, oxygen*co2))


