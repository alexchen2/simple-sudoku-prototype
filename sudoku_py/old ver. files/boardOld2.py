# Classes.py - stores primary classes used in main module

#Import math module for .floor and .ceil
from math import floor
from random import randint
from time import sleep

def mistakeCounter(numMistake):
    numMistake += 1

    if numMistake >= 3:
        print("Game Over (placeholder code here)")
        # Return some sort of boolean false value that will stop a continuous loop in main.py (which is in charge of continuing the game)
    return(numMistake)

mistakes = 0

# Gives the lower index for row/column of a 3x3 square area on the board (depending on num location) 
def sqIndexMin(index):
    return(3 * floor(index / 3))

# Gives the upper index for row/column of a 3x3 square area on the board (depending on num location) 
def sqIndexMax(index):                    # old eq for max limit: "(3 - (sqCol % 3)) + (sqCol - 1)"
    return((3 * floor(index / 3)) + 3)

# Board class for sudoku board
class Board:

    # Class variables for finding the bounds for the indexes within the area of a 3x3 square on the board

    def __init__(self):
        #self.squares = [Square(i, j) for i in range(1, 4) for j in range(1, 4)]  # Creates 9 Squares all numbered 1-3 vertically and horizontally
        self.squares = [[None for col in range(9)] for row in range(9)]

        self.mistakes = 0
    
    # Iterates through the squares in Board (increments column first, then row)
    def __iter__(self):                       #(is this really necessary...?)
        return(iter(self.squares))

    # Temp until I implement GUI
    def displayBoard(self):
        for tileRow in self:
            for tileNum in tileRow:
                print(tileNum, end = "\t")
            
            print("\n")
    
    # Temp method to test if Board __iter__ method iterates properly
    def displayOccur(self, num):
        displayCount = 0
        print(f"Squares containing the value \"{num}\":")

        for indexRow, row in enumerate(self):
            for col in range(9):

                if row[col] == num:
                    displayCount += 1
                    print(f"Square #{displayCount}: Row = {indexRow}, Column = {col}")

    # Code here for checking tiles within each square
    def checkSquare(self, num, tileRow, tileCol):
        for indexRow in range(sqIndexMin(tileRow), sqIndexMax(tileRow)):
            for indexCol in range(sqIndexMin(tileCol), sqIndexMax(tileCol)):
                if num == self.squares[indexRow][indexCol]:
                    print("\nFailure, number is in square. (placeholder)\n")    ##### Code for registering one mistake, use False boolean maybe?
                    return(False)

        print("\nSuccess, the number is not in the square area. (placeholder)\n")             ##### If no mistake, return True?
        return(True)

    def checkRow(self, num, tileRow):
        if num in self.squares[tileRow]:
            print("\nFailure, number is in the row. (placeholder)\n")
            return(False)
        else:
            print("\nSuccess, the number is not in the row. (placeholder)\n")
            return(True)

    # Method for checking for repeats of a number in a single column
    def checkCol(self, num, tileCol):
        for indexRow in range(9):
            if num == self.squares[indexRow][tileCol]:
                print("\nFailure, number is in the column. (placeholder)\n")
                return(False)

        print("\nSuccess, the number is not in the column. (placeholder)\n")
        return(True)

    # Method for placing a number
    def placeNum(self, num, tileRow, tileCol):
        print(f"\nAttempting to place number {num}...\n")
        sleep(2)

        # If check methods detect same num (return False), mistake counter goes up by 1
        if not(self.checkSquare(num, tileRow, tileCol) and self.checkRow(num, tileRow)):
            #print("Mistake + 1")
            return(False)
            #mistakeCounter(mistakes)
        else:
            self.squares[tileRow][tileCol] = num
            return(True)

    # Generates a good sudoku board at the start of the game - generate determining num for chance of generating num in sq, then check if sq num complies with .check rules
    def generateNum(self, difficulty):
        # Creates a set of nums 1-9 for each individual square area (numbering sq as 1-9 from left-right, then up-down)
        # Note that since this is in a 9x9 1d list format but squares are kept track in a 3x3 2d list format,
        #      a bit of converting between indices is necessary in order to access the right set
        #      Formula used is: "(rowIndex + 2**rowIndex - 1) + colIndex" (converts from 3x3 2d to 9x9 1d, 
        #      index var are from enumerate() for for loops below)
        numSet = [[num for num in range(1, 10)] for square in range(9)] 

        # Loop runs through 1, 4, 7 (representing squares within first, second, and third rows/columns respectively)
        for i in range(2):
            for rowIndex, row in enumerate(range(1, 6, 3)): #(1, 8, 3)
                for colIndex, col in enumerate(range(1, 8, 3)):  
                    firstRow = randint(sqIndexMin(row), sqIndexMax(row) - 1) # subtract 1 due to indexing syntax
                    firstCol = randint(sqIndexMin(col), sqIndexMax(col) - 1) # subtract 1 due to indexing syntax
                    
                    setIndex = numSet[(rowIndex + 2**rowIndex) + (colIndex + (rowIndex - 1))] ##### WORK ON EQN TO WORK WHEN ROWINDEX IS 2
                    firstChance = randint(1, 100)             # [difficulty]% chance of spawning a number in the square (win chance if num less than difficulty)

                    if firstChance < difficulty:
                        while True:
                            
                            ##### (currently trying to work on 3x3 to 9x9 converting...)  
                            firstNum = randint(setIndex[0],setIndex[-1])
                            numCheck = self.placeNum(firstNum, firstRow, firstCol)
                            
                            if numCheck:
                                setIndex.remove(firstNum)                # Taking advantage of identity trait between setIndex list and numSet nested list  
                                break
        print("Test \nBoard:")
        self.displayBoard()
        print("Sets:")

        for i, j in enumerate(numSet):
            print(f"#{i}: {j}")


        pass

#--------------------#
# Testing out methods:
if __name__ == "__main__":
    A = Board()

    A.displayBoard()

    sleep(2)

    A.generateNum(90)

    # A.displayOccur(5)

    # sleep(2)

    # print(A.checkSquare(5, 5, 5))
    # print(A.checkRow(5, 5))
    # print(A.checkCol(5, 5))