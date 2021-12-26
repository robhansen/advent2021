#!/usr/bin/env python3

import sys
import numpy

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

TRANSLATIONS = [(0,0,0),(0,0,1),(0,0,2),(0,0,3),(0,1,0),(0,1,1),(0,1,2),(0,1,3),(0,2,3),(0,3,3),
                (1,0,0),(1,0,1),(1,0,2),(1,0,3),(1,1,0),(1,1,1),(1,1,2),(1,1,3),(1,2,3),(1,3,3),
                (2,0,0),(2,0,1),(2,0,2),(2,0,3),(2,1,0),(2,1,1),(2,1,2),(2,1,3),(2,2,3),(2,3,3),
                (3,0,0),(3,0,1),(3,0,2),(3,0,3),(3,1,0),(3,1,1),(3,1,2),(3,1,3),(3,2,3),(3,3,3)]
COS = [1,0,-1,0]
SIN = [0,1,0,-1]
def get_rotation_matrix(a,b,c): # rotation indexes (0,1,2,3) of z,y,x respectively
    matrix = numpy.zeros((3,3), dtype=int)
    numpy.put(matrix, range(9), [COS[a]*COS[b], (COS[a]*SIN[b]*SIN[c])-(SIN[a]*COS[c]), (COS[a]*SIN[b]*COS[c])+(SIN[a]*SIN[c]),
                                SIN[a]*COS[b], (SIN[a]*SIN[b]*SIN[c])+(COS[a]*COS[c]), (SIN[a]*SIN[b]*COS[c])-(COS[a]*SIN[c]),
                                0-SIN[b],       COS[b]*SIN[c],                          COS[b]*COS[c]])
    return matrix

class Scanner:
    def __init__(self):
        self.beacons = []
        self.vector_list_bidirectional = set()
        self.vector_list_lookup_table = {}
        self.canon = False
        self.origin = numpy.array([0,0,0])

    def add_beacon(self, beacon_string):
        self.beacons.append(numpy.array([int(x) for x in beacon_string.split(",")]))

    def calculate_canonical_vectors(self):
        self.canon = True
        for i in range(len(self.beacons)):
            for j in range(len(self.beacons)):
                if j!=i:
                    vector = self.beacons[i]-self.beacons[j]
                    self.vector_list_bidirectional.add(tuple(vector.tolist())) # convert to tuple so it's hashable
                    self.vector_list_lookup_table[tuple(vector.tolist())] = (i,j)
    
    def get_vectors(self, rotation_indices):
        vector_list = set()
        for i in range(len(self.beacons)):
            for j in range(len(self.beacons)):
                if j>i: # for efficiency just get the ones in one direction, not their negatives too
                    vector = numpy.array(self.beacons[i])-numpy.array(self.beacons[j])
                    vector_list.add(tuple(numpy.dot(get_rotation_matrix(*rotation_indices), vector).tolist()))
        return vector_list

    def match_to(self, scanner, threshold):
        most_matches = [[], None]
        for t in TRANSLATIONS:
            inter = scanner.vector_list_bidirectional.intersection(self.get_vectors(t))
            if len(inter)>len(most_matches[0]):
                most_matches = [inter, t]
        if len(most_matches[0]) >= threshold: # match orientation and origin to that of scanner
            for i in range(len(self.beacons)):
                self.beacons[i] = numpy.dot(get_rotation_matrix(*most_matches[1]), self.beacons[i])
            self.calculate_canonical_vectors() # sets canon to True
            ref_vector = most_matches[0].pop()
            position_correction = scanner.beacons[scanner.vector_list_lookup_table[ref_vector][0]] - self.beacons[self.vector_list_lookup_table[ref_vector][0]]
            self.origin += position_correction
            for i in range(len(self.beacons)):
                self.beacons[i] += position_correction
            return True
        return False

scanners = []
with open(sys.argv[1]) as file:
    for line in file:
        if len(line) > 4:
            if line[:3] == "---":
                scanners.append(Scanner())
            else:
                scanners[-1].add_beacon(line.rstrip())

scanners[0].calculate_canonical_vectors() # use scanners[0] as the canonical orientation and position
canon_count = 1
while canon_count < len(scanners):
    for i in range(len(scanners)):
        for j in range(1, len(scanners)):
            if scanners[i].canon and not scanners[j].canon:
                if scanners[j].match_to(scanners[i], 12):
                    canon_count+=1
                    print("Matched scanner {} to {} - {} canon of {}".format(j,i,canon_count,len(scanners)))

all_beacons = set()
for scanner in scanners:
    for beacon in scanner.beacons:
        all_beacons.add(tuple(beacon.tolist()))
print("{} unique beacons".format(len(all_beacons)))

def manhatten_distance(a,b):
    return (abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2]))

max_distance = [0, None, None]
for i in range(len(scanners)):
    for j in range(len(scanners)):
        if manhatten_distance(scanners[i].origin, scanners[j].origin) > max_distance[0]:
            max_distance = [manhatten_distance(scanners[i].origin, scanners[j].origin), scanners[i].origin, scanners[j].origin]
print ("Max Manhatten distance {} between {} and {}".format(*max_distance))
