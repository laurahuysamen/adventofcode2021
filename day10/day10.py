import time
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

def part1(): 
    print("PART 1:")
    lines = read_file()
     
    opens = ["(", "[", "{", "<"]
    closes = [")", "]", "}", ">"]
    
    incomplete_lines = []
    corrupted_lines = []
    corrupting_chars = []
    
    for line in lines:
        corrupted = False
        expectedStack = []
        for l in line: 
            if l in opens: #we've opened a new chunk
                expectedStack.append(closes[opens.index(l)])
            elif l == expectedStack[-1]: #we've closed a chunk
                expectedStack.pop(-1) # remove it from the expected list
            else: #we've got an invalid character!
                corrupted = True
                corrupting_chars.append(l)
                break
        if corrupted: 
            corrupted_lines.append(line)
        else: 
            incomplete_lines.append(line)
    
    #work out points for corrupting_chars
    c = Counter(corrupting_chars)
    print (c)
    
    result = c[")"]*3 + c["]"]*57 + c["}"]*1197 + c[">"]*25137
    print("result: " + str(result))

def part2():
    print("PART 2:")
    lines = read_file()
    
    opens = ["(", "[", "{", "<"]
    closes = [")", "]", "}", ">"]
    
    incomplete_lines = []
    incomplete_stacks = []
    
    corrupting_chars = []
    
    for line in lines:
        corrupted = False
        expectedStack = []
        for l in line: 
            if l in opens: #we've opened a new chunk
                expectedStack.append(closes[opens.index(l)])
            elif l == expectedStack[-1]: #we've closed a chunk
                expectedStack.pop(-1) # remove it from the expected list
            else: #we've got an invalid character!
                corrupted = True
                corrupting_chars.append(l)
                break
        if not corrupted: 
            incomplete_lines.append(line)
            incomplete_stacks.append(expectedStack)
            
    scores = []
    
    for incomplete_stack in incomplete_stacks:
        closing_sequence = reversed(incomplete_stack)
        print (incomplete_stack)
        score = 0
        for bracket in closing_sequence:
            score = score*5
            score = score + closes.index(bracket) + 1
        scores.append(score)
        
    scores = sorted(scores)
    print (scores)
    
    middle = int(len(scores)/2)
    result = scores[middle]
    print("result: " + str(result))
    
if __name__ == "__main__":
    main()