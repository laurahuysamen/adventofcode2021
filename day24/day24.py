import time
import numpy as np
from collections import Counter
import itertools
from functools import reduce
import math
import uuid
import networkx as nx
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

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

def add(alu, a, b):
    operation = ""
    if (b in ["w","x","y","z"]):
        alu[a] = alu[a] + alu[b]
        operation = f"\nalu[\"{a}\"] = alu[\"{a}\"] + alu[\"{b}\"]"
    else:
        alu[a] = alu[a] + int(b)
        operation = f"\nalu[\"{a}\"] = alu[\"{a}\"] + {b}"
    return (alu, operation)

def mul(alu, a, b):
    operation = ""
    if (b in ["w","x","y","z"]):
        alu[a] = alu[a] * alu[b]
        operation = f"\nalu[\"{a}\"] = alu[\"{a}\"] * alu[\"{b}\"]"
    else:
        alu[a] = alu[a] * int(b)
        operation = f"\nalu[\"{a}\"] = alu[\"{a}\"] * {b}"
    return (alu, operation)
    
def div(alu, a, b):
    operation = ""
    if (b in ["w","x","y","z"]):
        alu[a] = math.trunc(alu[a] / alu[b])
        operation = f"\nalu[\"{a}\"] = math.trunc(alu[\"{a}\"] / alu[\"{b}\"])"
    else:
        alu[a] = math.trunc(alu[a] / int(b))
        operation = f"\nalu[\"{a}\"] = math.trunc(alu[\"{a}\"] / {b})"
    return (alu, operation)
    
def mod(alu, a, b):
    operation = ""
    if (b in ["w","x","y","z"]):
        alu[a] = alu[a] % alu[b]
        operation = f"\nalu[\"{a}\"] = alu[\"{a}\"] % alu[\"{b}\"]"
    else:
        alu[a] = alu[a] % int(b)
        operation = f"\nalu[\"{a}\"] = alu[\"{a}\"] % {b}"
    return (alu, operation)
    
def eql(alu, a, b):
    operation = ""
    if (b in ["w","x","y","z"]):
        alu[a] = 1 if alu[a] == alu[b] else 0
        operation = f"\nalu[\"{a}\"] = 1 if alu[\"{a}\"] == alu[\"{b}\"] else 0"
    else:
        alu[a] = 1 if alu[a] == int(b) else 0
        operation = f"\nalu[\"{a}\"] = 1 if alu[\"{a}\"] == {b} else 0"
    return (alu, operation)
    
def part1(): 
    print("PART 1:")
    lines = read_file()
    
    input = [int(i) for i in list("99999999999999")]
    
    alu = {"w":0, "x":0, "y":0, "z":0}
    digit_verifications = []
    digit_verification = ""
    for line in lines:
        if line.startswith("inp"):
            digit_verifications.append(digit_verification)
            (_, a) = line.split()
            alu[a] = input[0]
            input = input[1:]
            digit_verification = f"alu[\"{a}\"] = input[0]\ninput = input[1:]"
            if (alu[a] == 0): #just in case
                print ("PANIK")
                break
        else:
            (op, a, b) = line.split()
            operation = ""
            match op:
                case "add":
                    (alu, operation) = add(alu, a, b)
                case "mul":
                    (alu, operation) = mul(alu, a, b)
                case "div":
                    (alu, operation) = div(alu, a, b)
                case "mod":
                    (alu, operation) = mod(alu, a, b)
                case "eql":
                    (alu, operation) = eql(alu, a, b)
            digit_verification +=(operation)
    #for veri in digit_verifications:
    #    print(veri)
    
    
    #now that we've made the list of instructions.
    
    #looking at the input, x & y always have their first use as * 0, so are always zero for the beginning of the instruction.
    #Therefore, only z and w influence the value from step to step. 
    #x=0,y=0     
    #working from the back, what are the possible inputs for w and z that cause the last instruction to be 0? 
    
    
    #key note, looking at the instruction set, z must be -26 < 0 < +26 at step 5 which bounds our search space to a reasonable value!
    possible = find_possible_serial_numbers(digit_verifications, 0)
    
    result = max(possible)
    print("result: " + str(result))

# def find_valid_serial_numbers(digit_verifications, z_expectation):
    # numbers = []
    # print(len(digit_verifications))
    # if len(digit_verifications) == 0: #we've reached our end condition, we've been through all the instructions
        # return (True, [""])
    # else:
        # validpairs = find_valid_inputs(z_expectation, digit_verifications.pop())
        # print(f"validpairs={validpairs}")
        # if len(validpairs) == 0: #there's nothing valid for this expectation, kill it
            # return (False, [])
        # else:
            # for (w,z) in validpairs:
                # successful, nums = find_valid_serial_numbers(digit_verifications, z)
                # print(f"nums = {nums}")
                # if successful:
                    # numbers.extend([tail + str(w) for tail in nums])
            # return (True, numbers)
            
def find_possible_serial_numbers(digit_verifications, z_expectation):
    numbers = []
    print(len(digit_verifications))
    if len(digit_verifications) == 0: 
        #we've reached our end condition, we've been through all the instructions
        return [""]
    else:
        instruction_to_run = digit_verifications.pop()
        validpairs = find_valid_inputs(z_expectation, instruction_to_run)
        if len(validpairs) == 0: #there's nothing valid for this expectation, kill it
            return []
        else:
            print(f"validpairs={validpairs}")
            for (w,z) in validpairs:
                nums = find_possible_serial_numbers(digit_verifications, z)
                #print(f"nums = {nums}")
                numbers.extend([tail + str(w) for tail in nums])
            return numbers
            
      
            
def find_valid_inputs(z_expectation, instruction):
    validpairs = []
    for w in range(1,9):
        for z in range(-100000000000, 100000000000):
            alu = {"w":0, "x":0, "y":0, "z":z}
            input = [w]
            exec(instruction)
            if alu["z"] == z_expectation:
                validpairs.append((w,z))
    return validpairs
        
def part2():
    print("PART 2:")
    lines = read_file()
   

    result = 0
    print("result: " + str(result))

    
if __name__ == "__main__":
    main()