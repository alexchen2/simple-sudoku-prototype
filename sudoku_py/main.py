# Main module - run program from here

# Different package imports
# from time import sleep

# Same package imports
from board import Sudoku
from createBoard import create
from display import Game

def main():
    create()

    game = Game()
    game.start()

if __name__ == "__main__":
    main()

