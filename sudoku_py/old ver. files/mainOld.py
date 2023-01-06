# Main module - run program from here

from math import floor
from boardOld import Board, Square

# def mistakeCounter(numMistake):
#     numMistake += 1

#     if numMistake >= 3:
#         print("Game Over (placeholder code here)")
    
#     return(numMistake)

# mistakes = 0

# mistakes = mistakeCounter(mistakes)

# print(mistakes)


# def multipleOf3(num):
#     print(3 * floor(num/3))
#     print(3 * floor(num/3) + 3)

#-------------------------------------------------#

A = Board()

A.placeNum(4, 0, 0, 0, 0)

A.placeNum(4, 0, 0, 0, 0)

#Test code for iterating through for loop for squares (iterates through row, then column)
# for squareRow in A:
#     for squareCol in range(0,3):
#         squareRow[squareCol].display()
#         #print(squareRow[squareCol].tiles[0][1])

#Test code for calling .checkSquare method in Board obj
# print(A.checkSquare(4, 0, 0))

#Test code for iterating through for loop for tiles (iterates through row, then column)
for sqRow in A:
    for sqCol in range(0,3):
        sqRow[sqCol].display()
        
        for i in sqRow[sqCol].tiles:
            for j in range(3):
                print(i[j])
        

#Test code for displaying rows and columns (using [row][column] format)
A.squares[0][2].display()                