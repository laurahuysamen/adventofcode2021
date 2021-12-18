import time
import numpy as np
from collections import Counter
import itertools
from functools import reduce
import math
import uuid

import networkx as nx

def read_file(filename='input.txt'):
    with open(filename) as f:
        lines = f.readlines()
    lines = [str(l.strip()) for l in lines]
    return lines

def main():
    #part0()
    start = time.time()
    part1()
    middle = time.time()
    part2()
    end = time.time()
    print("Part 1 Time:  " + str(middle-start))
    print("Part 2 Time:  " + str(end-middle))
    print("Total Time:   " + str(end-start))

def flatten_tree_leaves(mytree):
    flat_tree = []
     
    if mytree.isLeaf():
        flat_tree.append(mytree.identifier)
    else:
        flat_tree.extend(flatten_tree_leaves(mytree.left))
        flat_tree.extend(flatten_tree_leaves(mytree.right))
    return flat_tree

class Tree: 
    def __init__(self, cargo, left=None, right=None):
        self.identifier = uuid.uuid4()
        self.cargo = cargo
        self.left = left
        self.right = right
    
    def __str__(self):
        #return str(self.identifier) +" "+ str(self.cargo) if self.isLeaf() else "(" + str(self.left) + "," +str(self.right) + ")"
        return  str(self.cargo) if self.isLeaf() else "(" + str(self.left) + "," +str(self.right) + ")"
    
    def isLeaf(self):
        return (self.left is None and self.right is None)
        
def find_first_deep_node_id(snailfishtree, level):
    left = snailfishtree.left
    right = snailfishtree.right
    
    if level >= 4:
        if not snailfishtree.isLeaf() and left.isLeaf() and right.isLeaf():
            newTree = Tree(0)
            #print (newTree.identifier)
            return (newTree, snailfishtree, newTree.identifier, True) #the replacement, the oldnode, the new tree identifier, and if it was found
            
    if snailfishtree.isLeaf():
        return (snailfishtree, None, None, False)
    else:
        (leftresult, oldnode, id, found) = find_first_deep_node_id(left, level+1)
        if found: 
            return (Tree(None, leftresult, right), oldnode, id, True)
        (rightresult, oldnode, id,  found) = find_first_deep_node_id(right, level+1)
        if found: 
            return (Tree(None, left, rightresult), oldnode, id, True)
        return (Tree(None, leftresult, rightresult), None, None, False)
        
        
def add_to_node(snailfishtree, identifier, amount):
    left = snailfishtree.left
    right = snailfishtree.right
    cargo = snailfishtree.cargo
    
    if snailfishtree.isLeaf():
        if snailfishtree.identifier == identifier:
            #snailfishtree.cargo = cargo + amount
            return (Tree(cargo + amount), True)
        else:
            return (snailfishtree, False)
    else:
        (leftresult,replaced) = add_to_node(left, identifier, amount)
        if replaced: 
            return (Tree(None, leftresult, right), True)
        (rightresult, replaced) = add_to_node(right, identifier, amount)
        if replaced: 
            return (Tree(None, left, rightresult), True)
        return (Tree(None, leftresult, rightresult), False)

def explode(snailfishnum):    
    #find the node that needs to be exploded, and do first step (replace with 0)
    (updatedTree, leaf, id, _) = find_first_deep_node_id(snailfishnum, 0)
    
    searchlist = flatten_tree_leaves(updatedTree)
        
    #now update the values to the left and right of where that one was.
    index = searchlist.index(id)
    #print(index)
    
    if index == 0: 
        #discard the left part, only add the right part
        (updatedTree, _) = add_to_node(updatedTree, searchlist[index+1], leaf.right.cargo)
    elif index == len(searchlist) -1: 
        #discard the right part, only add the left part 
        (updatedTree, _) = add_to_node(updatedTree, searchlist[index-1], leaf.left.cargo)
    else: 
        (updatedTree, _) = add_to_node(updatedTree, searchlist[index+1], leaf.right.cargo)
        (updatedTree, _) = add_to_node(updatedTree, searchlist[index-1], leaf.left.cargo)

    return updatedTree
    
def depth(L):
    return 0 if L.isLeaf() else 1 + max(depth(L.left), depth(L.right))

def can_be_exploded(snailfishnum):
    #print("can_be_exploded: " + str(snailfishnum))
    return depth(snailfishnum) > 4
    
