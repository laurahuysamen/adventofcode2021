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
    
    #create graph of the start_state: 
    
    boardstate = nx.Graph()
    start = list(start_state)
    for i in range(len(start)):
        boardstate.add_node(i, occupancy=start[i]) 
        
    goals = {"A":[11,7], "B":[12,8], "C":[13,9], "D":[14,10]}
    
    #we can ignore the hallway spots outside of a goal because they can't stop there.
    boardstate.add_edge(0, 1, weight=1)
    boardstate.add_edge(1, 7, weight=2)
    boardstate.add_edge(1, 2, weight=2)
    boardstate.add_edge(7, 11, weight=1)
    boardstate.add_edge(7, 2, weight=2)
    boardstate.add_edge(2, 8, weight=2)
    boardstate.add_edge(2, 3, weight=2)
    boardstate.add_edge(8, 12, weight=1)
    boardstate.add_edge(8, 3, weight=2)
    boardstate.add_edge(3, 9, weight=2)
    boardstate.add_edge(3, 4, weight=2)
    boardstate.add_edge(9, 13, weight=1)
    boardstate.add_edge(9, 4, weight=2)
    boardstate.add_edge(4, 10, weight=2)
    boardstate.add_edge(4, 5, weight=2)
    boardstate.add_edge(10, 14, weight=1)
    boardstate.add_edge(10, 5, weight=2)
    boardstate.add_edge(5, 6, weight=1)
    
    #for any in the hallway, can they move into their goal?
    for i in range(7): 
        movingamphipod = boardstate.nodes[i]["occupancy"]
        if movingamphipod != ".":
            #we've found someone in the hallway, lets prune the graph and see if we can get where we want to go
                pruned_graph = boardstate.copy()
                for j in range(15): 
                    if j != i: #dont cut ourselves off! 
                        if pruned_graph.nodes[j]["occupancy"] != ".":
                            pruned_graph.remove_node(j)
                            
                #now we can see if it's possible to get to goals[movingamphipod].
                path = []
                goal1 = goals[movingamphipod][0]
                goal2 = goals[movingamphipod][1]
                #is it possible to get to the bottom, if so, do that.
                if goal1 in pruned_graph and nx.has_path(pruned_graph, i, goal1):
                    path = nx.shortest_path(pruned_graph, i, goal1, weight="weight")
                else:
                    #if not, is it VALID and possible to get to the top space?
                    if boardstate.nodes[goal1]["occupancy"] == movingamphipod: # can only move in if it's friend is there too
                        if goal2 in pruned_graph and nx.has_path(pruned_graph, i, goal2):
                            path = nx.shortest_path(pruned_graph, i, goal2, weight="weight")
                
                if len(path) != 0: 
                    #we've found a valid move! figure out it's cost and new state, and add it to the list
                    path_length = nx.path_weight(pruned_graph, path, weight="weight")
                    cost = path_length * amphi_cost(movingamphipod)
                    new_state = start.copy()
                    new_state[i] = "." #set the original spot empty
                    new_state[path[-1]] = movingamphipod #set the destination spot to have the amphipod
                    end_states.append((cost, "".join(new_state)))
    
    #for any in the free row or the trapped row, can they move to the hallway? 
    #we will ignore the scenario of going straight to the goal for simplicity since we don't need to track steps, they can go hallway, then home in two steps.
    for i in range(7, 15): 
        #print (f"checking {i}")
        movingamphipod = boardstate.nodes[i]["occupancy"]
        if movingamphipod != ".":
        #we've found someone we can move, lets prune the graph and see where we can go
            pruned_graph = boardstate.copy()
            for j in range(15): 
                if j != i: #dont cut ourselves off! 
                    if pruned_graph.nodes[j]["occupancy"] != ".":
                        pruned_graph.remove_node(j)
            #now we can see where we can go?
            paths = []
            #print (pruned_graph)
            
            for n in range(7): 
                if n in pruned_graph and nx.has_path(pruned_graph, i, n):
                    paths.append(nx.shortest_path(pruned_graph, i, n, weight="weight"))
            for path in paths:
                #we've found valid moves! figure out cost and new state, and add it to the list
                path_length = nx.path_weight(pruned_graph, path, weight="weight")
                cost = path_length * amphi_cost(movingamphipod)
                new_state = start.copy()
                new_state[i] = "." #set the original spot empty
                new_state[path[-1]] = movingamphipod #set the destination spot to have the amphipod
                end_states.append((cost, "".join(new_state)))

    return end_states
    
