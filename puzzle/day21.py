#!/usr/bin/env python3
import copy

import sys

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

starting = []
with open(sys.argv[1]) as file:
    for line in file:
        starting.append([int(line.rstrip().split(": ")[1])-1, 0]) # [position-1, score]

class Die:
    def __init__(self):
        self.current = -1
        self.rolled = 0

    def roll(self):
        self.current+=1
        self.rolled+=1
        return (self.current%100)+1

players = copy.deepcopy(starting)
die = Die()
turn = 0
while max([x[1] for x in players]) < 1000:
    i = turn%len(players)
    turn+=1
    players[i][0] = (players[i][0]+die.roll()+die.roll()+die.roll())%10
    players[i][1] += (players[i][0]+1)

print("Deterministic: Low score = {}, die rolled {} times, which multiply to {}".format(min(x[1] for x in players), die.rolled, min(x[1] for x in players)*die.rolled))

# ---- Part 2 - pretty much entirely independent from part 1 ----------------------------

class StateTracker:
    def __init__(self, pos): # list of two positions
        self.current = {(pos, (0,0), 0): 1}
        self.wins = [0,0]

    def add_state(self, prev_pos, prev_score, prev_turn, next_turn, roll_sum, count): # tuple of two positions, tuple of two scores, index of whose turn is next
        pos = ((prev_pos[0]+roll_sum)%10 if prev_turn==0 else prev_pos[0],(prev_pos[1]+roll_sum)%10 if prev_turn==1 else prev_pos[1])
        score = ((prev_score[0]+pos[0]+1 if prev_turn==0 else prev_score[0]),(prev_score[1]+pos[1]+1 if prev_turn==1 else prev_score[1]))
        if score[prev_turn] > 20:
            self.wins[prev_turn] += count
        else:
            try:
                self.current[(pos, score, next_turn)] += count
            except KeyError:
                self.current[(pos, score, next_turn)] = count

    def step(self):
        prev = self.current
        self.current = {}
        for state, count in prev.items():
            next_turn = (state[2]+1)%2
            self.add_state(state[0],state[1],state[2],next_turn,3,1*count)
            self.add_state(state[0],state[1],state[2],next_turn,4,3*count)
            self.add_state(state[0],state[1],state[2],next_turn,5,6*count)
            self.add_state(state[0],state[1],state[2],next_turn,6,7*count)
            self.add_state(state[0],state[1],state[2],next_turn,7,6*count)
            self.add_state(state[0],state[1],state[2],next_turn,8,3*count)
            self.add_state(state[0],state[1],state[2],next_turn,9,1*count)

    def find_winners(self):
        while len(self.current) > 0:
            self.step()
        print("Quantum: {} wins for p1, {} wins for p2 (Max wins {})".format(self.wins[0], self.wins[1], max(self.wins)))

tracker = StateTracker((starting[0][0],starting[1][0]))
tracker.find_winners()
