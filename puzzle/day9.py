import sys

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

heights = []
with open(sys.argv[1]) as file:
    for line in file:
        heights.append([int(x) for x in list(line.rstrip())])

max_x = len(heights[0])
max_y = len(heights)

num_of_low_points = 0
sum_of_risks = 0
for y in range(0, max_y):
    for x in range(0, max_x):
        val = heights[y][x]
        if ((x == 0 or val < heights[y][x-1]) and
           (y == 0 or val < heights[y-1][x]) and
           (x >= (max_x-1) or val < heights[y][x+1]) and
           (y >= (max_y-1) or val < heights[y+1][x])):
            num_of_low_points+=1
            sum_of_risks+=(val+1)

print("Found {} low points, sum of risks {}".format(num_of_low_points, sum_of_risks))

def check_adjacent(x, y):
    score = 0
    if heights[y][x]<9:
        heights[y][x]=9
        score+=1
        if (x>0):
            score+=check_adjacent(x-1,y)
        if (y>0):
            score+=check_adjacent(x,y-1)
        if (x<=max_x-2):
            score+=check_adjacent(x+1,y)
        if (y<=max_y-2):
            score+=check_adjacent(x,y+1)
    return score

basin_sizes = []
for y in range(0, max_y):
    for x in range(0, max_x):
        basin_size = check_adjacent(x,y)
        if basin_size > 0:
            basin_sizes.append(basin_size)

basin_sizes.sort(reverse=True)
print("Found {} basins. Three largest multiple to {}".format(len(basin_sizes), basin_sizes[0]*basin_sizes[1]*basin_sizes[2]))