def add_steps_to_graph(G, start_state):
    new_states = find_all_valid_steps(start_state) 
    states_to_return = []
    for (cost, new_state) in new_states:
        #print(new_state)
        if new_state not in G:
            states_to_return.append(new_state)
        if not G.has_edge(start_state, new_state):
            G.add_edge(start_state, new_state, weight=cost)
    return (G, states_to_return)

def part1():
    print("PART 1:")
    lines = read_file()
   
    free_row = lines[2].replace("#", " ").split()
    trapped_row = lines[3].replace("#", " ").split()
    
    startstate = "......." + "".join(free_row) + "".join(trapped_row)
    winstate = ".......ABCDABCD" 
    print (startstate)
    
    G = nx.DiGraph()
    
    G.add_node(startstate, label="start")
    G.add_node(winstate, label="end")
    
    states_to_process = [startstate]
    while len(states_to_process) > 0:
        new_states_to_process = []
        
        print (len(states_to_process))
        for state in states_to_process:
            (G, new_states) = add_steps_to_graph(G, state)
            new_states_to_process.extend(new_states)
        states_to_process = list(set(new_states_to_process)) #remove dupes

    if nx.has_path(G, startstate, winstate):
        shortest_path = nx.shortest_path(G, startstate, winstate, weight="weight")
        print(shortest_path)
        result = nx.path_weight(G, shortest_path, weight="weight")
        print("result: " + str(result))

def find_all_valid_steps_2(start_state):
    end_states = []
    
    #create graph of the start_state: 
    
    boardstate = nx.Graph()
    start = list(start_state)
    for i in range(len(start)):
        boardstate.add_node(i, occupancy=start[i]) 
        
    goals = {"A":[19,15,11,7], "B":[20,16,12,8], "C":[21,17,13,9], "D":[22,18,14,10]}
    
    #we can ignore the hallway spots outside of a goal because they can't stop there.
    boardstate.add_edge(0, 1, weight=1)
    boardstate.add_edge(1, 7, weight=2)
    boardstate.add_edge(1, 2, weight=2)
    boardstate.add_edge(7, 11, weight=1)
    boardstate.add_edge(11, 15, weight=1)
    boardstate.add_edge(15, 19, weight=1)
    boardstate.add_edge(7, 2, weight=2)
    boardstate.add_edge(2, 8, weight=2)
    boardstate.add_edge(2, 3, weight=2)
    boardstate.add_edge(8, 12, weight=1)
    boardstate.add_edge(12, 16, weight=1)
    boardstate.add_edge(16, 20, weight=1)
    boardstate.add_edge(8, 3, weight=2)
    boardstate.add_edge(3, 9, weight=2)
    boardstate.add_edge(3, 4, weight=2)
    boardstate.add_edge(9, 13, weight=1)
    boardstate.add_edge(13, 17, weight=1)
    boardstate.add_edge(17, 21, weight=1)
    boardstate.add_edge(9, 4, weight=2)
    boardstate.add_edge(4, 10, weight=2)
    boardstate.add_edge(4, 5, weight=2)
    boardstate.add_edge(10, 14, weight=1)
    boardstate.add_edge(14, 18, weight=1)
    boardstate.add_edge(18, 22, weight=1)
    boardstate.add_edge(10, 5, weight=2)
    boardstate.add_edge(5, 6, weight=1)
    
    #for any in the hallway, can they move into their goal?
    for i in range(7):
        movingamphipod = boardstate.nodes[i]["occupancy"]
        if movingamphipod != ".":
            #we've found someone in the hallway, lets prune the graph and see if we can get where we want to go
                pruned_graph = boardstate.copy()
                for j in range(23): 
                    if j != i: #dont cut ourselves off! 
                        if pruned_graph.nodes[j]["occupancy"] != ".":
                            pruned_graph.remove_node(j)
                            
                #now we can see if it's possible to get to goals[movingamphipod].
                path = []
                goal1 = goals[movingamphipod][0]
                goal2 = goals[movingamphipod][1]
                goal3 = goals[movingamphipod][2]
                goal4 = goals[movingamphipod][3]
                #is it possible to get to the bottom, if so, do that.
                if goal1 in pruned_graph and nx.has_path(pruned_graph, i, goal1):
                    path = nx.shortest_path(pruned_graph, i, goal1, weight="weight")
                else:
                    #if not, is it VALID and possible to get to the 3rd space?
                    if boardstate.nodes[goal1]["occupancy"] == movingamphipod: # can only move in if it's friend is there too
                        if goal2 in pruned_graph and nx.has_path(pruned_graph, i, goal2):
                            path = nx.shortest_path(pruned_graph, i, goal2, weight="weight")
                        else:
                            #if not, is it VALID and possible to get to the 2nd space?
                            if boardstate.nodes[goal2]["occupancy"] == movingamphipod: # can only move in if it's friend is there too
                                if goal3 in pruned_graph and nx.has_path(pruned_graph, i, goal3):
                                    path = nx.shortest_path(pruned_graph, i, goal3, weight="weight")
                                else:
                                    #if not, is it VALID and possible to get to the 1st space?
                                    if boardstate.nodes[goal3]["occupancy"] == movingamphipod: # can only move in if it's friend is there too
                                        if goal4 in pruned_graph and nx.has_path(pruned_graph, i, goal4):
                                            path = nx.shortest_path(pruned_graph, i, goal4, weight="weight")
                            
                
                if len(path) != 0: 
                    #we've found a valid move! figure out it's cost and new state, and add it to the list
                    path_length = nx.path_weight(pruned_graph, path, weight="weight")
                    cost = path_length * amphi_cost(movingamphipod)
                    new_state = start.copy()
                    new_state[i] = "." #set the original spot empty
                    new_state[path[-1]] = movingamphipod #set the destination spot to have the amphipod
                    end_states.append((cost, "".join(new_state)))
    
    #for any in the free row or the trapped row, can they move to the hallway? 
    #we will ignore the scenario of going straight to the goal for simplicity since we don't need to track steps, they can go hallway, then home in two steps.
    for i in range(7, 23):
        #print (f"checking {i}")
        movingamphipod = boardstate.nodes[i]["occupancy"]
        if movingamphipod != ".":
        #we've found someone we can move, lets prune the graph and see where we can go
            pruned_graph = boardstate.copy()
            for j in range(23): ##TODO
                if j != i: #dont cut ourselves off! 
                    if pruned_graph.nodes[j]["occupancy"] != ".":
                        pruned_graph.remove_node(j)
            #now we can see where we can go?
            paths = []
            #print (pruned_graph)
            
            for n in range(7): 
                if n in pruned_graph and nx.has_path(pruned_graph, i, n):
                    paths.append(nx.shortest_path(pruned_graph, i, n, weight="weight"))
            for path in paths:
                #we've found valid moves! figure out cost and new state, and add it to the list
                path_length = nx.path_weight(pruned_graph, path, weight="weight")
                cost = path_length * amphi_cost(movingamphipod)
                new_state = start.copy()
                new_state[i] = "." #set the original spot empty
                new_state[path[-1]] = movingamphipod #set the destination spot to have the amphipod
                end_states.append((cost, "".join(new_state)))

    return end_states
    
