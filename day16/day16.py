import time
import numpy as np
from collections import Counter
from functools import reduce

hexadecimal = {
"0" : "0000",
"1" : "0001",
"2" : "0010",
"3" : "0011",
"4" : "0100",
"5" : "0101",
"6" : "0110",
"7" : "0111",
"8" : "1000",
"9" : "1001",
"A" : "1010",
"B" : "1011",
"C" : "1100",
"D" : "1101",
"E" : "1110",
"F" : "1111"} 

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

class Packet:
    version = ""
    packettype = ""
    def __init__(self, version,packettype):
        self.packettype = packettype
        self.version = version

class LiteralPacket(Packet):
    literal = ""
    def __init__(self, version, packettype, literal):
        Packet.__init__(self,version, packettype)
        self.literal = literal
        
class OperatorPacket(Packet):
    subPackets = []
    packetoperator = 0
    def __init__(self, version,packettype, packetoperator, subPackets):
        Packet.__init__(self,version, packettype)
        self.subPackets = subPackets
        self.packetoperator = packetoperator

def binstr_as_int(number):
    return int("0b"+ number, 0)
    
def parse_packet(bits):
    if len(bits) < 1:
        return
    version = binstr_as_int(bits[0:3])
    type = binstr_as_int(bits[3:6])
    
    bits = bits[6:]
    if type == 4: 
        return parse_literal_packet(version, bits)
    else: 
        return parse_operator_packet(version, type, bits)
        
def parse_literal_packet(version, bits):
    # its a literal
    literal = ""
    bits_length = len(bits)
    while True:
        group = bits[0:5]
        bits = bits[5:]
        if group[0] == "1":
            literal += group[1:5]
        elif group[0] == "0":
            literal += group[1:5]
            break
    #print ("literal: " + str(binstr_as_int(literal)))
    
    return (LiteralPacket(version, "literal", literal), bits)

def parse_operator_packet(version, type, bits):
    #its an operator
    length_type_id = bits[0]
    subpackets = []
    #print (bits)
    if length_type_id == "0":
        total_length_in_bits = binstr_as_int(bits[1:16])
        #print ("parsing the next " + str(total_length_in_bits) + " bits")
        bits = bits[16:]
        subpacketbits = bits[0:total_length_in_bits]
        bits = bits[total_length_in_bits:]
        
        while len(subpacketbits) > 0:
            (subPacket, subpacketbits) = parse_packet(subpacketbits)
            subpackets.append(subPacket)
    else: 
        number_of_packets = binstr_as_int(bits[1:12])
        bits = bits[12:]
        for i in range(number_of_packets):
            (subPacket, bits) = parse_packet(bits)
            subpackets.append(subPacket)
            
    return (OperatorPacket(version, "operator", type, subpackets), bits)
        
def part1(): 
    print("PART 1:")
    lines = read_file()

    for line in lines: 
        print ("-------------------------------------------")
        print (line)
        bits = "".join([hexadecimal[l] for l in list(line)])
        #print(bits)
        
        (packet, remaining_bits) = parse_packet(bits)
        #print_packet(packet)
        versions = find_versions(packet)
        print (versions)
    
        result = sum(versions)
        print("result: " + str(result))

def find_versions(packet):
    versions = []
    versions.append(packet.version)
    if packet.packettype == "operator": 
        for item in packet.subPackets:
            versions.extend(find_versions(item))
    return versions
        
def print_packet(packet):
    print ("version: " + str(packet.version))
    if packet.packettype == "literal":
        print ("Literal: "  + str(binstr_as_int(packet.literal)))
    elif packet.packettype == "operator": 
        print ("Operator: " + str(packet.packetoperator))
        print ("Subpackets: [")
        for item in packet.subPackets:
            print_packet(item)
        print ("]")
    
def part2():
    print("PART 2:")
    lines = read_file()
    
    for line in lines: 
        print ("-------------------------------------------")
        print (line)
        bits = "".join([hexadecimal[l] for l in list(line)])
        #print(bits)
        
        (packet, remaining_bits) = parse_packet(bits)
        
        print (generate_packet_string(packet))
        
        result = evaluate_packet(packet)
        print("result: " + str(result))
    
def evaluate_packet(packet):
    if packet.packettype == "literal": 
        return binstr_as_int(packet.literal)
    elif packet.packettype == "operator":
        subpackets = [evaluate_packet(pack) for pack in packet.subPackets]
        match packet.packetoperator:
            case 0:
                return sum(subpackets)
            case 1: 
                return reduce(lambda x, y: x*y, subpackets)   #np.prod(subpackets) << numpy defaults to INT32!!
            case 2: 
                return min(subpackets)
            case 3: 
                return max(subpackets)
            case 5: 
                return 1 if subpackets[0] > subpackets[1] else 0
            case 6: 
                return 1 if subpackets[0] < subpackets[1] else 0
            case 7: 
                return 1 if subpackets[0] == subpackets[1] else 0
    
def generate_packet_string(packet):
    if packet.packettype == "literal": 
        return str(binstr_as_int(packet.literal))
    elif packet.packettype == "operator":
        subpackets = [evaluate_packet(pack) for pack in packet.subPackets]
        match packet.packetoperator:
            case 0:
                return "(" + " + ".join([generate_packet_string(pack) for pack in packet.subPackets]) + ")"
            case 1:
                return "(" + " * ".join([generate_packet_string(pack) for pack in packet.subPackets]) + ")"
            case 2:
                return "min(" + ", ".join([generate_packet_string(pack) for pack in packet.subPackets]) + ")"
            case 3: 
                return "max(" + ", ".join([generate_packet_string(pack) for pack in packet.subPackets]) + ")"
            case 5: 
                
                return "(" +  (generate_packet_string(packet.subPackets[0])) + " > " + (generate_packet_string(packet.subPackets[1]))+ ")"
            case 6: 
                return "(" + (generate_packet_string(packet.subPackets[0])) + " < " + (generate_packet_string(packet.subPackets[1]))+ ")"
            case 7: 
                return "(" + (generate_packet_string(packet.subPackets[0])) + " == " + (generate_packet_string(packet.subPackets[1]))+ ")"

    
if __name__ == "__main__":
    main()