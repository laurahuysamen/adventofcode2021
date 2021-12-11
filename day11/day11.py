import time
import numpy as np
from collections import Counter

def read_file():
    with open('babyinput.txt') as f:
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

def part1(): 
    print("PART 1:")
    lines = read_file()
    mygridlines = [[int(l) for l in list(line)] for line in lines]
    
    mygrid = np.array(mygridlines)
    mygrid = np.pad(mygrid, (1, 1), mode='constant',constant_values=-2000000)
    
    flashes = 0
    
    for step in range(100):
        mygrid = mygrid + 1
        num_rows, num_cols = mygrid.shape 
        
        while np.count_nonzero(mygrid > 9):
            for x in range(1, num_rows-1):
                for y in range(1, num_cols-1):
                    if mygrid[x,y] > 9:
                        #flash, and update those around!
                        flashes += 1
                        mygrid[x-1,y-1]  = mygrid[x-1,y-1]  +1
                        mygrid[x, y-1]   = mygrid[x, y-1]   +1
                        mygrid[x+1, y-1] = mygrid[x+1, y-1] +1
                        mygrid[x-1, y]   = mygrid[x-1, y]   +1
                        mygrid[x+1, y]   = mygrid[x+1, y]   +1
                        mygrid[x-1,y+1]  = mygrid[x-1,y+1]  +1
                        mygrid[x, y+1]   = mygrid[x, y+1]   +1
                        mygrid[x+1, y+1] = mygrid[x+1, y+1] +1
                        mygrid[x,y] = -1000 #do not flash this one again!
        
        #reset those that flashed
        for x in range(1, num_rows-1):
            for y in range(1, num_cols-1):
                if mygrid[x,y] < 0 and mygrid[x,y] > -2000:
                    mygrid[x,y] = 0
    
    result = flashes
    print("result: " + str(result))

def part2():
    print("PART 2:")
    lines = read_file()
    mygridlines = [[int(l) for l in list(line)] for line in lines]
    
    mygrid = np.array(mygridlines)
    mygrid = np.pad(mygrid, (1, 1), mode='constant',constant_values=-2000000)
    
    flashes = 0
    result = 0
    
    for step in range(10000):
        mygrid = mygrid + 1
        num_rows, num_cols = mygrid.shape 
        while np.count_nonzero(mygrid > 9):
            for x in range(1, num_rows-1):
                for y in range(1, num_cols-1):
                    if mygrid[x,y] > 9:
                        #flash, and update those around!
                        flashes += 1
                        mygrid[x-1,y-1]  = mygrid[x-1,y-1]  +1
                        mygrid[x, y-1]   = mygrid[x, y-1]   +1
                        mygrid[x+1, y-1] = mygrid[x+1, y-1] +1
                        mygrid[x-1, y]   = mygrid[x-1, y]   +1
                        mygrid[x+1, y]   = mygrid[x+1, y]   +1
                        mygrid[x-1,y+1]  = mygrid[x-1,y+1]  +1
                        mygrid[x, y+1]   = mygrid[x, y+1]   +1
                        mygrid[x+1, y+1] = mygrid[x+1, y+1] +1
                        mygrid[x,y] = -1000 #do not flash this one again!
        
        #reset those that flashed
        for x in range(1, num_rows-1):
            for y in range(1, num_cols-1):
                if mygrid[x,y] < 0 and mygrid[x,y] > -2000:
                    mygrid[x,y] = 0
                    
        if np.count_nonzero(mygrid == 0) == 100:
            result = step + 1
            break
            
    print("result: " + str(result))
    
if __name__ == "__main__":
    main()