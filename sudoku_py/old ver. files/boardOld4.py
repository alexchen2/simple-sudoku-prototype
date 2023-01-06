# Classes.py - stores primary classes used in main module

#Import math module for .floor and .ceil
from math import floor
from random import choice, randint, shuffle
from time import sleep

# Temp function for printing formatted lists, delete later
def printListF(list1):
    for itemIter, item in enumerate(list1):
        if itemIter % 10 == 0:
            print(item)
        else:
            print(item, end="\t")

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
        self.squares = [[0 for col in range(9)] for row in range(9)]     
        self.squareChange = [[False for col in range(9)] for row in range(9)]   # determines whether a square has been modified or not (True = yes, False = no)

        self.mistakes = 0
    
    # Iterates through the squares in Board (increments column first, then row)
    def __iter__(self):                       #(is this really necessary...?)
        return(iter(self.squares))

    # Temp until I implement GUI
    def __str__(self):
        output = "╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗\n"

        for tileRow in self:
            output += "║"

            for tileSlot, tileNum in enumerate(tileRow):
                if tileSlot in [2, 5]:
                    if tileNum != 0:
                        output += f"\033[1;30;47m {tileNum} \033[0;0m║"
                    else:
                        output += f" {tileNum} ║"
                elif tileSlot != 8:
                    if tileNum != 0:
                        output += f"\033[1;30;47m {tileNum} \033[0;0m│"
                    else:
                        output += f" {tileNum} │"
                else:
                    if tileNum != 0:
                        output += f"\033[1;30;47m {tileNum} \033[0;0m"
                    else:
                        output += f" {tileNum} "
            
            output += "║\n"
            
            if tileRow is self.squares[2] or tileRow is self.squares[5]:
                output += "╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣\n"
            elif tileRow is not self.squares[-1]:
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
        if self.checkSquare(num, tileRow, tileCol) and self.checkRow(num, tileRow) and self.checkCol(num, tileCol):
            self.squares[tileRow][tileCol] = num
            #print("Mistake + 1")
            return True
            #mistakeCounter(mistakes)
        else:
            
            return False

    # Generates a good sudoku board at the start of the game - generate determining num for chance of generating num in sq, then check if sq num complies with .check rules
    def generateNum(self, 
                    difficulty, 
                    index = [(row, col) for row in range(9) for col in range(9)],           # Coords of each tile stored in a tuple, all within a list
                    numSet = [num for num in range(1, 10)],                                 # Available nums to place (unique to each iteration of function)
                    numSetIter = [num for num in range(1, 10)]):                            # numSet, but no changes are made until calling next iteration (as such, mainly used as iterable in loops)
        
        """
        (ver.5) Generates an already valid sudoku format, then shuffles it randomly to create a new board.

        Currently working on ver. 6 (uses ver. 4 code, but implements recursion with sudoku solver)
        """

        # ver. 5: (Mentioned above in docstring)
        # Note: This version still works, but boards formed are generally predictable. Therefore, ver. 6 is being made in hopes of achieving more randomness
        
        # boardFull = [[(num % 9) + 1 for num in range(row, row + 9)] for rowIncr in range(3) for row in range(rowIncr + 1, rowIncr + 8, 3)]
        
        # # Shuffling algorithm; repeats twice with original boardFull and boardFull rotated 90 degrees
        # for shuffleBoard in range(2):
        #     # For temporarily storing groups of 3 rows in boardFull and shuffling them WITHOUT BREAKING SUDOKU RULES
        #     boardRows = []

        #     # Adds rows of 3 as 1 element to boardRows, then shuffles the 3 rows within each group
        #     for smthNum, smth in enumerate(range(0, 7, 3)):
        #         boardRows.append(boardFull[smth:smth + 3])
        #         print(boardRows[smthNum])
        #         shuffle(boardRows[smthNum])
        #         print(boardRows[smthNum])

        #     # Shuffles all three groups of 3 rows, just for good measure
        #     shuffle(boardRows)
        #     print(boardRows)

        #     for i, j in enumerate(range(0, 7, 3)):
        #         for k in range(3):
        #             boardFull[k + j] = boardRows[i][k]

        #     # Flip board on its side, then shuffle around again
        #     if shuffleBoard == 0:
        #         boardFull = [[boardFull[initCol][initRow] for initCol in range(9)] for initRow in range(9)]
        #         print("\n", boardFull)

        # # 


        # # Assigning values to each square of self.squares
        # for rowIndex, row in enumerate(boardFull):
        #     for numIndex, num in enumerate(row):
        #         self.placeNum(num, rowIndex, numIndex)      
        # 
        # --------------------------------------------------------------------------------------------------        

        # ver4: numSet is now not nested and shared between all 3x3 squares on the board, and each number in numSet is only removed after every
        # square contains a copy of that number.

        # numSet = [num for num in range(1, 10)]
        # numSetIter = numSet[:]
        # #numSetCoord = [(row, column) for row in range(3) for column in range(3)]    # for indexing numSet and square areas in board


        # ### INITIAL RANDOM NUMBERS GENERATOR ###
        # # Loop runs through 1, 4, 7 (representing squares within first, second, and third rows/columns respectively)
        # for placeNum in numSetIter:
        #     for row in range(1, 8, 3): 
        #         for col in range(1, 8, 3):  
        #             #setIndex = numSet[numSetCoord.index((rowIndex, colIndex))]
        #             while True:
        #                 randRow = randint(sqIndexMin(row), sqIndexMax(row) - 1) # subtract 1 due to indexing syntax
        #                 randCol = randint(sqIndexMin(col), sqIndexMax(col) - 1) # subtract 1 due to indexing syntax
                        
        #                 if self.squares[randRow][randCol] == 0:
        #                     numCheck = self.placeNum(placeNum, randRow, randCol)
        #                 else:
        #                     numCheck = False
        #                 #self.squareChange[firstRow][firstCol] = False     ##### Might apply when hiding certain percentage of board later
                        
        #                 if numCheck:
        #                     print(f"Successfully placed {placeNum} at {randRow}, {randCol}.")
        #                     self.displayBoard()                        
        #                     break
            
        #     numSet.remove(placeNum)                # Taking advantage of identity trait between setIndex list and numSet nested list          
                    
        # ---------------------------------------------------------------------------------------------------------
        # ver. 6: Implement ver. 4 code, but with recursion and backtracking

        #numSetCoord = [(row, column) for row in range(3) for column in range(3)]    # for indexing numSet and square areas in board


        ### INITIAL RANDOM NUMBERS GENERATOR ###
        # Loop runs through 1, 4, 7 (representing squares within first, second, and third rows/columns respectively)
        randIndex = choice(index)
        randRow = randIndex[0] # subtract 1 due to indexing syntax
        randCol = randIndex[1] # subtract 1 due to indexing syntax
        numCount = 0               # Number of times num appears in board
        endLoop = False

        index.remove(randIndex)
        #Debugging below:
        printListF(index)
        # sleep(0.05)

        for placeNum in numSetIter:
        # for row in range(1, 8, 3): 
        #     for col in range(1, 8, 3):  
                #setIndex = numSet[numSetCoord.index((rowIndex, colIndex))]
            
            if not self.squareChange[randRow][randCol]:
                numCheck = self.placeNum(placeNum, randRow, randCol)
            # else:
            #     numCheck = False
            #self.squareChange[firstRow][firstCol] = False     ##### Might apply when hiding certain percentage of board later
            
            if numCheck:
                # print(f"Successfully placed {placeNum} at {randRow}, {randCol}.")
                self.squareChange[randRow][randCol] = True
                
                
                # Number of times num appears in board so far
                for numOccur in self:
                    if placeNum in numOccur:
                        numCount += 1

                # If the entire board is filled up, return True and end recursion loop
                if self.squareChange.count([True for i in range(9)]) == 9:
                    return True
                elif numCount == 9:                            # If number placed is in board 9 times now, remove from list of available nums to place on board
                    numSet.remove(placeNum)

                
                
                # numSet is used also for numSetIter to prevent any used up nums from being looped over and placed in blank tiles
                # print(self)
                # sleep(1)
                endLoop = self.generateNum(difficulty, index, numSet, numSet)                # Places num in another spot, and determines whether or not board is finally finished placing nums or if next spot cannot place any nums 
            
            else:
                
                if placeNum == numSetIter[-1]:                 # If NO numbers in arsenal can be fit into slot, return False to previous iteration's endLoop
                    # print("Medium Failure (go back 1 tile!)")
                    self.squareChange[randRow][randCol] = False
                    self.squares[randRow][randCol] = 0             # Resets current tile back to 0 (just in case!)
                    index.append(randIndex)                    # Adds index coord. back to list of available indices
                    #Debugging below:
                    # printListF(index)
                    # printListF(self.squareChange)
                    # sleep(0.10)
                    return False 
                # else:
                    # print("Mini Failure (num doesn't work!)")
                    
                
            if endLoop:                                        # If board is finally finished, continue returning True to previous iteration's endLoop 
                return True
            else:                                              # If next iteration was not able to place a num, then:                
                if placeNum not in numSet:                     # If current iter num was 9th one placed, then readds num to numSet
                    numSet.append(placeNum)

                if placeNum == numSetIter[-1]:                 # If next iter cannot work and current iter num is 9, then return False to previous iteration's endLoop
                    # print("Medium Failure (go back 2+ tiles!)")
                    self.squares[randRow][randCol] = 0         # Resets current tile back to 0
                    self.squareChange[randRow][randCol] = False
                    # sleep(1)
                    index.append(randIndex)                    # Adds current index coord. back to list of available indices
                    #Debugging below:
                    # printListF(index)
                    # printListF(self.squareChange)
                    # sleep(0.25)
                    return False 
                
                

                # self.displayBoard()                        
                # break
        
        

            # numSet.remove(placeNum)        
        # 


        # ### GENERATE REST OF BOARD PROCEDURALLY ###
        # #...This nested shit of a structure is a monstrosity to look at; revise later
        # # for rowIndex, row in enumerate(range(1, 8, 3)): 
        # #     for colIndex, col in enumerate(range(1, 8, 3)):
        # #         iterRow = [i for i in range(sqIndexMin(row), sqIndexMax(row))]
        # #         iterCol = [j for j in range(sqIndexMin(col), sqIndexMax(col))]
        # #         setIndex = numSet[numSetCoord.index((rowIndex, colIndex))]

        # #         for i in iterRow:
        # #             for j in iterCol:
        # #                 for k in setIndex:
        # #                     if self.squares[i][j] == None:
        # #                         numCheck = self.placeNum(k, i, j)

        # #                         if numCheck:
        # #                             setIndex.remove(k)           



        # print("Test Board + Current Index:")
        # printListF(index)
        # printListF(self.squareChange)
        # print(self)

        # print("Sets:")

        # for i, j in enumerate(numSet):
        #     print(f"#{i}: {j}")
        # pass

#--------------------#
# Testing out methods:
if __name__ == "__main__":
    A = Board()

    print(A)

    sleep(2)

    test = A.generateNum(90)
    
    if test:
        print(A)
        print("Success! (probably)") 
    else:
        print(A)
        print("Failure")


    # A.displayOccur(5)

    # sleep(2)

    # print(A.checkSquare(5, 5, 5))
    # print(A.checkRow(5, 5))
    # print(A.checkCol(5, 5))