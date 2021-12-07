def read_file():
    with open('input.txt') as f:
        lines = f.readlines()
    lines = [str(l.strip()) for l in lines]
    lines = [int(l) for l in lines[0].split(",")]
    return lines

def nth_triangle_num(n):
    return (n)*(n + 1) / 2.

def calculate_triangle_fuel(lines, position):
    return sum([nth_triangle_num(abs(position - line)) for line in lines])

def calculate_fuel(lines, position):
    return sum([abs(position - line) for line in lines])

def main():
    part1()
    part2()

def part1(): 
    print("PART 1:")
    lines = read_file()
    mymin = min(lines)
    mymax = max(lines)
    print(mymin)
    print(mymax)
    minfuel = 1000000000000000000000000
    
    for position in range(mymin, mymax+1):
        #print (position)
        fuel = calculate_fuel(lines, position)
        #print (fuel)
        if fuel < minfuel:
            minfuel = fuel
    
    result = minfuel
    print("result: " + str(result))

def part2():
    print("PART 2:")
    lines = read_file()
    mymin = min(lines)
    mymax = max(lines)
    print(mymin)
    print(mymax)
    minfuel = 1000000000000000000000000
    
    for position in range(mymin, mymax+1):
        #print (position)
        fuel = calculate_triangle_fuel(lines, position)
        #print (fuel)
        if fuel < minfuel:
            minfuel = fuel
    
    result = minfuel
    print("result: " + str(result))

if __name__ == "__main__":
    main()