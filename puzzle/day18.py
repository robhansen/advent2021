#!/usr/bin/env python3

import sys
import queue
import numbers
import math

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

class Number:
    def __init__(self, number_string):
        self.arr = [int(x) if x.isnumeric() else x for x in list(number_string)]

    def process(self, split):
        rhs = False
        stack = queue.LifoQueue() # stack of bools, False=left side, True=right side
        for i in range(len(self.arr)):
            if self.arr[i]=="[":
                stack.put(rhs)
                rhs = False
            elif self.arr[i]=="]":
                stack.get()
            elif self.arr[i]==",":
                rhs = True
            else:
                if not split and rhs and stack.qsize()>4:
                    for j in range(i-3,0,-1): # don't need to check 0 as it must be a "["
                        if isinstance(self.arr[j], numbers.Number):
                            self.arr[j] += self.arr[i-2]
                            break
                    for j in range(i+1,len(self.arr)):
                        if isinstance(self.arr[j], numbers.Number):
                            self.arr[j] += self.arr[i]
                            break
                    self.arr = self.arr[:i-3]+[0]+self.arr[i+2:]
                    return True
                elif split and self.arr[i]>9:
                    new_pair = ["[", math.floor(self.arr[i]/2.0), ",", math.ceil(self.arr[i]/2.0), "]"]
                    self.arr = self.arr[:i]+new_pair+self.arr[i+1:]
                    return True
                rhs = True
        return False

    def reduce(self):
        return (self.process(False) or self.process(True))

    def add(self, number):
        self.arr.insert(0,"[")
        self.arr.append(",")
        self.arr.extend(number.arr)
        self.arr.append("]")
        while self.reduce():
            pass

    def get_string(self):
        to_string = ""
        for char in self.arr:
            to_string+=str(char) if isinstance(char, numbers.Number) else char
        return to_string
    def get_magnitude(self): # pop pop
        while len(self.arr) > 1:
            for i in range(len(self.arr)):
                if isinstance(self.arr[i], numbers.Number) and i>1 and self.arr[i-1]=="," and isinstance(self.arr[i-2], numbers.Number):
                    self.arr = self.arr[:i-3]+[(3*self.arr[i-2])+(2*self.arr[i])]+self.arr[i+2:]
                    break
        return self.arr[0]

with open(sys.argv[1]) as file:
    lines = file.readlines()

base = None
for line in lines:
    if base is None:
        base = Number(line.rstrip())
    else:
        base.add(Number(line.rstrip()))
print("{} has magnitude {}".format(base.get_string(), base.get_magnitude()))

max_magnitude = 0
for i in range(len(lines)):
    for j in range(len(lines)):
        if i!=j:
            trial = Number(lines[i].rstrip())
            trial.add(Number(lines[j].rstrip()))
            if trial.get_magnitude() > max_magnitude:
                max_magnitude = trial.get_magnitude()
print("Max magnitude = {}".format(max_magnitude))