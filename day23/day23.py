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

def amphi_cost(amphi):
    if amphi == "A":
        return 1
    if amphi == "B":
        return 10
    if amphi == "C":
        return 100
    if amphi == "D":
        return 1000

def find_all_valid_steps(start_state):
    end_states = []
    #for any in the hallway, can they move into their spot? (to the bottom, no point tracking the intermediate)
    
    #for any in the free row, can they move to the hallway? 
    #for any in the trapped row, can they move into the hallway (no point tracking the intermediate)
    
    #if the hallway is empty, we can move something out into it.
    if start_state.startswith("..........."):
        #if the A row is not complete
        if start_state[11] != 'A' and start_state[15] != 'A':
            #move the free one to all possible hallway states
            amphipod_to_move = start_state[11]
            end_state = start_state
            end_state[11] = "."
            
            for (step_cost, location) in [(3,0),(2,1),(2,3),(4,5),(6,7),(8,9),(9,10)]:
                new_end_state = end_state
                new_end_state[location] = amphipod_to_move
                cost = step_cost*amphi_cost(amphipod_to_move)
                end_states.append((cost, new_end_state))
                
        #if the B row is not complete
        if start_state[11] != 'B' and start_state[15] != 'B':
            #move the free one to all possible hallway states
            amphipod_to_move = start_state[12]
            end_state = start_state
            end_state[12] = "."
            
            for (step_cost, location) in [(5,0),(4,1),(2,3),(2,5),(4,7),(6,9),(7,10)]:
                new_end_state = end_state
                new_end_state[location] = amphipod_to_move
                cost = step_cost*amphi_cost(amphipod_to_move)
                end_states.append((cost, new_end_state))
                
        #if the C row is not complete
        if start_state[11] != 'C' and start_state[15] != 'C':
            #move the free one to all possible hallway states
            amphipod_to_move = start_state[12]
            end_state = start_state
            end_state[12] = "."
            
            for (step_cost, location) in [(7,0),(6,1),(4,3),(2,5),(2,7),(4,9),(5,10)]:
                new_end_state = end_state
                new_end_state[location] = amphipod_to_move
                cost = step_cost*amphi_cost(amphipod_to_move)
                end_states.append((cost, new_end_state))
        
        #if the D row is not complete
        if start_state[11] != 'D' and start_state[15] != 'D':
            #move the free one to all possible hallway states
            amphipod_to_move = start_state[12]
            end_state = start_state
            end_state[12] = "."
            
            for (step_cost, location) in [(9,0),(8,1),(6,3),(4,5),(2,7),(2,9),(3,10)]:
                new_end_state = end_state
                new_end_state[location] = amphipod_to_move
                cost = step_cost*amphi_cost(amphipod_to_move)
                end_states.append((cost, new_end_state))
        
    #if there's something in the hallway, we can still move something out
    
    #this should be some sort of graph instead of trying to do it by hand, where blocked off paths are removed nodes. 
    
    
    #also the nodes at 2,4,6,8 don't really exist, they just add +1n to the cost
    
    
        for index in [11,12,13,14]:
            amphipod_to_move = start_state[index]
            end_state[index] = "."
            for i in [0,1,3,5,7,9,10]:
                new_end_state = end_state
                new_end_state[i] = amphipod_to_move
                
            
            end_states.append((cost, new_state))
        
   
   
   
    end_states.append((cost, new_state))
    return end_states
    
def add_steps_to_graph(G, start_state):
    new_states = find_all_valid_steps(start_state) 
    
    for (cost, new_state) in new_states:
        G.add_edge(start_state, new_state, weight=cost)
        G = add_steps_to_graph(G, new_state)
    
    return G

def part1(): 
    #solved by hand for a silver star 
    print("PART 1:")
    lines = read_file()
   
    free_row = lines[2].replace("#", " ").split()
    trapped_row = lines[3].replace("#", " ").split()
    
    startstate = "..........." + "".join(free_row) + "".join(trapped_row)
    winstate = "...........ABCDABCD" 
    print (startstate)
    
    G = nx.DiGraph()
    
    G.add_node(startstate, label="start")
    G.add_node(winstate, label="end")
    
    G = add_steps_to_graph(G, startstate)
    shortest_path = nx.shortest_path(G, startstate, winstate, weight="weight")
    
    result = nx.path_weight(G, path, weight="weight")
    print("result: " + str(result))


def part2():
    print("PART 2:")
    lines = read_file()
   

    result = 0
    print("result: " + str(result))

    
if __name__ == "__main__":
    main()