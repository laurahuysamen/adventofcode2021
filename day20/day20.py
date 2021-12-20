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
    start = time.time()
    part1()
    middle = time.time()
    part2()
    end = time.time()
    print("Part 1 Time:  " + str(middle-start))
    print("Part 2 Time:  " + str(end-middle))
    print("Total Time:   " + str(end-start))
    
def binstr_as_int(number):
    return int("0b"+ number, 0)
    
def part1(): 
    print("PART 1:")
    lines = read_file()
    image_processing = [1 if l == "#" else 0 for l in list(lines[0])]
    #print (image_processing)
    
    grid = []
    for line in lines[2:]:
        grid.append([1 if l == "#" else 0 for l in list(line)])
    image = np.array(grid, dtype="int8")
    
    iterations = 2
    image = np.pad(image, (3*iterations, 3*iterations), mode='constant',constant_values=0)
    
    for i in range(iterations):
        print (i)
        draw_to_file(image, "part1_" + str(i) + ".png")
        num_rows, num_cols = image.shape 
        
        #what does the rest of the infinite grid look like? 
        constant = find_constant_to_surround(image, image_processing)
        #print("constant: " + str(constant))
        newimage = np.ones(image.shape, dtype="int8") if constant == 1 else np.zeros(image.shape, dtype="int8")
       
       #run image processing
        for x in range(1, num_rows -1):
            for y in range(1, num_cols -1):
                instruction = [image[x-1, y-1], image[x-1,y], image[x-1, y+1],
                               image[x, y-1], image[x,y], image[x,y+1],
                               image[x+1, y-1], image[x+1, y], image [x+1, y+1]]
                image_instruction = "".join([str(ins) for ins in instruction])
                instruction_index = binstr_as_int(image_instruction)
            
                image_processing_instruction = image_processing[instruction_index]
                newimage[x,y] = image_processing_instruction
        image = newimage
    
    
    draw_to_file(image, "part1_" +str(iterations) + ".png")
    result = np.count_nonzero(image)
    print("result: " + str(result))
    
def find_constant_to_surround(image, image_processing):
    if image[0,0] == 0:
        if image_processing[0] == 0:
            constant = 0
        else:
            constant = 1
    else:
        if image_processing[-1] == 0:
            constant = 0
        else:
            constant = 1
    return constant
    
def draw(nparray):
    fig = plt.figure()
    plt.imshow(nparray)
    plt.show()
    
def draw_to_file(nparray, name):
    fig = plt.figure()
    plt.imshow(nparray)
    plt.savefig(name)
    plt.close(fig)
    
def part2():
    print("PART 2:")
    lines = read_file()
    image_processing = [1 if l == "#" else 0 for l in list(lines[0])]
    #print (image_processing)
    
    grid = []
    for line in lines[2:]:
        grid.append([1 if l == "#" else 0 for l in list(line)])
    image = np.array(grid, dtype="int8")
    
    iterations = 50
    image = np.pad(image, (3*iterations, 3*iterations), mode='constant',constant_values=0)
    
    for i in range(iterations):
        print (i)
        draw_to_file(image, "part2_" +str(i) + ".png")
        num_rows, num_cols = image.shape 
        
        #what does the rest of the infinite grid look like? 
        constant = find_constant_to_surround(image, image_processing)
        #print("constant: " + str(constant))
        newimage = np.ones(image.shape, dtype="int8") if constant == 1 else np.zeros(image.shape, dtype="int8")
       
       #run image processing
        for x in range(1, num_rows -1):
            for y in range(1, num_cols -1):
                instruction = [image[x-1, y-1], image[x-1,y], image[x-1, y+1],
                               image[x, y-1], image[x,y], image[x,y+1],
                               image[x+1, y-1], image[x+1, y], image [x+1, y+1]]
                image_instruction = "".join([str(ins) for ins in instruction])
                instruction_index = binstr_as_int(image_instruction)
            
                image_processing_instruction = image_processing[instruction_index]
                newimage[x,y] = image_processing_instruction
        image = newimage
    
    
    draw_to_file(image, "part2_" + str(iterations) + ".png")
    result = np.count_nonzero(image)
    print("result: " + str(result))

if __name__ == "__main__":
    main()