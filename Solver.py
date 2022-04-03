


matrix_of_sudoku = [[5,0,0,8,4,0,9,0,0],
                    [0,9,2,0,0,0,5,0,0],
                    [8,6,3,0,0,0,0,4,0],
                    [0,0,0,7,6,1,0,0,5],
                    [3,0,5,0,0,4,0,7,6],
                    [6,0,1,3,0,0,0,0,4],
                    [0,3,0,0,2,9,4,0,7],
                    [0,0,0,6,0,0,2,0,0],
                    [0,0,8,4,0,0,6,1,9]]

def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("---------------------") #pirnt line to separate every  row

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print("| ", end="") #separate every third column

            if j == 8:
                print(board[i][j]) #there is no space at the end of the one line of matrix
            else:
                print(str(board[i][j]) + " ", end="") #in any other case there is space after every number

def find_empty(board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == 0:
                return (y,x) #cordinates of the empty space

    return None

def valid(board, num, pos):

    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range (box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False

    return True



def solve(board):
    empty_spot_exist = find_empty(board)
    if not empty_spot_exist:
        return True
    else:
        row, column = empty_spot_exist

    for i in range(1,10):
        if valid(board, i, (row,column)):
            board[row][column] = i
            if solve(board):
                return True
            board[row][column] = 0

    return False


print_board(matrix_of_sudoku)
solve(matrix_of_sudoku)
print("_______________________")
print_board(matrix_of_sudoku)
