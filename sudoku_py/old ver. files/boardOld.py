# Classes.py - stores primary classes used in main module

#Import math module for .floor and .ceil
from math import floor

mistakes = 0

def mistakeCounter(numMistake):
    numMistake += 1

    if numMistake >= 3:
        print("Game Over (placeholder code here)")
        # Return some sort of boolean false value that will stop a continuous loop in main.py (which is in charge of continuing the game)
    return(numMistake)

class Square:
    # Each square keeps track of row and column #
    def __init__(self, numRow, numCol):
        self.numRow = numRow
        self.numCol = numCol

        self.tiles = [[None] * 3,
                      [None] * 3,
                      [None] * 3]
        

    # Temp method to test if Board __iter__ method iterates properly
    def display(self):
        print(f"Row = {self.numRow}, Column = {self.numCol}")

# Main class, has various squares
class Board:
    def __init__(self):
        #self.squares = [Square(i, j) for i in range(1, 4) for j in range(1, 4)]  # Creates 9 Squares all numbered 1-3 vertically and horizontally
        self.squares = [[Square(row,column) for column in range(0,3)] for row in range(0,3)]
        self.mistakes = 0
    
    # Iterates through the squares in Board (increments column first, then row)
    def __iter__(self):                       #(is this really necessary...?)
        return iter(self.squares)
    
    # Code here for checking tiles within each square
    def checkSquare(self, num, sqRow, sqCol):
        for tileRow in self.squares[sqRow][sqCol].tiles:
            if num in tileRow:
                print("\nFailure, number is in square. (placeholder)\n")    ##### Code for registering one mistake, use False boolean maybe?
                return(False)

        print("\nSuccess, the number is not in the square.\n")                 ##### If no mistake, return True?
        return(True)

    def checkRow(self, num, sqRow, sqCol, tileRow):
        for col in range(3 * floor(sqCol / 3), (3 * floor(sqCol / 3)) + 3):    # old eq for max limit: "(3 - (sqCol % 3)) + (sqCol - 1)"
            if num in self.squares[sqRow][col].tiles[tileRow]:
                print("\nFailure, number is in row. (placeholder)\n")
                return(False)

        print("\nSuccess, the number is not in the row.\n")
        return(True)

    def placeNum(self, num, sqRow, sqCol, tileRow, tileCol):
        if not(self.checkSquare(num, sqRow, sqCol) and self.checkRow(num, sqRow, sqCol, tileRow)):
            print("Mistake + 1")
            mistakeCounter(mistakes)
        else:
            self.squares[sqRow][sqCol].tiles[tileRow][tileCol] = num