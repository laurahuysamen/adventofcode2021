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
    part1()
    middle = time.time()
    part2()
    end = time.time()
    print("Part 1 Time:  " + str(middle-start))
    print("Part 2 Time:  " + str(end-middle))
    print("Total Time:   " + str(end-start))

def run_step(seafloor):
    (x_size, y_size) = seafloor.shape
        
    #move south herd
    locs = np.where(seafloor == ">")
    coords = list(zip(locs[0], locs[1]))
    
    newseafloor = np.copy(seafloor)
    
    for (x,y) in coords:
        if seafloor[x,(y+1)%y_size] == ".":
            #the space next to us is open, so we can move, leaving empty behind us
            newseafloor[x,y] = "."
            newseafloor[x,(y+1)%y_size] = ">"
            
    seafloor = newseafloor 
    
    #move east herd
    locs = np.where(seafloor == "v")
    coords = list(zip(locs[0], locs[1]))
    
    newseafloor = np.copy(seafloor)
    
    for (x,y) in coords:
        if seafloor[(x+1)%x_size,y] == ".":
            #the space next to us is open, so we can move, leaving empty behind us
            newseafloor[x,y] = "."
            newseafloor[(x+1)%x_size,y] = "v"
            
    seafloor = newseafloor
    
    return seafloor


def part1(): 
    print("PART 1:")
    lines = read_file()
    
    input = [list(line) for line in lines]
    seafloor = np.array(input)
    
    counter = 1
    while True: 
        #print (seafloor)
        newseafloor = run_step(seafloor)
        if np.array_equal(newseafloor, seafloor): 
            #running another step hasn't changed anything
            break
        else:
            seafloor = newseafloor
            counter += 1
    
    
    result = counter
    print("result: " + str(result))
        
def part2():
    print("PART 2:")
    lines = read_file()
   

    result = 0
    print("result: " + str(result))

    
if __name__ == "__main__":
    main()