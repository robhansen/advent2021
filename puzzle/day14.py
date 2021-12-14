#!/usr/bin/env python3

import sys
import copy

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

pairs_base = {} # key is a pair, value is [pair1, pair2, count]
with open(sys.argv[1]) as file:
    lines = file.readlines()
    for i in range(2,len(lines)):
        pairs_base[lines[i][0:2]]=[lines[i][0]+lines[i][6:7], lines[i][6:7]+lines[i][1], 0]
    pairs_with_data = copy.deepcopy(pairs_base)
    for i in range(0,len(lines[0].rstrip())-1):
        pairs_with_data[lines[0][i:i+2]][2]+=1

def add_count(count_dict, char, val):
    if char not in count_dict:
        count_dict[char] = 0
    count_dict[char]+=val

def polymerise(num_steps, base, pairs, initial_string):
    for i in range(num_steps):
        new_pairs = copy.deepcopy(base)
        for pair, values in pairs.items():
            new_pairs[values[0]][2]+=values[2]
            new_pairs[values[1]][2]+=values[2]
        pairs = new_pairs

    counts = {}
    for pair, values in pairs.items():
        add_count(counts, pair[0], values[2])
        add_count(counts, pair[1], values[2])
    add_count(counts, initial_string[0], 1)
    add_count(counts, initial_string[-1], 1)

    sorted_counts = sorted(counts.items(), key=lambda item: item[1])
    print("Most common {}/2 minus least common {}/2 after {} iterations = {}".format(sorted_counts[-1], sorted_counts[0], num_steps, int((sorted_counts[-1][1]-sorted_counts[0][1])/2)))

polymerise(10, pairs_base, pairs_with_data.copy(), lines[0].rstrip())
polymerise(40, pairs_base, pairs_with_data.copy(), lines[0].rstrip())
