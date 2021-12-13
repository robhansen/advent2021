import sys

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

def add_to_graph(key, value):
    if key not in GRAPH:
        GRAPH[key] = []
    GRAPH[key].append(value)

GRAPH = {}
with open(sys.argv[1]) as file:
    for line in file:
        elements = line.rstrip().split("-")
        add_to_graph(elements[0],elements[1])
        add_to_graph(elements[1],elements[0])

def dfs(graph, current, visited, path, extra_visit_allowed):
    path.append(current)
    if current not in visited or current.isupper() or (extra_visit_allowed and current!="start"):
        if current in visited and current.islower():
            extra_visit_allowed = False
        if current == "end":
            valid_paths.append(path)
            return
        visited.add(current)
        for adj in graph[current]:
            dfs(graph, adj, visited.copy(), path.copy(), extra_visit_allowed)

valid_paths = []
dfs(GRAPH, "start", set(), [], False)
print("{} paths with no extra visit".format(len(valid_paths)))

valid_paths = []
dfs(GRAPH, "start", set(), [], True)
print("{} paths with one extra visit".format(len(valid_paths)))