def can_be_split(snailfishtree):
    left = snailfishtree.left
    right = snailfishtree.right
    cargo = snailfishtree.cargo
    
    result = False
    
    if left != None:
        result = result or can_be_split(left)
    if right != None:
        result = result or can_be_split(right)
    if cargo != None:
        result = result or (cargo  > 9)
        
    return result
    
def snailsplit(snailfishtree):
    left = snailfishtree.left
    right = snailfishtree.right
    cargo = snailfishtree.cargo
    
    if snailfishtree.isLeaf(): 
        if (cargo > 9):
            #it needs to be split, split it!
            half = float(cargo)/2.0
            
            newleft = Tree(math.floor(half))
            newright = Tree(math.ceil(half))
            return (Tree(None, newleft, newright), True)
        else:
            return (snailfishtree, False)
    else: #both nodes should have trees in them, even if only cargo, so we won't check if they are not None
        
        (leftresult, found) = snailsplit(left)
        if found: 
            return (Tree(None, leftresult, right), True)
            
        (rightresult, found) = snailsplit(right)
        if found: 
            return (Tree(None, left, rightresult), True)
            
        return (Tree(None, leftresult, rightresult), False)

def can_be_reduced(snailfishnum):
    return can_be_exploded(snailfishnum) or can_be_split(snailfishnum)
     
def reduce_snailfish_number(snailfishnum):
    while can_be_reduced(snailfishnum):
        while can_be_exploded(snailfishnum):
            #print("explode")
            snailfishnum = explode(snailfishnum)
        if can_be_split(snailfishnum):
            #print ("split")
            #print ("split")
            (snailfishnum, _ ) = snailsplit(snailfishnum)
            
    return snailfishnum

def add_snailfish_number(snailfish_sum, num):
    #print (str(snailfish_sum) + " plus " + str(num))
    new_snailfish_sum = Tree(None, snailfish_sum, num)
    
    reduced_snailfish_sum = reduce_snailfish_number(new_snailfish_sum)
    
    return reduced_snailfish_sum

def make_tree(snailnum):
    first = snailnum[0]
    firsttree = None
    if isinstance(first, list):
        firsttree = make_tree(first)
    else:
        firsttree = Tree(first)
        
        
    second = snailnum[1]
    secondtree = None
    if isinstance(second, list):
        secondtree = make_tree(second)
    else:
        secondtree = Tree(second)
        
    return Tree(None, firsttree, secondtree)

def tree_magnitude(snailfishtree):
    if snailfishtree.isLeaf():
        return snailfishtree.cargo
    else:
        return 3*tree_magnitude(snailfishtree.left) + 2*tree_magnitude(snailfishtree.right)
    
def part0(): 
    #test the reducing code
    print("PART 0:")
    lines = read_file('reducinginput.txt')
    
    snailnums = [eval(l) for l in lines] #yolo
    
    for line in snailnums:
        snailTree = make_tree(line)
        print ("original: " + str(snailTree))
        result = reduce_snailfish_number(snailTree)
        print("result: " + str(result))
    print("-----------------------------")
    
def part1(): 
    print("PART 1:")
    lines = read_file()
    
    #Security, amirite?
    snailnums = [eval(l) for l in lines]
    snailTrees = [make_tree(s) for s in snailnums] 
    
   
    snailfish_sum = snailTrees[0]
    for line in snailTrees[1:]:
        snailfish_sum = add_snailfish_number(snailfish_sum, line)
    
    result = tree_magnitude(snailfish_sum)
    print("result: " + str(result))
    
def part2():
    print("PART 2:")
    lines = read_file()
    
    #Security, amirite?
    snailnums = [eval(l) for l in lines]
    snailTrees = [make_tree(s) for s in snailnums]
    
    combos = list(itertools.combinations(snailTrees, 2))
    #print ([str(c1) +", "+ str(c2) for (c1, c2) in combos])
    magnitudes = []
    #countdown = len(combos)
    for (item1, item2) in combos:
        #print(countdown)
        #countdown = countdown -1
        
        snailfish_sum1 = add_snailfish_number(item1, item2)
        magnitudes.append(tree_magnitude(snailfish_sum1))
        
        snailfish_sum2 = add_snailfish_number(item2, item1)
        magnitudes.append(tree_magnitude(snailfish_sum2))
        
        #print(magnitudes)
        
    result = max(magnitudes)
    print("result: " + str(result))
  
if __name__ == "__main__":
    main()