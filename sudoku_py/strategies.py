# strategies.py - stores functions and classes for solving sudoku boards, used in board.py

from math import floor

#---------------#
# Helper Functions (used in strats):
#---------------#

# Gives the lower index for row/column of a 3x3 square area on the board (depending on num location) 
def sqIndexMin(index):
    return 3 * floor(index / 3)

# Gives the upper index for row/column of a 3x3 square area on the board (depending on num location) 
def sqIndexMax(index):                    # old eq for max limit: "(3 - (sqCol % 3)) + (sqCol - 1)"
    return (3 * floor(index / 3)) + 3

# Code here for checking tiles within each row
def checkRow(nums : list, board, tileRow):
    setNums = set(nums)
    setRow = set(board[tileRow])

    # Set operations
    output = setNums - (setRow & setNums)

    if output == set():
        return [False, {}]

    return [True, output]

# Code here for checking tiles within each square 
def checkSq(nums : list, board, tileRow, tileCol):
    rowPseudo = []

    for indexRow in range(sqIndexMin(tileRow), sqIndexMax(tileRow)):
        for indexCol in range(sqIndexMin(tileCol), sqIndexMax(tileCol)):
            rowPseudo.append(board[indexRow][indexCol])

    return checkRow(nums, [rowPseudo], 0)

# Method for checking for repeats of a number in a single column
def checkCol(nums : list, board, tileCol):
    rowPseudo = []
    # Obtain nums in each row and place into a "pseudo-row"
    for row in board:
        rowPseudo.append(row[tileCol])
    
    # Simply get output of checkRow with rowPseudo and nums
    return checkRow(nums, [rowPseudo], 0)

def checkAll(nums : list, board, tileRow, tileCol):
    # Note: each elem of checks -> 1st = check if any num possible at all from check;
    #                              2nd = set of all possible nums that work
    checks = [checkSq(nums, board, tileRow, tileCol), 
              checkRow(nums, board, tileRow), 
              checkCol(nums, board, tileCol)]
    checksTF = [i[0] for i in checks]     # strat only works if all true values inside
    checksSet = [i[1] for i in checks]    # set of numbers that possibly work; we want only one # that passes all checks
    return checksTF, checksSet            # Note to self: returns TWO vars, not one

#---------------#
# Actual Strategies:
#---------------#

# Finished!
def NakedSingles(board, tileRow, tileCol):
    nums = [num for num in range(1, 10)]

    # Refer to same vars in checkAll for descrip. on checksTF and checksSet
    checksTF, checksSet = checkAll(nums, board, tileRow, tileCol)

    if all(checksTF):
        validNums = list(checksSet[0] & checksSet[1] & checksSet[2])

        if len(validNums) == 1:
            return validNums[0]
    
    return -1

# Finished!
def HiddenSingles(board, tileRow, tileCol):
    nums = [num for num in range(1, 10)]

    # 1). Check for valid values in tile first
    checksTF, checksSet = checkAll(nums, board, tileRow, tileCol)

    if all(checksTF):
        validNums = checksSet[0] & checksSet[1] & checksSet[2]  # set of all possible candidates for this specific tile only
        output = validNums.copy()
    else:
        return -1       # Placeholder value for failure of strat
    
    # 2). Check for valid values in row:
    for indexCol, tile in enumerate(board[tileRow]):
        if tile in nums or indexCol == tileCol:
            continue      # If tile already has a number in it, then save time by jumping to the next (rework later)

        checksTF, checksSet = checkAll(nums, board, tileRow, indexCol)
        # Intersection op. will handle any cases for whether checksTF has False values anyways, so don't have to make extra
        # conditional cases for it
        tempNums = checksSet[0] & checksSet[1] & checksSet[2]
        output -= tempNums    # set difference; want candidates that only appear once in the entire row

    if len(output) == 1:   # Check if only one unique candidate that appears in original tile of question within row
        return list(output)[0]
    output = validNums.copy() # otherwise, refresh output set to validNums set

    # 3). Check for valid values in col:
    for indexRow, row in enumerate(board):
        tile = row[tileCol]

        if tile in nums or indexRow == tileRow: 
            continue

        checksTF, checksSet = checkAll(nums, board, indexRow, tileCol)
        tempNums = checksSet[0] & checksSet[1] & checksSet[2]
        output -= tempNums    # set difference; want candidates that only appear once

    if len(output) == 1:   # Check if only one unique candidate that appears in original tile of question within col
        return list(output)[0]
    output = validNums.copy() # otherwise, refresh output set to validNums set

    # 4). Check for valid values in same sq:
    for indexRow in range(sqIndexMin(tileRow), sqIndexMax(tileRow)):
        for indexCol in range(sqIndexMin(tileCol), sqIndexMax(tileCol)):
            tile = board[indexRow][indexCol]

            if tile in nums or [indexRow, indexCol] == [tileRow, tileCol]:
                continue

            checksTF, checksSet = checkAll(nums, board, indexRow, indexCol)
            tempNums = checksSet[0] & checksSet[1] & checksSet[2]
            output -= tempNums    # set difference; want candidates that only appear once

    if len(output) == 1:   # Check if only one unique candidate that appears in original tile of question within col
        return list(output)[0]
    
    print("Fail 2")
    return -1    # strat fails

