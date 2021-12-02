
def read_file():
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def main():
    part1()
    part2()

def part1(): 
    lines = read_file()
    horizontalposition = 0
    depth = 0
    
    for command in lines: 
        instructions = command.split()
        direction = instructions[0]
        unit = int(instructions[1])
        
        if direction == "forward":
            horizontalposition = horizontalposition + unit
            
        elif direction == "down":
            depth = depth + unit
            
        elif direction == "up":
            depth = depth - unit
        else:
            print("OH NO")
            
    print("PART 1:")
    print("Horizontal: " + str(horizontalposition))
    print("Depth: " + str(depth))
    print("Multiplied: " + str(depth*horizontalposition))

def part2():
    lines = read_file()
    horizontalposition = 0
    depth = 0
    aim = 0 
    
    for command in lines: 
        instructions = command.split()
        direction = instructions[0]
        unit = int(instructions[1])
        
        if direction == "forward":
            horizontalposition = horizontalposition + unit
            depth = depth + (aim * unit)
            
        elif direction == "down":
            aim = aim + unit
            
        elif direction == "up":
            aim = aim - unit
        else:
            print("OH NO")
            
    print("PART 2:")
    print("Horizontal: " + str(horizontalposition))
    print("Depth: " + str(depth))
    print("Multiplied: " + str(depth*horizontalposition))
    
if __name__ == "__main__":
    main()