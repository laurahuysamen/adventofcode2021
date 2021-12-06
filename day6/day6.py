import math 
from decimal import * 
from collections import Counter

def read_file():
    with open('input.txt') as f:
        lines = f.readlines()
    lines = [str(l.strip()) for l in lines]
    return lines
    
def calculate_step(existing_fish):
    new_fish = []
    for fish in existing_fish:
        if fish == 0:
            #add old_fish 
            new_fish.append(6)
            #new_fish!
            new_fish.append(8)
        else:
            new_fish.append(fish-1)
    return new_fish
    
def main():
    part1()
    part2()

def part1(): 
    print("PART 1:")
    lines = read_file()
    fish = [int(f) for f in lines[0].split(",")]
    
    for i in range(80):
        fish = calculate_step(fish)
        #print (str(i+1) + " days " + str(len(fish)))
    
    result = len(fish)
    print("result: " + str(result))

def part2():
    print("PART 2:")
    lines = read_file()
    fish = [int(f) for f in lines[0].split(",")]
    occurances = Counter(fish)
    #print(occurances)
    
    fish0 = occurances[0]
    fish1 = occurances[1]
    fish2 = occurances[2]
    fish3 = occurances[3]
    fish4 = occurances[4]
    fish5 = occurances[5]
    fish6 = occurances[6]
    fish7 = occurances[7]
    fish8 = occurances[8]
    
    days = 256
    for day in range(days):
        oldfish8 = fish8
        oldfish0 = fish0 
        
        fish0 = fish1
        fish1 = fish2
        fish2 = fish3
        fish3 = fish4
        fish4 = fish5
        fish5 = fish6
        fish6 = fish7
        fish7 = fish8
        
        fish8 = oldfish0
        fish6 = fish6 + oldfish0
    
    result = fish0+ fish1+ fish2+ fish3+ fish4+ fish5+ fish6+ fish7+ fish8
    
    print("result: " + str(result))
if __name__ == "__main__":
    main()