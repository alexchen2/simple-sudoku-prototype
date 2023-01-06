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
        self.squareChange = [[True for col in range(9)] for row in range(9)]   # determines whether a square can be modified or not (True = can, False = cannot)

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
                    #print("\nFailure, number is in square. (placeholder)\n")    ##### Code for registering one mistake, use False boolean maybe?
                    return(False)

        #print("\nSuccess, the number is not in the square area. (placeholder)\n")             ##### If no mistake, return True?
        return(True)

    def checkRow(self, num, tileRow):
        if num in self.squares[tileRow]:
            #print("\nFailure, number is in the row. (placeholder)\n")
            return(False)
        else:
            #print("\nSuccess, the number is not in the row. (placeholder)\n")
            return(True)

    # Method for checking for repeats of a number in a single column
    def checkCol(self, num, tileCol):
        for indexRow in range(9):
            if num == self.squares[indexRow][tileCol]:
                #print("\nFailure, number is in the column. (placeholder)\n")
                return(False)

        #print("\nSuccess, the number is not in the column. (placeholder)\n")
        return(True)

    # Method for placing a number
    def placeNum(self, num, tileRow, tileCol):
        #print(f"\nAttempting to place number {num}...\n")
        #sleep(1)

        # If check methods detect same num (return False), mistake counter goes up by 1
        if not(self.checkSquare(num, tileRow, tileCol) and self.checkRow(num, tileRow) and self.checkCol(num, tileCol)):
            #print("Mistake + 1")
            return(False)
            #mistakeCounter(mistakes)
        else:
            self.squares[tileRow][tileCol] = num
            return(True)

    # Generates a good sudoku board at the start of the game - generate determining num for chance of generating num in sq, then check if sq num complies with .check rules
    def generateNum(self, difficulty):
        # ver3: Have 2 separate lists-one representing row, and the other being column. Another list with tuples containing each of the #s in the
        #       earlier row/column lists (in format of (0,0), like coordinates). When indexing the numSets, the index of the list with
        #       tuples should match up with the indices for the numLists, so just find the index for the correct square coordinates
        #       and use that index in getting the correct numSet. (reference OneNote doc for visual help)

        numSet = [[num for num in range(1, 10)] for square in range(9)] 
        numSetCoord = [(row, column) for row in range(3) for column in range(3)]    # for indexing numSet and square areas in board


        ### INITIAL RANDOM NUMBERS GENERATOR ###
        # Loop runs through 1, 4, 7 (representing squares within first, second, and third rows/columns respectively)
        for i in range(2):           # Max 4 random numbers per square
            for rowIndex, row in enumerate(range(1, 8, 3)): 
                for colIndex, col in enumerate(range(1, 8, 3)):  
                    firstRow = randint(sqIndexMin(row), sqIndexMax(row) - 1) # subtract 1 due to indexing syntax
                    firstCol = randint(sqIndexMin(col), sqIndexMax(col) - 1) # subtract 1 due to indexing syntax
                    setIndex = numSet[numSetCoord.index((rowIndex, colIndex))]
                    
                    while True:
                        firstNum = randint(setIndex[0],setIndex[-1])
                        numCheck = self.placeNum(firstNum, firstRow, firstCol)
                        #self.squareChange[firstRow][firstCol] = False     ##### Might apply when hiding certain percentage of board later
                        
                        if numCheck:
                            setIndex.remove(firstNum)                # Taking advantage of identity trait between setIndex list and numSet nested list  
                            break

        ### GENERATE REST OF BOARD PROCEDURALLY ###
        #...This nested shit of a structure is a monstrosity to look at; revise later
        for rowIndex, row in enumerate(range(1, 8, 3)): 
            for colIndex, col in enumerate(range(1, 8, 3)):
                iterRow = [i for i in range(sqIndexMin(row), sqIndexMax(row))]
                iterCol = [j for j in range(sqIndexMin(col), sqIndexMax(col))]
                setIndex = numSet[numSetCoord.index((rowIndex, colIndex))]

                for i in iterRow:
                    for j in iterCol:
                        for k in setIndex:
                            if self.squares[i][j] == None:
                                numCheck = self.placeNum(k, i, j)

                                if numCheck:
                                    setIndex.remove(k)           



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