from collections import Counter

def read_file():
    with open('input.txt') as f:
        lines = f.readlines()
    return lines

def main():
    part1()
    part2()

def part1(): 
    print("PART 1:")
    lines = read_file()
    gamma = ""
    epsilon = ""
    ones = [0,0,0,0,0,0,0,0,0,0,0,0]
    zeros = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    for item in lines: 
        for i in range(len(item)): 
            digit = str(item[i])
            if digit == "0" :
                zeros[i] = zeros[i] + 1
            elif digit == "1":
                ones[i] = ones[i] + 1
            else:
                "OH NO"
    
    for i in range(len(ones)):
        if int(ones[i]) > int(zeros[i]):
            gamma = gamma + "1"
            epsilon = epsilon + "0"
        elif int(ones[i]) < int(zeros[i]):
            gamma = gamma + "0"
            epsilon = epsilon + "1"
        else:
            print("OH NO")
            
    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2) 
    
    print(gamma)
    print(epsilon)
    power = gamma * epsilon
    print("power: " + str(power))

def part2():
    print("PART 2:")
    lines = read_file()
    lines = [str(l.strip()) for l in lines]
    o2lines = lines
    co2lines = lines
    
    for i in range(12):
        if len(o2lines) == 1:
            break
        ith_digits = [l[i] for l in o2lines]
        zeros = ith_digits.count("0")
        ones = ith_digits.count("1")
        most_common_digit = "1"
        
        if (zeros > ones):
            most_common_digit = "0"

        newo2lines = []
        for line in o2lines: 
            if line[i] == most_common_digit:
                newo2lines.append(line)
        o2lines = newo2lines
        
    for i in range(12):
        if len(co2lines) == 1:
            break
        ith_digits = [l[i] for l in co2lines]
        zeros = ith_digits.count("0")
        ones = ith_digits.count("1")
        least_common_digit = "0"
        
        if (zeros > ones):
            least_common_digit = "1"

        newco2lines = []
        for line in co2lines: 
            if line[i] == least_common_digit:
                newco2lines.append(line)
        co2lines = newco2lines

    o2 = int(o2lines[0], 2)
    co2 = int(co2lines[0], 2)

    print (o2lines)
    print (co2lines)
    life = o2 * co2
    print("life: " + str(life))
    
if __name__ == "__main__":
    main()