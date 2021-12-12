import time
import numpy as np
from collections import Counter
import networkx as nx
import copy 
import itertools

part1paths = []

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

def part1(): 
    print("PART 1:")
    lines = read_file()
    copies = 100
    
    mygraph = nx.Graph()
    for line in lines:
        l = line.split('-')
        mygraph.add_edge(l[0], l[1])
            
    isLarge = {}
    isVisited = {}
    for node in mygraph.nodes:
        isLarge[node] = node.isupper()
        isVisited[node] = False
        
    nx.set_node_attributes(mygraph, isLarge, "isLarge")
    nx.set_node_attributes(mygraph, isVisited, "isVisited")
    
    # print(mygraph.nodes)
    print(mygraph.nodes(data=True))
    #simple_paths = nx.all_simple_paths(mygraph, "start", "end")
    startnode = "start"
    nx.set_node_attributes(mygraph, {startnode: {"isVisited":True}})
    find_paths(mygraph.copy(), startnode, [startnode])
    
    result = len(part1paths)
    print("result: " + str(result))

def find_paths(mygraph, startnode, current_path):
    for (_ ,newnode) in mygraph.edges(startnode): 
        copied_path = copy.deepcopy(current_path)
        copied_graph = mygraph.copy()
        
        if newnode == "end": 
            copied_path.append("end")
            part1paths.append(copied_path)
            continue
        elif nx.get_node_attributes(copied_graph, "isVisited")[newnode]:
            continue
        else: 
            if not nx.get_node_attributes(copied_graph, "isLarge")[newnode]:
                nx.set_node_attributes(copied_graph, {newnode: {"isVisited":True}})
            copied_path.append(newnode)
            find_paths(copied_graph.copy(), newnode, copy.deepcopy(copied_path))

part2paths = []

def find_paths_with_small(mygraph, startnode, current_path):
    #print(current_path)
    for (_ ,newnode) in mygraph.edges(startnode): 
        copied_path = copy.deepcopy(current_path)
        copied_graph = mygraph.copy()
        
        if newnode == "end": 
            copied_path.append("end")
            part2paths.append(copied_path)
            continue
        elif nx.get_node_attributes(copied_graph, "isVisited")[newnode] > 0:
            continue
        else: 
            if not nx.get_node_attributes(copied_graph, "isLarge")[newnode]:
                visits = nx.get_node_attributes(copied_graph, "isVisited")[newnode]
                nx.set_node_attributes(copied_graph, {newnode: {"isVisited": visits +1}})
            copied_path.append(newnode)
            find_paths_with_small(copied_graph.copy(), newnode, copy.deepcopy(copied_path))

def part2():
    print("PART 2:")
    lines = read_file()
    copies = 100
    
    mygraph = nx.Graph()
    for line in lines:
        l = line.split('-')
        mygraph.add_edge(l[0], l[1])
            
    isLarge = {}
    isVisited = {}
    for node in mygraph.nodes:
        isLarge[node] = node.isupper()
        isVisited[node] = 0
        
    nx.set_node_attributes(mygraph, isLarge, "isLarge")
    nx.set_node_attributes(mygraph, isVisited, "isVisited")
    
    small_caves = []
    for (node, data) in mygraph.nodes(data=True):
        if not data['isLarge'] and (node != "start") and (node != "end"):
            small_caves.append(node)
    
    print(small_caves)
    print(mygraph.nodes(data=True))

    startnode = "start"
    nx.set_node_attributes(mygraph, {startnode: {"isVisited":2}})
    
    for small_cave in small_caves: #treat each cave as the "special case" in turn
        mycopy = mygraph.copy()
        nx.set_node_attributes(mycopy, {small_cave: {"isVisited":-1}})
        find_paths_with_small(mycopy, startnode, [startnode])
    
    part2paths.sort()
    results = list(k for k,_ in itertools.groupby(part2paths)) #remove dupes
    
    # for path in results:
        # print(path)
    
    result = len(results)
    print("result: " + str(result))
    
if __name__ == "__main__":
    main()