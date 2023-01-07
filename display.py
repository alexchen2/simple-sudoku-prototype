# display.py - all pygame and gui-related functions/classes
import pygame, sys, pygame_gui
from settings import *
from levelSelect import LevelSelect
from play import Play
from board import Sudoku, SudokuParser    # currently redundant
import time

class Game():
    def __init__(self):
        # Setup window and other things...
        pygame.init()

        self.status = 0      # For switching between different screens; 0 = lvlSelect, 1 = game, etc... (expand on later)
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), flags = pygame.HIDDEN) # Window is hidden beforehand (until Game.start() is run)
        self.title = pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.icon = pygame.image.load(WIN_ICON)
        pygame.display.set_icon(self.icon)

        # PyGameGUI UI manager + import JSON theme
        self.manager = pygame_gui.UIManager((WIN_WIDTH, WIN_HEIGHT), "theme.json")

        # Other classes:
        self.sudoku = None
        self.levelSelect = LevelSelect(self.manager)
        self.play = Play(self.manager)

    # Start running the entire game; open display window
    def start(self):
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        boardChange = True
        running = True

        while running:            
            # Amount of time passed within each tick
            timeDelta = (self.clock.tick(FPS) / 1000.0)   

            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # Press X button on window
                    running = False

                    pygame.quit()
                    sys.exit()
                else:
                    self.status, self.sudoku = self.levelSelect.eventCheck(event, self.status, self.sudoku)
                    if self.sudoku != None:
                        self.play.sudoku = self.sudoku

                    self.status = self.play.eventCheck(event, self.status)

                self.manager.process_events(event)
            
            self.manager.update(timeDelta)
            self.screen.fill((255, 255, 255))

            # Determine what screen to draw now
            match self.status:
                case 0:     # levelSelect menu
                    self.levelSelect.run()
                    boardChange = True      # for rewriting sudoku board in Play module
                case 1:     # main game menu, temp functionality for now
                    if boardChange:
                        print(self.sudoku)     # for debug
                        self.play.sudoku = self.sudoku
                        self.play.run(boardChange)
                        boardChange = False
                    else:
                        self.play.run()
                case 2:     # game over screen... possibly?
                    pass
                case _:     # probably omit or use to catch unexpected cases for self.status
                    pass

            self.manager.draw_ui(self.screen)
            pygame.display.update()
            # self.clock.tick(FPS)


# def mistakeCounter(mistake):
#     mistake += 1

#     if mistake >= 3:
#         print("Game Over (code here)")
#         return(None)
#     else: 
#         return(mistake)

# num = 3

# num = mistakeCounter(num)   

# print(num)

if __name__ == "__main__":
    test = Game()
    test.start()