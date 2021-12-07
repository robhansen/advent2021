import sys

def calculate_absolute_error(positions, target):
    err = 0
    for pos in positions:
        err += abs(pos-target)
    return err

def calculate_error_updated(positions, target):
    err = 0
    for pos in positions:        
        n = abs(pos-target)
        err += int((n*(n+1))/2) # error value is a triangular number
    return err

if len(sys.argv) != 2:
    print("Help: {} <filename>".format(sys.argv[0]))
    sys.exit(0)

positions = []
with open(sys.argv[1]) as file:
    positions = [int(x) for x in file.readline().rstrip().split(",")]

least_fuel = calculate_absolute_error(positions, 0)
least_fuel_index = 0
for i in range(1, max(positions)+1):
    fuel = calculate_absolute_error(positions, i)
    if fuel < least_fuel:
        least_fuel = fuel
        least_fuel_index = i

print("Moving to position {} costs {} fuel".format(least_fuel_index, least_fuel))

least_fuel = calculate_error_updated(positions, 0)
least_fuel_index = 0
for i in range(1, max(positions)+1):
    fuel = calculate_error_updated(positions, i)
    if fuel < least_fuel:
        least_fuel = fuel
        least_fuel_index = i

print("Updated: moving to position {} costs {} fuel".format(least_fuel_index, least_fuel))