#---------------#
# Global Variables:
#---------------#
strategies = [NakedSingles, HiddenSingles]

def main(): # Debugging purposes
    testNum = [1, 2, 3, 4, 5, 6, 7, 8] 
    testBoard = [[7, 0, 0, 0, 0, 0, 0, 2, 0], 
                 [0, 8, 3, 0, 9, 1, 5, 0, 7], 
                 [5, 0, 6, 4, 0, 3, 0, 9, 0], 
                 [0, 9, 4, 7, 0, 5, 3, 0, 8], 
                 [0, 0, 0, 0, 6, 0, 2, 0, 0], 
                 [2, 0, 1, 9, 0, 0, 0, 4, 0], 
                 [0, 4, 0, 0, 8, 0, 6, 0, 5], 
                 [0, 3, 5, 6, 0, 7, 1, 0, 0], 
                 [8, 0, 7, 0, 1, 2, 0, 0, 4]]
    testBoard2 = [[7, 1, 9, 8, 5, 6, 4, 2, 3], 
                  [4, 8, 3, 0, 9, 1, 5, 6, 7], 
                  [5, 2, 6, 4, 7, 3, 8, 9, 1], 
                  [6, 9, 4, 7, 2, 5, 3, 1, 8], 
                  [3, 7, 8, 1, 6, 4, 2, 5, 9], 
                  [2, 5, 1, 9, 3, 8, 7, 4, 6], 
                  [1, 4, 2, 3, 8, 9, 6, 7, 5],
                  [9, 3, 5, 6, 4, 7, 1, 8, 2], 
                  [8, 6, 7, 5, 1, 2, 9, 3, 4]]

    # Board for testing Hidden Singles (at tile coords. (1, 7); should return "7") 
    # Another test: (6, 6) should return 3         
    testBoard3 = [[7, 9, 0, 0, 0, 0, 6, 0, 0],
                  [0, 0, 3, 9, 0, 4, 0, 0, 0],
                  [0, 0, 0, 0, 8, 0, 0, 9, 3],
                  [0, 3, 2, 0, 0, 0, 0, 0, 0],
                  [9, 0, 7, 0, 4, 0, 2, 0, 0],
                  [8, 1, 0, 2, 0, 0, 9, 0, 7],
                  [5, 7, 9, 4, 2, 6, 0, 0, 0],
                  [0, 0, 0, 5, 0, 0, 7, 6, 0],
                  [1, 0, 0, 0, 3, 0, 5, 0, 9]]
    # (1, 3; 2)

    print(NakedSingles(testBoard, 1, 3))
    print(checkSq([2], testBoard2, 1, 3))
    print(checkRow([2], testBoard2, 1)[0])
    print(checkCol([2], testBoard2, 3)[0])

    print(HiddenSingles(testBoard3, 1, 7))
    print(HiddenSingles(testBoard3, 6, 6))
    print(checkAll(testNum, testBoard3, 1, 7))
    test1 = {1, 2, 3}
    test2 = {2, 3, 4}
    test3 = test1 | test2
    test4 = test3
    # print(test3, test4)
    test4 -= test1
    # print(test3, test4)

if __name__ == "__main__":
    main()