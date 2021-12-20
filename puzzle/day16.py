#!/usr/bin/env python3

import sys
import math

OPERATORS = {
    0: (lambda a: sum(a)),
    1: (lambda a: math.prod(a)),
    2: (lambda a: min(a)),
    3: (lambda a: max(a)),
    5: (lambda a: 1 if a[0]>a[1] else 0),
    6: (lambda a: 1 if a[0]<a[1] else 0),
    7: (lambda a: 1 if a[0]==a[1] else 0),
}

class Reader:
    def __init__(self, hex_string):
        self.bstring = "".join([bin(int(x, 16))[2:].zfill(4) for x in list(hex_string)])
        self.version_sum = 0
        self.value_sum = 0

    def pop_value(self, num_bits):
        val_string = self.bstring[:num_bits]
        self.bstring = self.bstring[num_bits:]
        return int(val_string, 2)

    def readLiteral(self):
        binary_value_string = ""
        while True:
            final_bit = self.bstring[0:1]
            binary_value_string += self.bstring[1:5]
            self.bstring = self.bstring[5:]
            if final_bit=="0":
                break
        return int(binary_value_string, 2)

    def readPacket(self):
        version = self.pop_value(3)
        self.version_sum+=version
        id_val = self.pop_value(3)
        if id_val == 4: # literal value
            return self.readLiteral()
        else: # operator
            length_id = self.pop_value(1)
            subpackets = []
            if length_id==1:
                num_sub_packets = self.pop_value(11)
                for i in range(num_sub_packets):
                    subpackets.append(self.readPacket())
            else:
                num_bits_for_subpackets = self.pop_value(15)
                len_bstring = len(self.bstring)
                while num_bits_for_subpackets>(len_bstring-len(self.bstring)):
                    subpackets.append(self.readPacket())
            return OPERATORS[id_val](subpackets)

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

with open(sys.argv[1]) as file:
    reader = Reader(file.readline().rstrip())

print("Value = {}".format(reader.readPacket()))
print("Version sum = {}".format(reader.version_sum))
