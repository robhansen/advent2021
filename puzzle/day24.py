#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

INSTRUCTIONS = {
    "inp": (lambda a, s: s.inputs.pop()),
    "add": (lambda a, s: s.vars[a[0]] + s.vars[a[1]]),
    "mul": (lambda a, s: s.vars[a[0]] * s.vars[a[1]]),
    "div": (lambda a, s: int(s.vars[a[0]] / s.vars[a[1]])),
    "mod": (lambda a, s: s.vars[a[0]] % s.vars[a[1]]),
    "eql": (lambda a, s: 1 if s.vars[a[0]] == s.vars[a[1]] else 0),
}

class ALU:
    def __init__(self, inputs):
        self.vars = {"w": 0, "x": 0, "y": 0, "z": 0, "num": 0}
        self.inputs = inputs
    def input_contains(self, contain):
        return contain in self.inputs
    def process(self, instruction_tokens):
        if len(instruction_tokens)==3 and (instruction_tokens[2][0].isnumeric() or instruction_tokens[2][0]=="-"):
            self.vars["num"] = int(instruction_tokens[2])
            instruction_tokens[2] = "num"
        #print(instruction_tokens, self.vars)
        self.vars[instruction_tokens[1]] = INSTRUCTIONS[instruction_tokens[0]](instruction_tokens[1:], alu)

instructions = []
with open(sys.argv[1]) as file:
    for line in file:
        instructions.append(line.rstrip().split(" "))
model = 99999999999999
while True:
    #print("trying {}".format(model))
    alu = ALU([int(x) for x in str(model)])
    if not alu.input_contains(0):
        for instruction in instructions:
            alu.process(instruction.copy())
        if alu.vars["z"] == 0:
            break
    model-=1
print("Model number {} is valid".format(model))
