# Main module - run program from here

# Different package imports
from time import sleep

# Same package imports
from board import Sudoku
from createBoard import create
from display import Game

# Depreciated text ver. of lvl select, remove later
def levelSet():
    while True:
        choice = input("Choose what difficulty you would like to play at (safety, easy, medium, hard, asian): ")

        match choice[0].lower():
            case "s":
                print("You chose: safety.")
                return("1")
            case "e":
                print("You chose: easy.")
                return("2")
            case "m":
                print("You chose: medium.")
                return("3")
            case "h":
                print("You chose: hard.")
                return("4")
            case "a":
                print("You chose: eMoTiOnAl DaMaGe")
                return("5")
            case _: 
                print("Unrecognized input. Please input either \"safety\", \"easy\", \"medium\",      \
                       \"hard\", or \"asian\".")
                sleep(2)

def main():
    create()

    game = Game()
    game.start()

# mistakes = 0

# mistakes = mistakeCounter(mistakes)

# print(mistakes)

if __name__ == "__main__":
    main()

#Test code for displaying rows and columns (using [row][column] format)
#A.squares[0][2].display()                