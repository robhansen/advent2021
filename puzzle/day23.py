#!/usr/bin/env python3

import sys
import queue
import copy
import time

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

POD = {"A": 0, "B": 1, "C": 2, "D": 3}
ROOM_POSITIONS = [2,4,6,8]
COSTS = [1,10,100,1000]

class State:
    def __init__(self, *args):
        if len(args) == 1:
            self.hall = [-1,-1,-2,-1,-2,-1,-2,-1,-2,-1,-1]
            self.rooms = [[],[],[],[]]
            for line in args[0]:
                for i in range(4):
                    self.rooms[i].append(POD[line[(2*i)+3]])
            self.cost = 0
            self.steps = 0
            self.depth = len(args[0])
            self.history = []
        else:
            self.hall = args[0]
            self.rooms = args[1]
            self.cost = args[2]
            self.steps = args[3]+1
            self.depth = len(self.rooms[0])

    def __lt__(self, other):
        return True # needed when multiple states in the queue have the same cost - order doesn't matter

    def room_can_leave(self, room_number):
        to_leave = -1
        for i in range(self.depth-1, -1, -1):
            if self.rooms[room_number][i] < 0:
                return to_leave
            elif self.rooms[room_number][i] != room_number or to_leave >= 0:
                to_leave = i
        return to_leave

    def room_can_enter(self, room_number):
        for i in range(self.depth-1, -1, -1):
            if self.rooms[room_number][i] < 0:
                return i
            elif self.rooms[room_number][i] != room_number:
                return -1
        return -1

    def room_to_hall(self, room_number, room_index, hall_index): # return steps (or 0 if invalid)
        for i in range(ROOM_POSITIONS[room_number], hall_index, -1 if hall_index < ROOM_POSITIONS[room_number] else 1):
            if self.hall[i] >= 0:
                return 0
        return room_index+abs(hall_index-ROOM_POSITIONS[room_number])+1

    def hall_to_room(self, room_number, room_index, hall_index): # return steps (or 0 if invalid)
        for i in range(hall_index+(1 if hall_index < ROOM_POSITIONS[room_number] else -1), ROOM_POSITIONS[room_number], 1 if hall_index < ROOM_POSITIONS[room_number] else -1):
            if self.hall[i] >= 0:
                return 0
        return room_index+abs(hall_index-ROOM_POSITIONS[room_number])+1

    def room_to_room(self, room_number_start,room_index_start, room_number_end, room_index_end): # return steps (or 0 if invalid)
        min_hall_index = min(ROOM_POSITIONS[room_number_start], ROOM_POSITIONS[room_number_end])
        max_hall_index = max(ROOM_POSITIONS[room_number_start], ROOM_POSITIONS[room_number_end])
        for i in range(min_hall_index, max_hall_index+1):
            if self.hall[i] >= 0:
                return 0
        return room_index_start+1+(max_hall_index-min_hall_index)+1+room_index_end

    def list_of_valid_nexts(self):
        nexts = []
        for i in range(11): # len(self.hall)
            pod = self.hall[i]
            if pod >=0:
                room_index = self.room_can_enter(pod)
                if room_index>=0:
                    cost = self.hall_to_room(pod, room_index, i)*COSTS[pod]
                    if cost > 0:
                        new_state = State(self.hall.copy(), copy.deepcopy(self.rooms), self.cost, self.steps)
                        new_state.hall[i] = -1
                        new_state.rooms[pod][room_index] = pod
                        new_state.cost += cost
                        nexts.append(new_state)
        for i in range(4): # len(ROOM_POSITIONS)
            room_index = self.room_can_leave(i)
            if room_index >= 0:
                pod = self.rooms[i][room_index]
                for j in range(11): # len(self.hall)
                    if self.hall[j]==-1:
                        cost = self.room_to_hall(i,room_index,j)*COSTS[pod]
                        if cost > 0:                                
                            new_state = State(self.hall.copy(), copy.deepcopy(self.rooms), self.cost, self.steps)
                            new_state.hall[j] = pod
                            new_state.rooms[i][room_index] = -1
                            new_state.cost += cost
                            nexts.append(new_state)
                room_enter_index = self.room_can_enter(pod)
                if room_enter_index>=0:
                    cost = self.room_to_room(i, room_index, pod, room_enter_index)*COSTS[pod]
                    if cost > 0:                                
                        new_state = State(self.hall.copy(), copy.deepcopy(self.rooms), self.cost, self.steps)
                        new_state.rooms[pod][room_enter_index] = -1
                        new_state.rooms[i][room_index] = -1
                        new_state.cost += cost
                        nexts.append(new_state)
        return nexts

    def hashable(self):
        return tuple(self.hall + [tuple(x) for x in self.rooms])

    def heuristic(self):
        # Simple admissable heuristic for A* - minimum cost to move any items not in their right room slot from the closest hall space
        h = 15554 if self.depth == 4 else 5555 # precomputed: for efficiency sum(COSTS)*(2+3) or sum(COSTS)*(2+3+4+5)
        for i in range(4):
            for j in range(self.depth-1, -1, -1):
                if self.rooms[i][j]==i:
                    h -= (j+2)*COSTS[i]
                else:
                    break
        return h

    def finished(self):
        for i in range(4):
            if self.rooms[i][0]!=i or self.rooms[i][1]!=i:
                return False
        return True

def find_best_solution(initial_state):
    start_time = time.time()
    pq = queue.PriorityQueue()
    pq.put((0,initial_state))
    iterations = 1
    seen = set()
    while True:
        state = pq.get()
        if iterations%10000 == 0:
            print("  {} iterations: Queue size {}, {} steps in, cost {}".format(iterations, pq.qsize(), state[1].steps, state[1].cost))
        iterations+=1
        hashable = state[1].hashable()
        if hashable in seen:
            continue
        seen.add(hashable)
        if state[1].finished():
            print("Complete for {} lines after {} iterations in {:.2f} seconds, cost {}".format(state[1].depth, iterations, time.time()-start_time, state[1].cost))
            break
        next_states = state[1].list_of_valid_nexts()
        for next_state in next_states:
            pq.put((next_state.cost+next_state.heuristic(), next_state))


with open(sys.argv[1]) as file:
    lines = file.readlines()
find_best_solution(State(lines[2:4]))
find_best_solution(State([lines[2],"  #D#C#B#A#","  #D#B#A#C#",lines[3]]))
