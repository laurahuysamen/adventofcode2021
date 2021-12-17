import time
import numpy as np
from collections import Counter
from functools import reduce
import re

def read_file():
    with open('input.txt') as f:
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
    
def is_on_target(x_range, y_range, coord):
    (x,y) = coord
    return x >= x_range[0] and x <= x_range[1] and y >= y_range[0] and y <= y_range[1]

def is_out_of_range(x_range, y_range, coord):
    (x,y) = coord
    return x > x_range[1] or y < y_range[0]
    
def run_step(velocity, coord, highestpoint):
    (x,y) = coord
    (vx, vy) = velocity
    
    coord = (x+vx, y+vy)
    
    if y+vy > highestpoint:
        highestpoint = y+vy
        
    if vx < 0:
        vx = vx + 1
    elif vx > 0: 
        vx = vx - 1
    velocity = (vx, vy-1)
    return (velocity, coord, highestpoint)
    
def part1(): 
    print("PART 1:")
    lines = read_file()[0].split()
    x_range = [int(i) for i in lines[2].split('=')[1].strip(",").split('..')]
    y_range = [int(i) for i in lines[3].split('=')[1].strip(",").split('..')]
    print (x_range)
    print (y_range)
    
    max_x = x_range[1]
    max_y = y_range[1]
    min_x = x_range[0]
    min_y = y_range[0]
    
    successful_velocities = []
    
    for x in range(0,max_x+1): #no point doing greater than max_x 
        for y in range(min_y,-min_y): #negative of the min is *likely* enough possible range
            startingvelocity = (x,y)
            velocity = (x,y)
            coord = (0,0)
            highestpoint = 0
            
            while True:
                (velocity, coord, highestpoint) = run_step(velocity, coord, highestpoint)
                if is_on_target(x_range, y_range, coord):
                    successful_velocities.append((startingvelocity, highestpoint))
                    break;
                elif is_out_of_range(x_range, y_range, coord): 
                    break;
                    
    print (successful_velocities)
    
    max_highestpoint = successful_velocities[0][1]
    value_with_max_y = successful_velocities[0]
    for i in range(len(successful_velocities)):
        (coord, highestpoint) = successful_velocities[i]
        if highestpoint > max_highestpoint:
            value_with_max_y = coord
            max_highestpoint = highestpoint
         
    print(value_with_max_y)
    result = max_highestpoint
    print("result: " + str(result))
    
def part2():
    print("PART 2:")
    lines = read_file()[0].split()
    x_range = [int(i) for i in lines[2].split('=')[1].strip(",").split('..')]
    y_range = [int(i) for i in lines[3].split('=')[1].strip(",").split('..')]
    print (x_range)
    print (y_range)
    
    max_x = x_range[1]
    max_y = y_range[1]
    min_x = x_range[0]
    min_y = y_range[0]
    
    successful_velocities = []
    
    for x in range(0,max_x+1): #no point doing greater than max_x 
        for y in range(min_y,-min_y): #negative of the min is *likely* enough possible range
            startingvelocity = (x,y)
            velocity = (x,y)
            coord = (0,0)
            highestpoint = 0
            
            while True:
                (velocity, coord, highestpoint) = run_step(velocity, coord, highestpoint)
                if is_on_target(x_range, y_range, coord):
                    successful_velocities.append((startingvelocity, highestpoint))
                    break;
                elif is_out_of_range(x_range, y_range, coord): 
                    break;
                    
    print (successful_velocities)
    
    result = len(successful_velocities)
    print("result: " + str(result))
  
if __name__ == "__main__":
    main()