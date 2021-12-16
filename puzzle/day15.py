#!/usr/bin/env python3

import sys
import networkx as nx

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

def solve_graph(filename, expansion):
    graph = nx.DiGraph()
    risks = []
    with open(sys.argv[1]) as file:
        lines = file.readlines()
        for i in range(expansion):
            for line in lines:
                new_row = []
                for j in range(expansion):
                    new_row.extend([((int(x)+i+j-1)%9)+1 for x in list(line.rstrip())])
                risks.append(new_row)

    for y in range(len(risks)):
        for x in range(len(risks[0])):
            # add right and down edges in each direction
            if x < len(risks[0])-1:
                graph.add_edge((x,y), (x+1,y), weight=risks[y][x+1])
                graph.add_edge((x+1,y), (x,y), weight=risks[y][x])
            if y < len(risks)-1:
                graph.add_edge((x,y), (x,y+1), weight=risks[y+1][x])
                graph.add_edge((x,y+1), (x,y), weight=risks[y][x])

    length = nx.shortest_path_length(graph, source=(0,0), target=(len(risks[0])-1,len(risks)-1),weight='weight',method='bellman-ford')
    print("Shortest path with {} expansions = {}".format(expansion, length))

solve_graph(sys.argv[1], 1)
solve_graph(sys.argv[1], 5)