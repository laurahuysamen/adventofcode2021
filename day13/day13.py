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
    
def do_fold(mygrid, fold_instruction):
    (direction, index) = fold_instruction
    (original_x, original_y) = mygrid.shape
    print (fold_instruction)
    #print("original shape : " + str(original_x) +" , "+str(original_y)) 
    
    if direction == 'y': ## numpy X
        #print("DIRECTION Y!")
        folded_grid = np.zeros((index, original_y))
        (folded_x,folded_y) = folded_grid.shape 
        #print("folded shape : " + str(folded_x) +" , "+str(folded_y)) 
                
        newgrid = np.zeros((index, original_y))
        for i in range(folded_x):
            for j in range(original_y):
                ix = index
                newi = i + 1
                newgrid[ix - newi, j] = mygrid[ix+newi, j]
                
        for i in range(folded_x):
            for j in range(folded_y-1):
                folded_grid[i,j] = mygrid[i, j] + newgrid[i,j]
                
    elif direction == 'x': ## numpy Y
        #print("DIRECTION X!")
        folded_grid = np.zeros((original_x, index))
        (folded_x,folded_y) = folded_grid.shape 
        #print("folded shape : " + str(folded_x) +" , "+str(folded_y)) 
        
        newgrid = np.zeros((original_x, index))
        for i in range(original_x):
            for j in range(folded_y):
                ix = index
                newj = j + 1
                newgrid[i, ix-newj] = mygrid[i, ix+newj]
        
        for i in range(folded_x):
            for j in range(folded_y):
                folded_grid[i,j] = mygrid[i,j] + newgrid[i,j]
                
    #print("COUNT: " + str(np.count_nonzero(folded_grid)))
    return folded_grid
    
def part1(): 
    print("PART 1:")
    lines = read_file()
    index = lines.index("")
    
    folds = lines[index+1:]
    dots = lines[0:index]
    
    mydots = [[int(l) for l in line.split(',')] for line in dots]
    myfolds = [fold.split()[2] for fold in folds]
    #print (mydots)
    #print (myfolds)
    
    max_x_coord = max([l[1] for l in mydots])  +2
    max_y_coord = max([l[0] for l in mydots])  +2
    
    #CAREFUL! you have transposed this
    mygrid = np.zeros((max_x_coord+1, max_y_coord+1))
    for dot in mydots:
        mygrid[dot[1], dot[0]] = 1

    #print(mygrid)
    #print(np.count_nonzero(mygrid))
    
    folded_grid = np.array(0)
    for fold in myfolds:
        fold_details = fold.split('=')
        folded_grid = do_fold(mygrid, (fold_details[0], int(fold_details[1])))
        break
    
    #print (folded_grid)
 
    result = np.count_nonzero(folded_grid)
    print("result: " + str(result))
    
def part2():
    print("PART 2:")
    lines = read_file()
    index = lines.index("")
    
    folds = lines[index+1:]
    dots = lines[0:index]
    
    mydots = [[int(l) for l in line.split(',')] for line in dots]
    myfolds = [fold.split()[2] for fold in folds]
    #print (mydots)
    #print (myfolds)
    
    max_x_coord = max([l[1] for l in mydots]) + 5
    max_y_coord = max([l[0] for l in mydots]) + 5
    
    #print(max_x_coord)
    #print(max_y_coord) 
    
    #CAREFUL! you have transposed this
    mygrid = np.zeros((max_x_coord+1, max_y_coord+1))
    for dot in mydots:
        mygrid[dot[1], dot[0]] = 1

    #print(mygrid)
    #print(np.count_nonzero(mygrid))
    
    folded_grid = mygrid.copy()
    for fold in myfolds:
        fold_details = fold.split('=')
        folded_grid = do_fold(folded_grid, (fold_details[0], int(fold_details[1])))
        
    #print (folded_grid)
 
    result = np.count_nonzero(folded_grid)
    #print("result: " + str(result))
    
    (x, y) = folded_grid.shape
    for i in range(x):
        mystring = ""
        for j in range(y):
            if folded_grid[i,j] > 0:
                mystring = mystring + ("█")
            else:
                mystring = mystring + (".")
        print(mystring)

    #ehhhhhhhhhhhhhh, close enough
    
if __name__ == "__main__":
    main()