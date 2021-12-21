#!/usr/bin/env python3

import sys
import numpy

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

with open(sys.argv[1]) as file:
    lines = file.readlines()

def enhance(enhance):
    padding = enhance+1
    width = len(lines[2].rstrip())+(2*padding)
    height = len(lines[2:])+(2*padding)
    images = [numpy.zeros((width,height), dtype=numpy.int8)]

    lookup_array = [0 if x=="." else 1 for x in list(lines[0].rstrip())]
    pad_array = [0] * padding
    for i in range(padding, len(lines[2:])+padding):
        numpy.put(images[0], range((i*width),(i*width)+width), pad_array+[0 if x=="." else 1 for x in list(lines[i+2-padding].rstrip())]+pad_array)

    border_value = 0
    for e in range(0, enhance):
        border_value = lookup_array[int(str(border_value) * 9, 2)]
        images.append(numpy.full((width,height), border_value, dtype=numpy.int8))
        for y in range(1,height-1):
            for x in range(1,width-1):
                index_str = ""
                for i in range(-1,2):
                    for j in range(-1,2):
                        index_str += str(images[e][y+i][x+j])
                images[e+i][y][x] = lookup_array[int(index_str, 2)]
        #print(images[e+1])
    print("After {} enhancements, {} illuminated".format(e+1, numpy.sum(images[e+1])))

enhance(2)
enhance(50)



	