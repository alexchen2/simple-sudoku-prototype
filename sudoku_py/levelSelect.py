import pygame, pygame_gui
from pygame_gui.elements import *
from pygame_gui.core import ObjectID
from settings import *
from board import Sudoku
import time

class LevelSelect():
    def __init__(self, manager):
        # Display + manager
        self.screen = pygame.display.get_surface()
        self.manager = manager

        # Buttons
        self.safeBtn = UIButton(pygame.Rect(SAFE_BPOS, LBTN_DIM),
                                            text = "Safety",
                                            manager = self.manager,
                                            object_id = ObjectID(class_id="@lvl_button",
                                                                 object_id="#safe_button"),
                                            anchors = {"centerx" : "centerx"})
        self.easyBtn = UIButton(pygame.Rect(EASY_BPOS, LBTN_DIM),
                                            text = "Easy",
                                            manager = self.manager,
                                            object_id = ObjectID(class_id="@lvl_button",
                                                                 object_id="#easy_button"),
                                            anchors = {"centerx" : "centerx"})
        self.medBtn = UIButton(pygame.Rect(MED_BPOS, LBTN_DIM),
                                            text = "Medium",
                                            manager = self.manager,
                                            object_id = ObjectID(class_id="@lvl_button",
                                                                 object_id="#medium_button"),
                                            anchors = {"centerx" : "centerx"})
        self.hardBtn = UIButton(pygame.Rect(HARD_BPOS, LBTN_DIM),
                                            text = "Hard",
                                            manager = self.manager,
                                            object_id = ObjectID(class_id="@lvl_button",
                                                                 object_id="#hard_button"),
                                            anchors = {"centerx" : "centerx"})
        self.asinBtn = UIButton(pygame.Rect(ASIN_BPOS, LBTN_DIM),
                                            text = "ASIAN",
                                            manager = self.manager,
                                            object_id = ObjectID(class_id="@lvl_button",
                                                                 object_id="#asian_button"),
                                            anchors = {"centerx" : "centerx"})
        # Font + text
        # title = pygame.image.load(LTITLE_IMG).convert()
        # self.title = UIImage(pygame.Rect(LTITLE_POS, LTITLE_DIM),
        #                      image_surface = title,
        #                      manager = self.manager,
        #                      object_id = ObjectID(class_id="@play_img",
        #                                          object_id="#grid_image"),
        #                      anchors = {"centerx" : "centerx"})
        self.title = UILabel(pygame.Rect(LTITLE_POS, LTITLE_DIM),
                             text = LTITLE_TXT,
                             manager = self.manager,
                             object_id = ObjectID(class_id="@lvl_label",
                                                  object_id="#title_label"),
                             anchors = {"centerx" : "centerx"})
        self.subtitle = UILabel(pygame.Rect(LSUBTITLE_POS, LSUBTITLE_DIM),
                                text = LSUBTITLE_TXT,
                                manager = self.manager,
                                object_id = ObjectID(class_id="@lvl_label",
                                                    object_id="#subtitle_label"),
                                anchors = {"centerx" : "centerx"})

        self.disable()
        # self.titleFont = pygame.font.Font(MENU_FONT, TITLE_FONT_SIZE)
        # self.subtitleFont = pygame.font.Font(MENU_FONT, SUBTITLE_FONT_SIZE)
        # self.title = self.titleFont.render("Sudoku Prototype", True, (0, 0, 0))
        # self.subtitle = self.subtitleFont.render("Choose your level:", True, (0, 0, 0))

    def run(self):  # Might later move contents of self.enable over to here, if self.run proves redundant in the future
        # Enable elements if not already enabled
        self.enable()

        # # Place text on screen display
        # self.screen.blit(self.title, (400, 100))
        # self.screen.blit(self.subtitle, (560, 195))
            
    def enable(self):
        # Show all elements on screen
        self.title.show()
        self.subtitle.show()
        self.safeBtn.show()
        self.easyBtn.show()
        self.medBtn.show()
        self.hardBtn.show()
        self.asinBtn.show()

        # Enable all element functionality
        self.title.enable()
        self.subtitle.enable()
        self.safeBtn.enable()
        self.easyBtn.enable()
        self.medBtn.enable()
        self.hardBtn.enable()
        self.asinBtn.enable()

    def disable(self):
        # Hide all buttons from screen
        self.title.hide()
        self.subtitle.hide()
        self.safeBtn.hide()
        self.easyBtn.hide()
        self.medBtn.hide()
        self.hardBtn.hide()
        self.asinBtn.hide()

        # Disable all button functionality
        self.title.disable()
        self.subtitle.disable()
        self.safeBtn.disable()
        self.easyBtn.disable()
        self.medBtn.disable()
        self.hardBtn.disable()
        self.asinBtn.disable()

    def eventCheck(self, event, status, sudoku = None):
        btnPress = False
        lvl = ""

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_object_id in ["#safe_button", "#easy_button", "#medium_button", "#hard_button", "#asian_button"]:
                btnPress = True
            
            match event.ui_object_id:
                case "#safe_button":
                    lvl = "1"
                case "#easy_button":
                    lvl = "2"
                case "#medium_button":
                    lvl = "3"
                case "#hard_button":
                    lvl = "4"
                case "#asian_button":
                    lvl = "5"
        # For debugging, and placeholder for future kb input functionality                    
        # elif event.type == pygame.KEYDOWN: 
        #     if event.key == pygame.K_SPACE:
        #         board = Sudoku("5")
        #         self.status = 1
        #         self.disable()
        if btnPress:
            sudoku = Sudoku(lvl)
            sudoku.getBoard()
            status = 1
            self.disable()

        return status, sudoku

if __name__ == "__main__":
    from math import floor
    print((3 * floor(7 / 3)) + 3)
    pass