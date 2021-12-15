import time
import numpy as np
from collections import Counter
import networkx as nx

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
    
def nodename(i, j):
    return str(i) + ", " + str(j)
    
def part1(): 
    print("PART 1:")
    lines = read_file()
    
    G = nx.Graph()
    
    grid = []
    for line in lines:
        grid.append(list(line))
    def weight_func(u, v, d):
        node_v_wt = G.nodes[v].get("node_weight", 1)
        return node_v_wt
    for i in range(len(grid)):
        for j in range(len(grid[0])): 
            G.add_node(nodename(i,j), node_weight=int(grid[i][j]))
            if i != 0:
                G.add_edge(nodename(i,j), nodename(i-1, j))
            if j != 0:
                G.add_edge(nodename(i,j), nodename(i, j-1))
    
    print (G)
    
    start = nodename(0,0)
    end = nodename(len(grid)-1, len(grid[0])-1)
    
    shortest_path = nx.dijkstra_path(G, start, end, weight_func)
    
    print(shortest_path)
    
    total_weight = - int(grid[0][0]) #don't count the first one
    
    for node in shortest_path:
        weight = G.nodes[node].get("node_weight", 1)
        total_weight += weight
    
    result = total_weight
    print("result: " + str(result))

    
def part2():
    print("PART 2:")
    lines = read_file()
    
    G = nx.Graph()
    
    grid = []
    
    #expand the grid horizontally 5 times , increasing
    horizontal_grid =[]
    for line in lines:
        expanded_list = []
        for i in range(5):
            expanded_list.extend([(int(l)+i-9 if int(l)+i > 9 else int(l)+i) for l in list(line)])
        horizontal_grid.append(expanded_list)
    
    print (horizontal_grid)
    
    #expand the grid vertically 5 times, increasing
    for j in range(5):
        for line in horizontal_grid:
            newline = [(int(l)+j-9 if int(l)+j > 9 else int(l)+j) for l in list(line)]
            grid.append(newline)
        
    print (grid)
    def weight_func(u, v, d):
        node_v_wt = G.nodes[v].get("node_weight", 1)
        return node_v_wt
    for i in range(len(grid)):
        for j in range(len(grid[0])): 
            G.add_node(nodename(i,j), node_weight=int(grid[i][j]))
            if i != 0:
                G.add_edge(nodename(i,j), nodename(i-1, j))
            if j != 0:
                G.add_edge(nodename(i,j), nodename(i, j-1))
    
    print (G)
    
    start = nodename(0,0)
    end = nodename(len(grid)-1, len(grid[0])-1)
    
    shortest_path = nx.dijkstra_path(G, start, end, weight_func)
    
    print(shortest_path)
    
    total_weight = - int(grid[0][0]) #don't count the first one
    
    for node in shortest_path:
        weight = G.nodes[node].get("node_weight", 1)
        total_weight += weight
    
    result = total_weight
    print("result: " + str(result))

    
if __name__ == "__main__":
    main()