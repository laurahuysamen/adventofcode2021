
def read_file():
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def main():
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
            
    print("Increases: " + str(increases))
    print("Decreases: " + str(decreases))
    print("SUM: " + str((increases + decreases)))
    print("Total: " + str(len(lines)))

if __name__ == "__main__":
    main()