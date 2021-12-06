#!/usr/bin/env python3

import sys

MAX_DAYS = 256
REPORT_AFTER = (80,256)

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

time_to_spawn = [0] * 9 # buckets representing counts of fish with 0 to 9 days until spawning

with open(sys.argv[1]) as file:
    for tts in file.readline().split(","):
        time_to_spawn[int(tts)]+=1

for i in range(1, MAX_DAYS+1):
    num_spawning = time_to_spawn.pop(0)
    time_to_spawn[6] += num_spawning
    time_to_spawn.append(num_spawning)
    if i in REPORT_AFTER:
        print("After {} days: {} fish".format(i, sum(time_to_spawn)))
