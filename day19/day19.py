import time
import numpy as np
from collections import Counter
import itertools
from functools import reduce
import math
import uuid
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

import networkx as nx

def read_file(filename='babyinput.txt'):
    with open(filename) as f:
        lines = f.readlines()
    lines = [str(l.strip()) for l in lines]
    return lines
        
def main():
    print(time.time())
    start = time.time()
    part1()
    middle = time.time()
    part2()
    end = time.time()
    print("Part 1 Time:  " + str(middle-start))
    print("Part 2 Time:  " + str(end-middle))
    print("Total Time:   " + str(end-start))
    
def part1(): 
    print("PART 1:")
    lines = read_file()
    print(len(lines))
    
    #split by blank lines
    scanner_raw = [list(g) for k, g in itertools.groupby(lines, key=bool) if k]
    
    #print(scanner_raw)
    scanners_data = [] 
    for scanner in scanner_raw:
        scanner_data = []
        for coord in scanner[1:]:
            coords = [int(c) for c in coord.split(",")]
            scanner_data.append((coords[0], coords[1], coords[2]))
        scanners_data.append(scanner_data)
    
    #draw(scanners_data)
    print("scanner count: " + str(len(scanners_data)))
    good_map = []
    good_map.extend(scanners_data[0])
    unincorporated = scanners_data[1:]
    colour_map = [1]*len(good_map)
    scanner_locations = [(0,0,0)]
    
    (good_map, unincorporated, colour_map, scanner_locations) = run_through_rotations(good_map, unincorporated, colour_map, scanner_locations)
    
    print("unincorporated scanners: " + str(len(unincorporated)))
    
    for i in range(7):
        #maybe there are some that were unincorporatable earlier, try again. 
        (good_map, unincorporated, colour_map, scanner_locations) = run_through_rotations(good_map, unincorporated, colour_map, scanner_locations)

        print("good_map currently is of length: " + str(len(good_map)))
        print("unincorporated scanners: " + str(len(unincorporated)))
        
        if len(unincorporated) == 0:
            break
        
    print("Final unincorporated scanners: " + str(len(unincorporated)))

    result = len(good_map)
    print("result: " + str(result))
    draw (good_map, colour_map)

def run_through_rotations(good_map, unincorporated, colour_map, scanner_locations):

    #NOTE rotations are *no longer cumulative!*
    rotations = [
        # z (1)
        lambda s: [(x,y,z) for (x,y,z) in s], #0
        lambda s: [(-y,x,z) for (x,y,z) in s], #90
        lambda s: [(-x,-y,z) for (x,y,z) in s], #180
        lambda s: [(y,-x,z) for (x,y,z) in s], #270
        # -z (4)
        lambda s: [(y,x,-z) for (x,y,z) in s], #0
        lambda s: [(-x,y,-z) for (x,y,z) in s], #90
        lambda s: [(-y,-x,-z) for (x,y,z) in s], #180
        lambda s: [(x,-y,-z) for (x,y,z) in s], #270
        #y (2)
        lambda s: [(z,x,y) for (x,y,z) in s], #0
        lambda s: [(-x,z,y) for (x,y,z) in s], #90
        lambda s: [(-z,-x,y) for (x,y,z) in s], #180
        lambda s: [(x,-z,y) for (x,y,z) in s], #270
        # -y (5)
        lambda s: [(x,z,-y) for (x,y,z) in s], #0
        lambda s: [(-z,x,-y) for (x,y,z) in s], #90
        lambda s: [(-x,-z,-y) for (x,y,z) in s], #180
        lambda s: [(z,-x,-y) for (x,y,z) in s], #270
        #z (3)
        lambda s: [(y,z,x) for (x,y,z) in s], #0
        lambda s: [(-z,y,x) for (x,y,z) in s], #90
        lambda s: [(-y,-z,x) for (x,y,z) in s], #180
        lambda s: [(z,-y,x) for (x,y,z) in s], #270
        # -z (6)
        lambda s: [(z,y,-x) for (x,y,z) in s], #0
        lambda s: [(-y,z,-x) for (x,y,z) in s], #90
        lambda s: [(-z,-y,-x) for (x,y,z) in s], #180
        lambda s: [(y,-z,-x) for (x,y,z) in s], #270
    ]
    reverse_rotations = [
        # z (1)
        lambda s: [(x,y,z) for (x,y,z) in s], #0
        lambda s: [(y,-x,z) for (x,y,z) in s], #90
        lambda s: [(-x,-y,z) for (x,y,z) in s], #180
        lambda s: [(-y,x,z) for (x,y,z) in s], #270
        # -z (4)
        lambda s: [(x,y,-z) for (y,x,z) in s], #0
        lambda s: [(-x,y,-z) for (x,y,z) in s], #90
        lambda s: [(-x,-y,-z) for (y,x,z) in s], #180
        lambda s: [(x,-y,-z) for (x,y,z) in s], #270
        #y (2)
        lambda s: [(x,y,z) for (z,x,y) in s], #0
        lambda s: [(-x,y,z) for (x,z,y) in s], #90
        lambda s: [(-x,y,-z) for (z,x,y) in s], #180
        lambda s: [(x,y,-z) for (x,z,y) in s], #270
        # -y (5)
        lambda s: [(x,-y,z) for (x,z,y) in s], #0
        lambda s: [(x,-y,-z) for (z,x,y) in s], #90
        lambda s: [(-x,-y,-z) for (x,z,y) in s], #180
        lambda s: [(-x,-y,z) for (z,x,y) in s], #270
        #z (3)
        lambda s: [(x,y,z) for (y,z,x) in s], #0
        lambda s: [(x,y,-z) for (z,y,x) in s], #90
        lambda s: [(x,-y,-z) for (y,z,x) in s], #180
        lambda s: [(x,-y,z) for (z,y,x) in s], #270
        # -z (6)
        lambda s: [(-x,y,z) for (z,y,x) in s], #0
        lambda s: [(-x,-y,z) for (y,z,x) in s], #90
        lambda s: [(-x,-y,-z) for (z,y,x) in s], #180
        lambda s: [(-x,y,-z) for (y,z,x) in s], #270
        
    ]
    
    for i in range(len(rotations)):
        #rotate
        print(i)
        unincorporated = [rotations[i](scanner) for scanner in unincorporated]
                #print(unincorporated[0][0])
        (good_map, unincorporated, colour_map, scanner_locations) = test_linear_transforms(good_map, unincorporated, colour_map, scanner_locations)
        if len(unincorporated) == 0:
            return (good_map, unincorporated, colour_map, scanner_locations)
        #reset the rotation
        unincorporated = [reverse_rotations[i](scanner) for scanner in unincorporated]
                #print(unincorporated[0][0])
    print("break")
    return (good_map, unincorporated, colour_map, scanner_locations)


