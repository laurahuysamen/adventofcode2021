def read_file():
    with open('input.txt') as f:
        lines = f.readlines()
    lines = [str(l) for l in lines]
    return lines

def main():
    part1()
    part2()

def checkforwin(markerboard):
    for row in markerboard: 
        if all(marker for marker in row):
            return True
    for i in range(5):
        ith_column = [line[i] for line in markerboard]
        if all(marker for marker in ith_column):
            return True
    return False


def part1(): 
    print("PART 1:")
    lines = read_file()
    final_number = 0
    board_score = 0
    winning_board = None
    winning_markerboard = None
    
    calling_numbers = lines[0].strip().split(',')
    boards = []
    markerboards = []
    currentboard = []
    
    for line in lines[2:]: 
        if line == "\n":
            boards.append(currentboard)
            currentboard = []
            markerboards.append([[False,False,False,False,False],[False,False,False,False,False],[False,False,False,False,False],[False,False,False,False,False],[False,False,False,False,False]])
        else:
            currentboard.append(line.strip().split())
    
    for calling in calling_numbers:
        #print ( "CALLING " + str(calling))
        #update boards  
        for board_index in range(len(boards)):
            board = boards[board_index]
            markerboard = markerboards[board_index]
            
            for i in range(5):
                for j in range(5):
                    if int(board[i][j]) == int(calling): 
                        markerboard[i][j] = True

        #check boards
        for board_index in range(len(boards)):
            board = boards[board_index]
            markerboard = markerboards[board_index]
            
            if(checkforwin(markerboard)):
                winning_board = board
                winning_markerboard = markerboard
                break
        
        if winning_board != None:
            final_number = calling
            break
            
    print(winning_board)
    print(winning_markerboard)
    print(final_number)
    sum = 0
    
    for i in range(5):
        for j in range(5):
            if not winning_markerboard[i][j]: 
                sum = sum + int(winning_board[i][j])
    
    print(sum)
    result = sum * int(final_number)
    print("result: " + str(result))

def part2():
    print("PART 2:")
    lines = read_file()
    board_score = 0
    last_winning_board = None
    last_winning_markerboard = None
    final_number = 0
    
    calling_numbers = lines[0].strip().split(',')
    boards = []
    markerboards = []
    currentboard = []
    
    for line in lines[2:]: 
        if line == "\n":
            boards.append(currentboard)
            currentboard = []
            markerboards.append([[False,False,False,False,False],[False,False,False,False,False],[False,False,False,False,False],[False,False,False,False,False],[False,False,False,False,False]])
        else:
            currentboard.append(line.strip().split())
    
    for calling in calling_numbers:
        #print ( "CALLING " + str(calling))
        #update boards  
        for board_index in range(len(boards)):
            board = boards[board_index]
            markerboard = markerboards[board_index]
            
            for i in range(5):
                for j in range(5):
                    if int(board[i][j]) == int(calling): 
                        markerboard[i][j] = True
                        
        newboardlist = []
        newmarkerboardlist = []
        for board_index in range(len(boards)):
            board = boards[board_index]
            markerboard = markerboards[board_index]
            
            if(checkforwin(markerboard)):
                #remove it from the list and set it as the last winning one
                last_winning_board = board
                last_winning_markerboard = markerboard
                final_number = calling
            else:
                newboardlist.append(board)
                newmarkerboardlist.append(markerboard)
        boards = newboardlist
        markerboards = newmarkerboardlist
        
    print(last_winning_board)
    print(last_winning_markerboard)
    print(final_number)
    sum = 0
    
    for i in range(5):
        for j in range(5):
            if not last_winning_markerboard[i][j]: 
                sum = sum + int(last_winning_board[i][j])
    
    print(sum)
    result = sum * int(final_number)
    print("result: " + str(result))
    
if __name__ == "__main__":
    main()