def add_steps_to_graph_2(G, start_state):
    new_states = find_all_valid_steps_2(start_state) 
    states_to_return = []
    for (cost, new_state) in new_states:
        #print(new_state)
        if new_state not in G:
            states_to_return.append(new_state)
        if not G.has_edge(start_state, new_state):
            G.add_edge(start_state, new_state, weight=cost)
    return (G, states_to_return)

def part2():
    print("PART 2:")
    lines = read_file()
   
    free_row = lines[2].replace("#", " ").split()
    trapped_row = lines[3].replace("#", " ").split()
    
    startstate = "......." + "".join(free_row) + "DCBADBAC" + "".join(trapped_row)
    winstate = ".......ABCDABCDABCDABCD" 
    print (startstate)
    
    G = nx.DiGraph()
    
    G.add_node(startstate, label="start")
    G.add_node(winstate, label="end")
    
    states_to_process = [startstate]
    while len(states_to_process) > 0:
        new_states_to_process = []
        
        print (len(states_to_process))
        for state in states_to_process:
            (G, new_states) = add_steps_to_graph_2(G, state)
            new_states_to_process.extend(new_states)
        states_to_process = list(set(new_states_to_process)) #remove dupes

    if nx.has_path(G, startstate, winstate):
        shortest_path = nx.shortest_path(G, startstate, winstate, weight="weight")
        print(shortest_path)
        result = nx.path_weight(G, shortest_path, weight="weight")
        print("result: " + str(result))

    
if __name__ == "__main__":
    main()