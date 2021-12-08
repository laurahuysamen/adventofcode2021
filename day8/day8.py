import time

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
    
    results = [0]*10
    for line in lines:
        inout = [l.strip() for l in line.split("|")]
        wires = [l.strip() for l in inout[0].split()]
        display = [l.strip() for l in inout[1].split()]
        
        for digit in display:
            if len(digit) == 2:
                results[1] = results[1] + 1
            if len(digit) == 3:
                results[7] = results[7] + 1
            if len(digit) == 4:
                results[4] = results[4] + 1
            if len(digit) == 7:
                results[8] = results[8] + 1
                
    print(results)
    result = sum(results)
    print("result: " + str(result))


def part2():
    print("PART 2:")
    lines = read_file()
       
    results = []
    for line in lines:
        
        v0 = ""
        v1 = ""
        v2 = ""
        v3 = ""
        v4 = ""
        v5 = ""
        v6 = ""
        v7 = ""
        v8 = ""
        v9 = ""
        
        v2v3v5_candidates = []
        v0v6v9_candidates = []
        
        inout = [l.strip() for l in line.split("|")]
        wires = [l.strip() for l in inout[0].split()]
        display = [l.strip() for l in inout[1].split()]
        
        for digit in wires:
            if len(digit) == 2: #must be a 1, should activate c & f
                v1 = digit
            if len(digit) == 3: #must be a 7, should activate a, c & f
                v7 = digit
            if len(digit) == 4:#must be a 4, should activate b,c,d,f
                v4 = digit 
            if len(digit) == 7:#must be a 8, should activate a,b,c,d,e,f,
                v8 = digit
            if len(digit) == 5: # must be a 2, 3, or 5, should activate a,b,c,d,e,f,g
                v2v3v5_candidates.append(digit)
            if len(digit) == 6: # must be a 0, 6, or 9, should activate a,b,c,d,e,f,g
                v0v6v9_candidates.append(digit)
        
        #based on the values for c and f, we should now know what segment a is:
        a = [val for val in v7 if val not in v1][0]
        
        #we also know that 3 must be the one in v2, v3, and v5 that shares c & f
        for item in v2v3v5_candidates:
            if v1[0] in item and v1[1] in item:
                v3 = item
        
        v2v3v5_candidates.remove(v3)
        v2v5_candidates = v2v3v5_candidates
        
        #6 must be the one in v0, v6, v9 that does not share c & f
        for item in v0v6v9_candidates:
            if not(v1[0] in item and v1[1] in item):
                v6 = item
        
        v0v6v9_candidates.remove(v6)
        v0v9_candidates = v0v6v9_candidates
        
        # out of 0,2,5,9
        #0 is now the only one without the middle segment. 
        
        #which are the two segments not in 0 and 9?
        missing_digit0 = [val for val in "abcdefg" if val not in v0v9_candidates[0]][0]
        missing_digit1 = [val for val in "abcdefg" if val not in v0v9_candidates[1]][0]
        
        #which of these segments is not in 2 and 5? that's the middle segment and the marker of 9
        if missing_digit0 in v2v5_candidates[0] and missing_digit0 in v2v5_candidates[1]:
            v0 = v0v9_candidates[0]
            v9 = v0v9_candidates[1]
        else:
            v0 = v0v9_candidates[1]
            v9 = v0v9_candidates[0]
        
        #5 has all it's digits in common with 6, but 2 doesnt. 
        
        #so if we check the first one, if it's not in 6
        for val in v2v5_candidates[0]:
            if val not in v6:
                #this candidate must be 2
                v2 = v2v5_candidates[0]
                v5 = v2v5_candidates[1]
                break
                
        #otherwise it's 5
        if (v2 == ""):
            v5 = v2v5_candidates[0]
            v2 = v2v5_candidates[1]
        
        valueDict = {
        "".join(sorted(v0)) : "0",
        "".join(sorted(v1)) : "1",
        "".join(sorted(v2)) : "2",
        "".join(sorted(v3)) : "3",
        "".join(sorted(v4)) : "4",
        "".join(sorted(v5)) : "5",
        "".join(sorted(v6)) : "6",
        "".join(sorted(v7)) : "7",
        "".join(sorted(v8)) : "8",
        "".join(sorted(v9)) : "9",
        }
        print(valueDict)
        
        displayvalue = ""
        print (display)
        for digit in display:
            displayvalue = displayvalue + valueDict["".join(sorted(digit))]
            continue
        
        print (displayvalue)
        results.append(int(displayvalue))
        
    print(results)
    result = sum(results)
    print("result: " + str(result))
    #insert "it's done" frodo meme here

if __name__ == "__main__":
    main()