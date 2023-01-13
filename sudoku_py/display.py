# display.py - all pygame and gui-related functions/classes
import pygame
import sys
import pygame_gui
from pygame_gui.core import ObjectID
from settings import *
from levelSelect import LevelSelect
from play import Play
from board import Sudoku, SudokuParser    # currently redundant
from createBoard import create
import time

class Game():
    def __init__(self):
        # Setup window and other things...
        pygame.init()

        # For switching between different screens; 0 = lvlSelect, 1 = game, etc... (expand on later)
        self.status = 0

        # Window is hidden beforehand (until Game.start() is run)
        self.screen = pygame.display.set_mode(
            (WIN_WIDTH, WIN_HEIGHT), flags=pygame.HIDDEN)
        self.title = pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.icon = pygame.image.load(WIN_ICON)
        pygame.display.set_icon(self.icon)

        # PyGameGUI UI manager + import JSON theme
        self.manager = pygame_gui.UIManager(
            (WIN_WIDTH, WIN_HEIGHT), "theme.json")

        # Other classes:
        self.sudoku = None
        self.levelSelect = LevelSelect(self.manager)
        self.play = Play(self.manager)

        self.isDebug = False
        self.debugLayerView = False
        self.debugPrompt = self.createDebugPrompt("Placeholder")
        self.debugPrompt.hide()
        self.debugPrompt.disable()

        create()

    def debugCheck(self, event):
        if event.key == pygame.K_TAB:
            # Closes previous debug prompt popup, if it is still open
            if self.debugPrompt.is_enabled:
                self.debugPrompt.kill()

            debugMsg = f"Debug mode: {not self.isDebug}\n"

            if self.isDebug:
                self.isDebug = False
                debugMsg += "\nDebug features are now disabled."
            else:
                self.isDebug = True
                debugMsg += "\nPress B during gameplay to toggle board solutions.\nPress L on any screen to toggle UIObject Layer View."

            self.debugPrompt = self.createDebugPrompt(debugMsg)

        elif event.key == pygame.K_b:
            if self.isDebug:
                if self.debugPrompt.is_enabled:
                    self.debugPrompt.kill()

                if all([self.sudoku != None, self.status == 1]):
                    debugMsg = "Board Solution:\n" + self.sudoku.getStr()
                    self.debugPrompt = self.createDebugPrompt(debugMsg, winParam = (315, 35, 650, 650))
        elif event.key == pygame.K_l:
            if self.isDebug:
                # if self.debugPrompt.is_enabled: 
                #     self.debugPrompt.kill()

                if self.debugLayerView:
                    self.debugLayerView = False
                else:
                    self.debugLayerView = True
                
                self.manager.set_visual_debug_mode(self.debugLayerView)
                # debugMsg = f"UIObject Layer Toggle View: {self.debugLayerView}"
                # self.debugPrompt = self.createDebugPrompt(debugMsg)

    def createDebugPrompt(self, msg: str, winParam = (DEBUG_WIN_POS, DEBUG_WIN_DIM)):
        output = pygame_gui.windows.UIMessageWindow(pygame.Rect(winParam),
                                                html_message=msg,
                                                manager=self.manager,
                                                object_id=ObjectID(class_id="@display_msg_box",
                                                                    object_id="#debug_message"),
                                                window_title="Debug")

        return output

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
                elif event.type == pygame.KEYDOWN:   # Debug mode - press tab to enable/disable
                    self.debugCheck(event)
                
                if event.type != pygame.QUIT:
                    self.status, self.sudoku = self.levelSelect.eventCheck(
                        event, self.status, self.sudoku)
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

# --------------------#
# Test/Debug
# --------------------#


def main():
    test = Game()
    test.start()


if __name__ == "__main__":
    main()
