# Classes.py - stores primary classes for boards and board-solving used in other modules

# Import math module for .floor and .ceil
from math import floor
from random import choice, randint, shuffle
from time import sleep
import json
import pygame

# Import self-made modules
from createBoard import create, addFive
from strategies import strategies

# Temp function for printing formatted lists, delete later


def printListF(list1):
    for itemIter, item in enumerate(list1):
        if itemIter % 10 == 0:
            print(item)
        else:
            print(item, end="\t")

# Gives the lower index for row/column of a 3x3 square area on the board (depending on num location)


def sqIndexMin(index):
    return (3 * floor(index / 3))

# Gives the upper index for row/column of a 3x3 square area on the board (depending on num location)


# old eq for max limit: "(3 - (sqCol % 3)) + (sqCol - 1)"
def sqIndexMax(index):
    return ((3 * floor(index / 3)) + 3)

# Throw special exception IF too many errors made in SudokuParser obj


class MistakeException(Exception):
    pass

# Board class for sudoku board


class Sudoku():
    # Class variables for finding the bounds for the indexes within the area of a 3x3 square on the board
    def __init__(self, level: str = '3'):
        # self.squares = [Square(i, j) for i in range(1, 4) for j in range(1, 4)]  # Creates 9 Squares all numbered 1-3 vertically and horizontally
        self.answer = [["*" for col in range(9)] for row in range(9)]
        # determines whether a square has been modified or not (True = yes, False = no)
        self.visible = [["*" for col in range(9)] for row in range(9)]

        self.level = level

    # Iterates through the squares in Board (increments column first, then row)
    def __iter__(self):  # (is this really necessary...?)
        return (iter(self.answer))

    # Temp until I implement GUI
    def __str__(self):
        board = self.answer
        output = "╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗\n"

        for tileRow in self:
            output += "║"

            for tileSlot, tileNum in enumerate(tileRow):
                if tileSlot in [2, 5]:
                    if tileNum != "*":
                        output += f"\033[1;30;47m {tileNum} \033[0;0m║"
                    else:
                        output += f" {tileNum} ║"
                elif tileSlot != 8:
                    if tileNum != "*":
                        output += f"\033[1;30;47m {tileNum} \033[0;0m│"
                    else:
                        output += f" {tileNum} │"
                else:
                    if tileNum != "*":
                        output += f"\033[1;30;47m {tileNum} \033[0;0m"
                    else:
                        output += f" {tileNum} "

            output += "║\n"

            if tileRow is board[2] or tileRow is board[5]:
                output += "╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣\n"
            elif tileRow is not board[-1]:
                output += "╟───┼───┼───╫───┼───┼───╫───┼───┼───╢\n"

        output += "╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝"
        return output

    # Temp method to test if Board __iter__ method iterates properly

    def displayOccur(self, num):
        displayCount = 0
        print(f"Squares containing the value \"{num}\":")

        for indexRow, row in enumerate(self):
            for col in range(9):

                if row[col] == num:
                    displayCount += 1
                    print(
                        f"Square #{displayCount}: Row = {indexRow}, Column = {col}")

    # Generates a good sudoku board at the start of the game - generate determining num for chance of generating num in sq, then check if sq num complies with .check rules
    def getBoard(self):
        """
        (ver.6) Calls a function that reads json file for boards (instead of creating algorithm for generating a board)
        """
        # 1). Read file for boards first
        try:
            with open("boards.json", 'r') as fh:
                reader = fh.read()
                database = json.loads(reader)
        except FileNotFoundError:
            print("Error, check board.py line 113; either tried to read and store board data before \
                .json file even existed, or something unknown happened...")
            assert True == False

        # 2). Get boardID and corresponding board from database
        try:                 # block for dict debugging, can remove later
            boardID = int(database["Current Boards"][self.level])
            boards = database[self.level]

            for board in boards:
                if board["boardID"] == boardID:
                    self.answer = board["answer"]
                    self.visible = board["board"]
        except KeyError:     # Can remove later after debugging
            print("Error: Something's wrong with the \"database\" dictionary in board.py; maybe check \
                   and/or debug for the keys?")
            assert True == False

        # 3). Check if database needs to be updated w/ new boards + update current boards dict in database
        boardID += 1
        print(self.level, boardID)

        if boardID > 5:
            print("Adding new boards to json...")
            addFive(self.level)
        else:
            database["Current Boards"][self.level] = boardID

            with open("boards.json", 'w') as fh:
                output = json.dumps(database)
                fh.write(output)


class SudokuParser():
    def __init__(self, board: Sudoku):
        self.mistakes = 0
        self.answer = board.answer()
        self.visible = board.visible()
        self.notes = [[{i for i in range(1, 10)}
                       for j in range(9)] for k in range(9)]

    def mistakeCounter(numMistake):
        numMistake += 1

        if numMistake >= 3:
            print("Game Over (placeholder code here)")
            # Return some sort of boolean false value that will stop a continuous loop in main.py (which is in charge of continuing the game)
        return (numMistake)

    # def applyStrat(self, strategy):
    #     success = False
    #     boardIter = self.visible[:]

    #     for rowNum, row in enumerate(boardIter):
    #         for colNum, tile in enumerate(row):
    #             # 0 check for tile
    #             if tile != 0:
    #                 continue

    #             # Attempt to check if one value suitable for tile; if so, replaces tile old value with new one
    #             value = strategy(self, colNum, rowNum)
    #             if value == -1:
    #                 continue

    #             # print("Value:", value)
    #             success = True

    #             self.board[rowNum][colNum] = value
    #             # print("Board value:", self.board[rowNum][colNum])

    #     return success
        # while self.mistakes < 5:
        #     print("")

    def placeNum(self, guess, row, col):
        # print(f"\nAttempting to place number {num}...\n")
        # sleep(1)
        if guess == self.answer[row][col]:
            self.visible[row][col] = guess

            return True

        self.mistakes += 1
        return False

# --------------------#
# Test/Debug
# --------------------#
def main():          
    create()

    A = Sudoku("5")

    print(A)
    print("")
    print(A.answer)

    sleep(3)

    try:
        A.getBoard()

        print(A)
        print("")
        print(A.answer)
        
        # A.displayOccur(5)

        # sleep(2)

        # print(A.checkSquare(5, 5, 5))
        # print(A.checkRow(5, 5))
        # print(A.checkCol(5, 5))

        print("Success! (probably)")
    except AssertionError:
        print("...Something went wrong, so...")
        print("Failure.")


if __name__ == "__main__":
    main()