def test_linear_transforms(good_map, scanners_data, colour_map, scanner_locations): 
    unincorporated = []
    for scanner_coords in scanners_data:
        transforms_to_try = find_transforms_to_try(good_map, scanner_coords)
        found = False
        #now we have a list of possible linear transforms to try
        for transform in transforms_to_try:
            (tx,ty,tz) = transform
            transformed_coords = [(sx+tx,sy+ty,sz+tz) for (sx,sy,sz) in scanner_coords]
            intersection = [ele1 for ele1 in transformed_coords for ele2 in good_map if ele1 == ele2]
            if len(intersection) >= 12:
                scanner_locations.append(transform)
                #THIS IS THE RIGHT TRANSFORM!
                #add the non-dupes to good_map and break
                for element in transformed_coords:
                    if element in good_map:
                        colour_map[good_map.index(element)] += 1
                    else:
                        good_map.append(element)
                        colour_map.append(1)
                found = True
                print ("found one!" + str(transform))
                break
        if not found: #add to unincorporated list to try after a rotation
            unincorporated.append(scanner_coords)
    return (good_map, unincorporated, colour_map, scanner_locations)


def find_transforms_to_try(good_map, scanner_coords):
    transforms_to_try = []
    for (sx,sy,sz) in scanner_coords: 
        for (gx, gy, gz) in good_map: 
            transforms_to_try.append((gx - sx,gy - sy,gz - sz))
    return transforms_to_try
    
    
def draw(map, colourdata, scanners=None):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    
    xdata = []
    ydata = []
    zdata = []
    for (x,y,z) in map: 
        xdata.append(x)
        ydata.append(y)
        zdata.append(z)
    
    ax.scatter3D(xdata, ydata, zdata, c=colourdata, cmap="winter")
    if scanners is not None:
        x2data = []
        y2data = []
        z2data = []
        for (x,y,z) in scanners: 
            x2data.append(x)
            y2data.append(y)
            z2data.append(z)
    
        ax.scatter3D(x2data, y2data, z2data, c="red", marker="*")
    plt.show()

def part2():
    print("PART 2:")
    lines = read_file()
    print(len(lines))
    
    #split by blank lines
    scanner_raw = [list(g) for k, g in itertools.groupby(lines, key=bool) if k]
    
    #print(scanner_raw)
    scanners_data = [] 
    for scanner in scanner_raw:
        scanner_data = []
        for coord in scanner[1:]:
            coords = [int(c) for c in coord.split(",")]
            scanner_data.append((coords[0], coords[1], coords[2]))
        scanners_data.append(scanner_data)
    
    #draw(scanners_data)
    print("scanner count: " + str(len(scanners_data)))
    good_map = []
    good_map.extend(scanners_data[0])
    unincorporated = scanners_data[1:]
    colour_map = [1]*len(good_map)
    scanner_locations = [(0,0,0)]
    
    (good_map, unincorporated, colour_map, scanner_locations) = run_through_rotations(good_map, unincorporated, colour_map, scanner_locations)

    
    print("unincorporated scanners: " + str(len(unincorporated)))
    
    for i in range(7):
        #maybe there are some that were unincorporatable earlier, try again. 
        (good_map, unincorporated, colour_map, scanner_locations) = run_through_rotations(good_map, unincorporated, colour_map, scanner_locations)

        print("good_map currently is of length: " + str(len(good_map)))
        print("unincorporated scanners: " + str(len(unincorporated)))
        
        if len(unincorporated) == 0:
            break
        
    print("Final unincorporated scanners: " + str(len(unincorporated)))

    print(scanner_locations)
    
    manhattan_distances = []
    
    for scanner1 in scanner_locations:
        for scanner2 in scanner_locations:
            manhattan_distances.append(compute_manhattan_distance(scanner1, scanner2))

    result = max(manhattan_distances)
    print("result: " + str(result))
    draw (good_map, colour_map, scanner_locations)

def compute_manhattan_distance(scanner1, scanner2):
    (x1,y1,z1) = scanner1
    (x2,y2,z2) = scanner2
    
    return abs(x1-x2) + abs(y1-y2) + abs(z1-z2)
if __name__ == "__main__":
    main()