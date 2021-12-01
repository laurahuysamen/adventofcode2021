
def read_file():
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def main():
    part1()
    part2()

def part1(): 
    lines = read_file()
    increases = 0
    decreases = 0
    previous = None
    
    for measurement in lines: 
        if previous == None:
            previous = int(measurement)
        else:
            if int(measurement) > previous:
                increases = increases + 1
            else:
                decreases = decreases + 1
            previous = int(measurement)
            
    print("PART 1:")
    print("Increases: " + str(increases))
    print("Decreases: " + str(decreases))
    print("SUM: " + str((increases + decreases)))
    print("Total: " + str(len(lines)))

def part2(): 
    lines = read_file()
    increases = 0
    decreases = 0
    
    previous_A = int(lines[0])
    previous_B = int(lines[1])
    previous_C = int(lines[2])

    for measurement in lines[3:]:
        previousSum = previous_A + previous_B + previous_C
        
        #update the values
        previous_A = previous_B
        previous_B = previous_C
        previous_C = int(measurement)
        
        newSum = previous_A + previous_B + previous_C
        
        if newSum > previousSum:
            increases = increases +1
        else:
            decreases = decreases +1
        
    print("PART 2:")
    print("Increases: " + str(increases))
    print("Decreases: " + str(decreases))
    print("SUM: " + str((increases + decreases)))
    print("Total: " + str(len(lines)))

if __name__ == "__main__":
    main()