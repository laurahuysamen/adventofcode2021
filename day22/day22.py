import time
import numpy as np
from collections import Counter
import itertools
from functools import reduce
import math
import uuid
import networkx as nx
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

def read_file(filename='input.txt'):
    with open(filename) as f:
        lines = f.readlines()
    lines = [str(l.strip()) for l in lines]
    return lines

def main():
    start = time.time()
    #part1()
    middle = time.time()
    part2()
    end = time.time()
    print("Part 1 Time:  " + str(middle-start))
    print("Part 2 Time:  " + str(end-middle))
    print("Total Time:   " + str(end-start))
    

def part1(): 
    print("PART 1:")
    lines = read_file()
    
    #grid is at least -50 to at most 50. 
    #lets shift that to 0 to 100 to make indexing easier
    instructions = []
    offset = 50
    
    for line in lines:
        splitline = line.replace(".", " ").replace(",", " ").replace("=", " ").split()
        state = 1 if splitline[0] == "on" else 0
        #print (splitline)
        xrange = [int(splitline[2])+offset, int(splitline[3])+offset]
        yrange = [int(splitline[5])+offset, int(splitline[6])+offset]
        zrange = [int(splitline[8])+offset, int(splitline[9])+offset]
        instructions.append((state, xrange, yrange, zrange))
    
    print (instructions)
    
    cubes = np.zeros((100,100,100), dtype="int8")
    
    for instruction in instructions:
        print (instruction)
        (state, xrange, yrange, zrange) = instruction
        if 0 > xrange[0] or xrange[0] > 100 or 0 > yrange[0] or yrange[0] > 100 or 0 > zrange[0] or zrange[0] > 100    \
        or 0 > xrange[1] or xrange[1] > 100 or 0 > yrange[1] or yrange[1] > 100 or 0 > zrange[1] or zrange[1] > 100:
            print (f"Skipping instruction {instruction}")
            continue
        
        cubes[xrange[0]:xrange[1]+1, yrange[0]:yrange[1]+1, zrange[0]:zrange[1]+1] = state

    result = np.count_nonzero(cubes)
    print("result: " + str(result))


def part2():
    print("PART 2:")
    lines = read_file()
    
    instructions = []
    
    for line in lines:
        splitline = line.replace(".", " ").replace(",", " ").replace("=", " ").split()
        state = 1 if splitline[0] == "on" else 0
        #print (splitline)
        xunsorted = [int(splitline[2]), int(splitline[3])]
        yunsorted = [int(splitline[5]), int(splitline[6])]
        zunsorted = [int(splitline[8]), int(splitline[9])]
        xrange = (min(xunsorted), max(xunsorted))
        yrange = (min(yunsorted), max(yunsorted))
        zrange = (min(zunsorted), max(zunsorted))
        instructions.append((state, xrange, yrange, zrange))
        #print (instructions)
             
    lit_cuboids = [instructions[0]]
    
    for instruction in instructions[1:]:
        #print(lit_cuboids)
        print(f"instruction: {instruction}")
        new_lit_cuboids = []
        if instruction_state == 1:
            new_lit_cuboids.append(instruction) 
            #append the new cuboid, since we will remove any overlaps in the next steps
        for lit_cuboid in lit_cuboids:
            if not is_overlapping(lit_cuboid, instruction):
                new_lit_cuboids.append(lit_cuboid)
            else:
                print (f"overlaps with {lit_cuboid}")
                #find the part of the cube that is *not* overlapped by the new cube and add that back to the new_lit_cuboids
                (state1, (x1min, x1max), (y1min, y1max), (z1min, z1max)) = lit_cuboid
                (state2, (x2min, x2max), (y2min, y2max), (z2min, z2max)) = instruction
                
                if state2 == 1: #lets just deal with lit cubes first
                    if  x2min >= x1min and x2max <= x1max \
                    and 
                    #case 1 - instruction(2) is entirely surrounded by lit_cuboid(1)
                        #remove instruction from new_lit_cuboids, add lit_cuboid and break (since nothing should overlap)
                        new_lit_cuboids.pop()
                        new_lit_cuboids.append(lit_cuboid)
                        break
                        
                        
                    #case 2 - lit_cuboid is entirely surrounded by instruction
                        #no need to worry, don't add lit_cuboid, continue
                    #case 3 - instruction is encased in x, y, greater z
                    #case 4 - instruction is encased in x, z, greater y
                    #case 6 - instruction is encased in x, y, smaller z
                    #case 7 - instruction is encased in x, z, smaller y
                    #case 5 - instruction is encased in y, z, greater x
                    #case 8 - instruction is encased in y, z, smaller x
                    
                    #case 9  - instruction is encased in x, greater y, greater z
                    #case 10 - instruction is encased in x, smaller y, greater z
                    #case 11 - instruction is encased in x, greater y, smaller z
                    #case 12 - instruction is encased in x, smaller y, smaller z
                    
                    #case 13 - instruction is encased in x, greater z, greater y
                    #case 14 - instruction is encased in x, smaller z, greater y
                    #case 15 - instruction is encased in x, greater z, smaller y
                    #case 16 - instruction is encased in x, smaller z, smaller y
                    
                    #case 17 - instruction is encased in y, greater z, greater x
                    #case 18 - instruction is encased in y, smaller z, greater x
                    #case 19 - instruction is encased in y, greater z, smaller x
                    #case 20 - instruction is encased in y, smaller z, smaller x
                    
                    #case 21 - instruction is in upper x, upper y, upper z corner
                    
                    #case 22 - instruction is in upper x, upper y, lower z corner
                    #case 23 - instruction is in upper x, lower y, upper z corner
                    #case 24 - instruction is in lower x, upper y, upper z corner
                    
                    #case 25 - instruction is in lower x, lower y, upper z corner
                    #case 26 - instruction is in lower x, upper y, lower z corner
                    #case 27 - instruction is in upper x, lower y, lower z corner
                    
                    #case 28 - instruction is in lower x, lower y, lower z corner
                    
                    
                    
                
                
                
                
                
                
                
        lit_cuboids = new_lit_cuboids
        
        #(instruction_state, instruction_x, instruction_y, instruction_z) = instruction
        #new_lit_cuboids = []
        #if instruction_state == 1:
        #    new_lit_cuboids.append(instruction) 
        #    #append the new cuboid, since we will remove any overlaps in the next steps
        #for lit_cuboid in lit_cuboids:
        #    #first find out if the new instruction overlaps at all, cause if not we can skip all this
        #    if not is_overlapping(lit_cuboid, instruction):
        #        new_lit_cuboids.append(lit_cuboid)
        #    else:
        #        #split existing lit_cuboid and only add back the parts that don't overlap. 
        #        (xs,ys,zs) = find_all_coordinate_pairs(lit_cuboid, instruction)
        #        allsubcuboids = []
        #        #there are 27 sub-cuboids which could be lit or unlit. 
        #        #generate all 27 of them
        #        for i in range(3):
        #            for j in range(3):
        #                for k in range(3):
        #                    subcuboid = (0, (xs[i] , xs[i+1]),(ys[j] , ys[j+1]),(zs[k] , zs[k+1]))
        #                    allsubcuboids.append(subcuboid)
        #        #print (f"Allsubcuboids: {allsubcuboids}")
        #        
        #        newsubcuboids = []
        #        for subcuboid in allsubcuboids: #light up the ones that should initially be lit:
        #            if is_overlapping(subcuboid, lit_cuboid):
        #                (_, x,y,z) = subcuboid
        #                newsubcuboids.append((1, x, y, z))
        #            else: 
        #                newsubcuboids.append(subcuboid)
        #        allsubcuboids = newsubcuboids
        #        
        #        newsubcuboids = []
        #        for subcuboid in allsubcuboids: #light up the ones that should now be lit:
        #            if is_overlapping(subcuboid, instruction):
        #                (_, x,y,z) = subcuboid
        #                newsubcuboids.append((instruction[0], x, y, z))
        #            else: 
        #                newsubcuboids.append(subcuboid)
        #        allsubcuboids = newsubcuboids
        #        
        #        #then, add the lit ones back:
        #        new_lit_cuboids.extend([s for s in allsubcuboids if s[0] == 1])
        #
        #lit_cuboids = new_lit_cuboids

    result = sum([get_instruction_size(c) for c in lit_cuboids])
    print("result: " + str(result))

