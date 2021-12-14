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

def calculate_step(polymer, replacements):
    newpolymer = ""
    for i in range(len(polymer)-1):
        subpolymer = polymer[i:i+2]
        #print (subpolymer)
        if subpolymer in replacements:
            newpolymer = newpolymer + replacements[subpolymer]
        else:
            newpolymer = newpolymer + subpolymer
    newpolymer = newpolymer + polymer[-1:]
    #print(newpolymer)
    #print("---------------------------")
    return newpolymer

def part1(): 
    print("PART 1:")
    lines = read_file()
    
    polymer = lines[0]
    
    pairs = lines[2:]
    mypairs = [(pair.split()[0], pair.split()[2]) for pair in pairs]
    pairdict = {}
    for (search,replace) in mypairs:
        searchsplit = list(search)
        pairdict[search] = search[0] + replace 
    #print (pairdict)
    
    for step in range(10):
        polymer = calculate_step(polymer, pairdict)
        print (len(polymer))
        
       
    occurances = Counter(list(polymer))
    print(occurances)
    common = occurances.most_common()
    print(common)
    result = common[0][1] - common[-1][1]
    print("result: " + str(result))

    
def part2():
    print("PART 2:")
    lines = read_file()
    
    polymer = lines[0]
    
    pairs = lines[2:]
    mypairs = [(pair.split()[0], pair.split()[2], pair.split()[0][0]+pair.split()[2], pair.split()[2]+pair.split()[0][1]) for pair in pairs]
    
    pairdict = {}
    initial_pairs = {}
    letters_running_count = {}
    
    for (pair, letter, a , b) in mypairs:
        letters_running_count[letter] = 0
        initial_pairs[pair] = 0
        pairdict[pair] = (letter, a, b)
    
    for letter in polymer: 
        letters_running_count[letter] += 1
        
    #print(mypairs)
    #print(letters_running_count)
    #print(initial_pairs)
    
    first_step = initial_pairs.copy()
    
    for i in range(len(polymer)-1):
        subpolymer = polymer[i:i+2]
        #print (subpolymer)
        if subpolymer in pairdict:
            (letter, a, b) = pairdict[subpolymer]
            letters_running_count[letter] += 1
            if a in initial_pairs:
                first_step[a] += 1
            if b in initial_pairs: 
                first_step[b] += 1
    
    #print(letters_running_count)
    #print(first_step)
    
    previous_step = first_step
    for step in range(39):
        #print(previous_step)
        next_step = initial_pairs.copy()
        
        for key in previous_step: 
            val = previous_step[key]
            (letter, a, b) = pairdict[key]
            letters_running_count[letter] += val
            if a in initial_pairs:
                next_step[a] += val
            if b in initial_pairs: 
                next_step[b] += val
        previous_step = next_step
    
    # for step in range(40):
        # next_step.append(step)
    print(letters_running_count)
    
    
    
    # for step in range(40):
        # polymer = calculate_step(polymer, pairdict)
        # print (len(polymer))
        
       
    occurances = Counter(letters_running_count)
    print(occurances)
    common = occurances.most_common()
    print(common)
    result = common[0][1] - common[-1][1]
    print("result: " + str(result))
    
if __name__ == "__main__":
    main()