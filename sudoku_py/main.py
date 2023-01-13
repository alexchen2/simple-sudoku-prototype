# Main module - run program from here

# Different package imports
# from time import sleep

# Same package imports
from board import Sudoku

from display import Game

def main():
    game = Game()
    game.start()

if __name__ == "__main__":
    main()