def get_instruction_size(ins):
    (_, xrange, yrange, zrange) = ins
    return (xrange[1]+1-xrange[0]) * (yrange[1]+1-yrange[0]) * (zrange[1]+1-zrange[0])
    
def find_all_coordinate_pairs(ins1, ins2):
    (_, (x1min, x1max), (y1min, y1max), (z1min, z1max)) = ins1
    (_, (x2min, x2max), (y2min, y2max), (z2min, z2max)) = ins2
    xrange = (min(x1min, x2min), max(x1min, x2min), min(x1max, x2max), max(x1max, x2max))
    yrange = (min(y1min, y2min), max(y1min, y2min), min(y1max, y2max), max(y1max, y2max))
    zrange = (min(z1min, z2min), max(z1min, z2min), min(z1max, z2max), max(z1max, z2max))
    return (xrange, yrange, zrange)
    
def find_overlap_cuboid(ins1, ins2):
    (_, (x1min, x1max), (y1min, y1max), (z1min, z1max)) = ins1
    (_, (x2min, x2max), (y2min, y2max), (z2min, z2max)) = ins2
      
    xrange = (max(x1min, x2min), min(x1max, x2max))
    yrange = (max(y1min, y2min), min(y1max, y2max))
    zrange = (max(z1min, z2min), min(z1max, z2max))
    
    is_overlapped = (xrange[1] - xrange[0]) > 0 and (yrange[1] - yrange[0]) > 0 and (zrange[1] - zrange[0]) > 0
    
    return (is_overlapped, xrange, yrange, zrange)

def is_overlapping(ins1, ins2):
    (_, (x1min, x1max), (y1min, y1max), (z1min, z1max)) = ins1
    (_, (x2min, x2max), (y2min, y2max), (z2min, z2max)) = ins2
        
    xrange = (max(x1min, x2min), min(x1max, x2max))
    yrange = (max(y1min, y2min), min(y1max, y2max))
    zrange = (max(z1min, z2min), min(z1max, z2max))
    
    result = (xrange[1] - xrange[0]) >= 0 and (yrange[1] - yrange[0]) >= 0 and (zrange[1] - zrange[0]) >= 0
    #print(result)
    return result
    
if __name__ == "__main__":
    main()