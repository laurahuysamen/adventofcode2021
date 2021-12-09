import time
import numpy as np
from collections import Counter

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

def find_local_minima(grid): 
    local_minima = []
    num_rows, num_cols = grid.shape
    for x in range(0, num_rows-1):
        for y in range(0, num_cols-1):
            if grid[x,y] < grid[x, y+1] and grid[x,y] < grid[x, y-1] and grid[x,y] < grid[x+1, y] and grid[x,y] < grid[x-1, y]:
                local_minima.append(grid[x,y])
    return local_minima

def get_basins(grid):
    candidatenames = [int(i) for i in range(-20000, 0)]
    basins = np.copy(grid)
    num_rows, num_cols = grid.shape
    print(num_rows)
    print(num_cols)
    basin_names = []
    for x in range(0, num_rows-1):
        for y in range(0, num_cols-1):
            #print(basins[x,y])
            if basins[x,y] == 9:
                continue
            else:
                if basins[x-1, y] in basin_names: 
                    basins[x,y] = basins[x-1, y] 
                elif basins[x, y-1] in basin_names:
                    basins[x,y] = basins[x, y-1]
                else: #we have a new basin  
                    new_basin_name = candidatenames.pop()
                    basin_names.append(new_basin_name)
                    basins[x,y] = new_basin_name

                    
    #merge basins
    for x in range(0, num_rows-1):
        for y in range(0, num_cols-1):
            #print(basins[x,y])
            if basins[x,y] == 9:
                continue
            else:
                if basins[x, y+1] != 9 and (basins[x,y] != basins[x, y+1]):
                    basins[basins==basins[x,y]] = basins[x,y+1]
                if basins[x, y-1] != 9 and (basins[x,y] != basins[x, y-1]):
                    basins[basins==basins[x,y]] = basins[x,y-1]
                if basins[x+1, y] != 9 and (basins[x,y] != basins[x+1, y]):
                    basins[basins==basins[x,y]] = basins[x+1,y]
                if basins[x-1, y] != 9 and (basins[x,y] != basins[x-1, y]):
                    basins[basins==basins[x,y]] = basins[x-1,y]
    return basins

def part1(): 
    print("PART 1:")
    lines = read_file()
    gridlines = [[int(l) for l in list(line)] for line in lines]
    
    mygrid = np.array(gridlines)
    padded_grid = np.pad(mygrid, (1, 1), mode='constant',constant_values=9)
    
    local_minima = find_local_minima(padded_grid)
    print (padded_grid)
    print(local_minima)
    
    result = sum([l+1 for l in local_minima])
    print("result: " + str(result))

def part2():
    print("PART 2:")
    lines = read_file()
    gridlines = [[int(l) for l in list(line)] for line in lines]
    
    mygrid = np.array(gridlines)
    padded_grid = np.pad(mygrid, (1, 1), mode='constant',constant_values=9)
    
    basins = get_basins(padded_grid)
    
    occurances = Counter(np.reshape(basins, -1))
    occurances[9] = 0 #dont care about 9s.
    
    print (padded_grid)
    print (basins)
    print (occurances)
    
    largest_basin_sizes = [val for (_, val) in occurances.most_common(3)]
    print(largest_basin_sizes)

    result = largest_basin_sizes[0] * largest_basin_sizes[1] * largest_basin_sizes[2]
    print("result: " + str(result))

if __name__ == "__main__":
    main()