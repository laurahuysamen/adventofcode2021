from collections import namedtuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
Point = namedtuple('Point', 'x y')
Line = namedtuple('Line', 'start end')

def read_file():
    with open('input.txt') as f:
        lines = f.readlines()
    lines = [str(l.strip()) for l in lines]
    return lines

def main():
    part1()
    part2()

def getline(line):
    lineResult = []
    if line.start.x == line.end.x:
        miny = min(line.start.y, line.end.y)
        maxy = max(line.start.y, line.end.y)
        for newy in range(miny, maxy+1):
            lineResult.append(Point(line.start.x, newy))
    elif line.start.y == line.end.y:
        minx = min(line.start.x, line.end.x)
        maxx = max(line.start.x, line.end.x)
        for newx in range(minx, maxx+1):
            lineResult.append(Point(newx, line.start.y))
    return lineResult
    
def getline_withdiagonals(line):
    lineResult = []
    if line.start.x == line.end.x:
        miny = min(line.start.y, line.end.y)
        maxy = max(line.start.y, line.end.y)
        for newy in range(miny, maxy+1):
            lineResult.append(Point(line.start.x, newy))
    elif line.start.y == line.end.y:
        minx = min(line.start.x, line.end.x)
        maxx = max(line.start.x, line.end.x)
        for newx in range(minx, maxx+1):
            lineResult.append(Point(newx, line.start.y))
    else:
        if (line.start.y < line.end.y): 
            if (line.start.x < line.end.x): 
                for i in range((line.end.y - line.start.y) + 1):
                    lineResult.append(Point(line.start.x + i, line.start.y + i))
            else: 
                for i in range((line.end.y - line.start.y) +1):
                    lineResult.append(Point(line.start.x - i, line.start.y + i))
        else:
            if (line.start.x < line.end.x): 
                for i in range((line.start.y - line.end.y) + 1):
                    lineResult.append(Point(line.start.x + i, line.start.y - i))
            else:
                for i in range((line.start.y - line.end.y) +1):
                    lineResult.append(Point(line.start.x - i, line.start.y - i))
    return lineResult

def part1(): 
    print("PART 1:")
    lines = read_file()
        
    newlist = []
    for line in lines: 
        ls = line.split()
        from_array = ls[0].split(",")
        to_array = ls[2].split(",")
        start_point = Point(int(from_array[0]), int(from_array[1]))
        end_point = Point(int(to_array[0]), int(to_array[1]))
        newline = Line(start_point, end_point)
        newlist.append (newline)
        
    #find the size of the grid
    xvalues = [l.start.x for l in newlist] + [l.end.x for l in newlist]
    yvalues = [l.start.y for l in newlist] + [l.end.y for l in newlist]
    
    maxx = int(max(xvalues))+1
    maxy = int(max(yvalues))+1
    
    grid = pd.DataFrame(np.zeros((maxx, maxy)), dtype=int)
    for item in newlist:
        plotline = getline(item)
        for (x, y) in plotline:
                grid.at[x,y] = grid.at[x,y] + 1
     
    print (grid.transpose())
    mysum = 0
    
    for row in grid.axes[0]:
      for column in grid.axes[1]:
          value = grid.at[row,column]
          if value > 1:
              mysum = mysum + 1;
                
    result = mysum
    print("result: " + str(result))

def part2():
    print("PART 2:")
    lines = read_file()
        
    newlist = []
    for line in lines: 
        ls = line.split()
        from_array = ls[0].split(",")
        to_array = ls[2].split(",")
        start_point = Point(int(from_array[0]), int(from_array[1]))
        end_point = Point(int(to_array[0]), int(to_array[1]))
        newline = Line(start_point, end_point)
        newlist.append (newline)
        
    #find the size of the grid
    xvalues = [l.start.x for l in newlist] + [l.end.x for l in newlist]
    yvalues = [l.start.y for l in newlist] + [l.end.y for l in newlist]
    
    maxx = int(max(xvalues))+1
    maxy = int(max(yvalues))+1
    
    grid = pd.DataFrame(np.zeros((maxx, maxy)), dtype=int)
    
    for item in newlist:
        plotline = getline_withdiagonals(item)
        for (x, y) in plotline:
            if x < maxx and y < maxy:
                grid.at[x,y] = grid.at[x,y] + 1
     
    print (grid.transpose())
    mysum = 0
    
    for row in grid.axes[0]:
      for column in grid.axes[1]:
          value = grid.at[row,column]
          if value > 1:
              mysum = mysum + 1;
                
    result = mysum
    print("result: " + str(result))
    
if __name__ == "__main__":
    main()