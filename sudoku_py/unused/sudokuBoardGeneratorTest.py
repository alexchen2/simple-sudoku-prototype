import random

numSet = [x for x in range(10)]

def create_board(height, width):
    board = [[(i + k) % 9 + 1 for i in range(1, height + 1)] for k in range(width)] # Creates a board where each row counts to 9 such that no row contains more than one kind of each number. You can run this separately to see what it generates.
    
    # random.shuffle(board) # Shuffles this list of lists
    # board = [[board[x][y] for x in range(9)] for y in range(9)] # Reads each row and puts it into a column. (basically rotates it to its side)
    # random.shuffle(board) # Shuffles this list again but while its on its side
    return board

for i in create_board(9, 9):
    print(i)