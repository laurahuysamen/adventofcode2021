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
    start = time.time()
    part1()
    middle = time.time()
    part2()
    end = time.time()
    print("Part 1 Time:  " + str(middle-start))
    print("Part 2 Time:  " + str(end-middle))
    print("Total Time:   " + str(end-start))
    
deterministic_die = 0
number_of_deterministic_die_rolls = 0

def get_deterministic_die_roll():
    global deterministic_die, number_of_deterministic_die_rolls
    roll = deterministic_die + 1
    deterministic_die = (deterministic_die + 1)%100
    number_of_deterministic_die_rolls += 1
    return roll

def part1(): 
    print("PART 1:")
    lines = read_file()
    
    player1 = int(lines[0].split()[-1]) -1
    player2 = int(lines[1].split()[-1]) -1
    
    player1_score = 0
    player2_score = 0
    
    player1Turn = True
    
    while (player1_score < 1000 and player2_score < 1000):
        #take a turn
        if player1Turn:
            rolls = [get_deterministic_die_roll() , get_deterministic_die_roll() , get_deterministic_die_roll()]
            player1 = (player1 + sum(rolls)) % 10
            player1_score += player1 + 1
            #print(f"Player1 rolls: {rolls}, for score {player1_score}")
            player1Turn = False
        else: 
            rolls = [get_deterministic_die_roll() , get_deterministic_die_roll() , get_deterministic_die_roll()]
            player2 = (player2 + sum(rolls)) % 10
            player2_score += player2 + 1
            #print(f"Player2 rolls: {rolls}, for score {player2_score}")
            player1Turn = True
    
    
    global number_of_deterministic_die_rolls
    result = number_of_deterministic_die_rolls * min(player1_score, player2_score)
    print("result: " + str(result))

def generate_dirac_rolls():
    #(score, num_universes)
    return [(3,1),(4,3),(5,6),(6,7),(7,6),(8,3),(9,1)]
    

def part2():
    print("PART 2:")
    lines = read_file()
    player1 = int(lines[0].split()[-1]) -1
    player2 = int(lines[1].split()[-1]) -1

    player1Wins = 0
    player2Wins = 0
    
    universes = {(player1, 0, player2, 0): 1}
    
    player1Turn = True
    #each universe will have a state & a number of instances
    #(player1_pos, player1_score, player2_pos, player2_score), number_of_universes in this state
    #for each turn, duplicate out the new universes, 
    #check for win conditions and remove any that are in a winning state 
    while len(universes) > 0:
        print(len(universes), end = " ")
        new_universes = {}
        for (score, num_universes_spawned) in generate_dirac_rolls():
            for key in universes:
                (player1, player1_score, player2, player2_score) = key
                num_universes_existing = universes[key]
                if player1Turn: 
                    player1 = (player1 + score) % 10
                    player1_score += player1 + 1
                    if player1_score > 20:
                        #we've won these universes, skip over the rest of this
                        player1Wins += num_universes_spawned * num_universes_existing
                        continue
                else:
                    player2 = (player2 + score) % 10
                    player2_score += player2 + 1
                    if player2_score > 20:
                        #we've won these universes, skip over the rest of this
                        player2Wins += num_universes_spawned * num_universes_existing
                        continue
                        
                #we haven't won these games yet, so add them to the next round
                newKey = (player1, player1_score, player2, player2_score)
                if newKey in new_universes:
                    new_universes[newKey] += num_universes_spawned * num_universes_existing
                else:
                    new_universes[newKey] = num_universes_spawned * num_universes_existing
                    
        universes = new_universes
        player1Turn = not player1Turn
        
    print ("")
    print (f"Player 1 wins: {player1Wins}")
    print (f"Player 2 wins: {player2Wins}")
    result = max(player1Wins, player2Wins)
    print("result: " + str(result))
  
if __name__ == "__main__":
    main()