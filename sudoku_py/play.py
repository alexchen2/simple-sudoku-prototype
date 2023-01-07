# play.py - Code here for main game display class
import pygame
import pygame_gui
from pygame_gui.elements import *
from pygame_gui.core import ObjectID
from settings import *
from board import Sudoku, sqIndexMin, sqIndexMax
import time

# note: UIPanels seem to be broken; UIButtons within them lose their click functionality, for some reason;
#       therefore, this window was designed with everything situated on top of the root window (layer #1).


class Play():
    def __init__(self, manager):
        # Obligatory display screen + manager
        self.screen = pygame.display.get_surface()
        self.manager = manager
        self.sudoku = None
        self.mode = None
        self.startTime = 0

        # Sudoku grid (just an image with the self.tileBtns overlaid on top of it)
        grid = pygame.image.load(GRID_IMG).convert()
        self.grid = UIImage(pygame.Rect(GRID_POS, GRID_DIM),
                            image_surface=grid,
                            manager=self.manager,
                            object_id=ObjectID(class_id="@play_img",
                                               object_id="#grid_image"),
                            anchors={"center": "center"})

        # WIP progress bar to show progress of current game
        # placeholder value; number of currently correct HIDDEN, interactable tiles on the board
        self.correctTiles = 0
        # placeholder value; number of total HIDDEN, interactable tiles on the board
        self.totalTiles = 1
        self.pBar = UIProgressBar(pygame.Rect(PBAR_POS, PBAR_DIM),
                                  manager=self.manager,
                                  object_id=ObjectID(class_id="@play_pbar",
                                                     object_id="#progress_bar"),
                                  anchors={"centerx": "centerx"})
        self.pBar.set_current_progress(0.00)
        self.pBar.status_text = lambda: f"Progress: {self.pBar.current_progress:0.2f}%"

        nums = [str(num) for num in range(1, 10)]
        self.numBtns = [self.createSideBtn(num, index, len(nums) - 1, NUM_BTN_LEFT)
                        for index, num in enumerate(nums)]

        # Middle Button Contents + Variables
        # Initial placeholder value for tileBtns, until receiving board info
        self.tileBtns = {"N/A": UIButton(pygame.Rect((0, 0), (0, 0)),
                                         text="",
                                         manager=self.manager,
                                         object_id=ObjectID(class_id="@play_tile_btn",
                                                            object_id="#null"))}

        # Variable to store the currently selected button in order for its text to be modified
        self.selectedBtn = UIButton(pygame.Rect((0, 0), (0, 0)),
                                    text="",
                                    manager=self.manager,
                                    object_id=ObjectID(class_id="@play_tile_btn",
                                                       object_id="#null"))
        # (Row, Col.) of currently selected button on the sudoku board
        # Placeholder, replace if causing problems
        self.selectedCoords = (0, 0)
        self.mistakes = 0
        # Stores overlaid "#wrong_button" UIButtons; if length goes over 5 (or 3), then game over
        self.wrongBtns = {}

        # Left Info Panel Contents
        self.infoPanelOut = UIPanel(pygame.Rect(INFO_PNL_POS, INFO_PNL_DIM),
                                    manager=self.manager,
                                    object_id=ObjectID(class_id="@play_pnl",
                                                       object_id="#info_panel"),
                                    anchors={"centery": "centery",
                                             "left": "left"})

        self.infoPanelIn = UIPanel(pygame.Rect((INFO_PNL_LEFT + 4, INFO_PNL_TOP),
                                               (INFO_PNL_WIDTH - 8, INFO_PNL_LENGTH - 8)),
                                   manager=self.manager,
                                   object_id=ObjectID(class_id="@play_pnl",
                                                      object_id="#info_panel"),
                                   anchors={"centery": "centery",
                                            "left": "left"})

        # Put in list to save typing space below
        self.infoPanel = [self.infoPanelOut, self.infoPanelIn]

        self.modeLbl = UILabel(pygame.Rect(MODE_LBL_POS, PLBL_DIM),
                               text=f"Mode: {self.mode}",
                               container=self.infoPanelIn,
                               manager=self.manager,
                               object_id=ObjectID(class_id="@play_label",
                                                  object_id="#mode_label"),
                               anchors={"centerx": "centerx",
                                        "centerx_target": self.infoPanelIn})

        self.mistakeLbl = UILabel(pygame.Rect(MIST_LBL_POS, PLBL_DIM),
                                  text=f"Mistakes: {str(self.mistakes)} / 5",
                                  container=self.infoPanelIn,
                                  manager=self.manager,
                                  object_id=ObjectID(class_id="@play_label",
                                                     object_id="#mistake_label"),
                                  anchors={"centerx": "centerx",
                                           "centerx_target": self.infoPanelIn})

        self.timerLbl = UILabel(pygame.Rect(TIMER_LBL_POS, PLBL_DIM),
                                text=f"Time: 00:00:00:00",       # Format = hr:min:sec:millisec
                                container=self.infoPanelIn,
                                manager=self.manager,
                                object_id=ObjectID(class_id="@play_label",
                                                   object_id="#timer_label"),
                                anchors={"centerx": "centerx",
                                         "centerx_target": self.infoPanelIn})

        self.QuitBtn = UIButton(pygame.Rect((10, 10), (100, 50)),
                                text="Quit Game",
                                manager=self.manager,
                                object_id=ObjectID(class_id="@play_menu_btn",
                                                   object_id="#quit_button"))

        self.disable()

    def run(self, boardChange=False):
        if boardChange:
            match self.sudoku.level:
                case "1":
                    self.mode = "Safety"
                case "2":
                    self.mode = "Easy"
                case "3":
                    self.mode = "Medium"
                case "4":
                    self.mode = "Hard"
                case "5":
                    self.mode = "Asian"
            self.modeLbl.set_text(f"Mode: {self.mode}")
            
            self.mistakes = 0
            self.mistakeLbl.set_text(f"Mistakes: {str(self.mistakes)} / 5")

            self.tileBtns = {(row, col): self.createTileBtn(self.sudoku, row, col)
                             for col in range(9) for row in range(9)}
            self.totalTiles = sum(
                1 for btn in self.tileBtns.values() if "#hidden_button" in btn.object_ids)
            self.correctTiles = 0

            self.startTime = pygame.time.get_ticks()

        time = self.timer()
        self.timerLbl.set_text(f"Time: {time}")
        self.checkProgress()
        self.enable()

    def enable(self):
        # Show all elements on screen + enable all functionality
        for coord in self.tileBtns:
            # if "#shown_button" in self.tileBtns[coord].object_ids:     # Not needed, probably...
            if coord not in self.wrongBtns:       # If tileBtn currently not overlaid by a "#mistake_button"
                self.tileBtns[coord].show()
                self.tileBtns[coord].enable()

        for btn in self.numBtns:
            btn.enable()
            btn.show()

        for uipanel in self.infoPanel:
            uipanel.show()
            uipanel.enable()

        self.pBar.show()
        self.pBar.enable()
        self.grid.show()
        self.QuitBtn.show()
        self.QuitBtn.enable()

    def disable(self):
        # Hide all buttons from screen + disable all button functionality
        for coord in self.tileBtns:
            self.tileBtns[coord].disable()
            self.tileBtns[coord].hide()

        for btn in self.numBtns:
            btn.disable()
            btn.hide()

        if len(self.wrongBtns) > 0:
            tempList = []
            for coord in self.wrongBtns:
                tempList.append(coord)

            for coord in tempList:
                self.wrongBtns[coord].kill()
                del (self.wrongBtns[coord])

        for uipanel in self.infoPanel:
            uipanel.hide()
            uipanel.disable()

        self.pBar.hide()
        self.pBar.disable()
        self.grid.hide()
        self.grid.disable()
        self.QuitBtn.hide()
        self.QuitBtn.disable()

    def createTileBtn(self, sudoku: Sudoku, row, col):
        """
        Function that creates and returns a button located within the sudoku grid UIImage,
        given information from the current sudoku board.
        """
        objID = "#shown_button"
        num = sudoku.visible[row][col]

        if num == "*":
            objID = "#hidden_button"
            num = " "

        # x-coord of button = (eq relative to center anchor) + (displacement due to grid thick bars)
        x = (-260 + (65 * col)) + (-6 + sqIndexMax(col))
        # y-coord of button = same as x-coord, but for rows
        y = (-260 + (65 * row)) + (-6 + sqIndexMax(row)) + (GRID_TOP - 1)

        button = UIButton(pygame.Rect((x, y), PBTN_DIM),
                          text=num,
                          manager=self.manager,
                          object_id=ObjectID(class_id="@play_tile_btn",
                                             object_id=objID),
                          anchors={"center": "center",
                                   "center_target": self.grid})

        return button

    def createSideBtn(self, txtContent, btnIndex, maxNumBtns, yCoord, imgContent=None, isImage=False):
        """
        Function that creates and returns a button located to the side of the sudoku grid UIImage,
        whether that be a number or image button.
        """
        x = yCoord
        y = (-(maxNumBtns // 2) * 65) + (65 * btnIndex)
        pos = (x, y)

        if isImage:
            button = UIButton(pygame.Rect(pos, PBTN_DIM),
                              text=" ",
                              manager=self.manager,
                              object_id=ObjectID(class_id="@play_side_btn",
                                                 object_id="#img_button"),
                              anchors={"left": "left",
                                       "left_target": self.grid,
                                       "centery": "centery"})

            button.set_image = imgContent
        else:
            button = UIButton(pygame.Rect(pos, PBTN_DIM),
                              text=txtContent,
                              manager=self.manager,
                              object_id=ObjectID(class_id="@play_side_btn",
                                                 object_id="#num_button"),
                              anchors={"left": "left",
                                       "left_target": self.grid,
                                       "centery": "centery"})

        return button

    # WIP
    def placeNum(self, inputNum):
        if not (self.selectedBtn.is_selected and
                (self.tileBtns[self.selectedCoords] == self.selectedBtn  # Case where "#hidden_button" was selected
                 or self.selectedCoords in self.wrongBtns)):             # Case where "#wrong_button" was selected
            # ...maybe replace "or" in above conditional with bitwise or? (^)
            return

        row = self.selectedCoords[0]
        col = self.selectedCoords[1]
        # By this point, self.sudoku should not have a value of None
        answer = self.sudoku.answer[row][col]

        if inputNum == answer:
            # if self.tileBtns[self.selectedCoords] == self.selectedBtn:  # Remove this conditional clause later
            #     self.selectedBtn.set_text(inputNum)

            #     self.correctTiles += 1

            if self.selectedCoords in self.wrongBtns:
                self.wrongBtns[self.selectedCoords].kill()
                del (self.wrongBtns[self.selectedCoords])

                self.selectedBtn = self.tileBtns[self.selectedCoords]
                self.selectedBtn.enable()
                self.selectedBtn.show()
                self.selectedBtn.select()

            self.selectedBtn.set_text(inputNum)

            self.correctTiles += 1

            # progress = round(self.correctTiles / self.totalTiles, 1)
            # self.pBar.set_current_progress(progress)
        else:
            # Case A: selected btn is a "#hidden_button":
            if self.tileBtns[self.selectedCoords] == self.selectedBtn:
                # Overlay a selected "#wrong_button" UIButton on top of original button
                # same x/y-coord formulas as in self.createTileBtn
                x = (-260 + (65 * col)) + (-6 + sqIndexMax(col))
                y = (-260 + (65 * row)) + \
                    (-6 + sqIndexMax(row)) + (GRID_TOP - 1)
                wrongButton = UIButton(pygame.Rect((x, y), PBTN_DIM),
                                       text=inputNum,
                                       starting_height=2,
                                       manager=self.manager,
                                       object_id=ObjectID(class_id="@play_tile_btn",
                                                          object_id="#wrong_button"),
                                       anchors={"center": "center",
                                                "center_target": self.grid})
                wrongButton.select()
                self.wrongBtns[self.selectedCoords] = wrongButton

                # If selected btn initially had a correct ans before change, then deduct # of correct tiles (for progress bar)
                if self.selectedBtn.text == answer and self.correctTiles != 0:
                    self.correctTiles -= 1

                self.selectedBtn.set_text(" ")
                self.selectedBtn.unselect()
                self.selectedBtn.disable()
                self.selectedBtn.hide()

                self.selectedBtn = wrongButton

            # Case B: selected btn is already a "#wrong_button":
            elif self.selectedCoords in self.wrongBtns:
                self.selectedBtn.set_text(inputNum)

            # Update num of mistakes and mistake counter
            self.mistakes += 1
            self.mistakeLbl.set_text(f"Mistakes: {str(self.mistakes)} / 5")

        self.checkProgress()

    def checkProgress(self):
        """
        Checks the current progress of the game; specifically, if the user either has made more than 
        five mistakes (a loss) or has correctly filled out all of the hidden interactable tiles on the 
        board (a win). If either condition checks True, then the game ends and the window transitions 
        to the Game End/Game Over screen (WIP).
        """
        progress = round((self.correctTiles / self.totalTiles) * 100, 2)
        self.pBar.set_current_progress(progress)
        self.pBar.status_text = lambda: f"Progress: {self.pBar.current_progress:0.2f}%"

    def timer(self):
        currentTicks = pygame.time.get_ticks() - self.startTime

        # Time calculation
        millisec = currentTicks % 1000
        secs = int((currentTicks / 1000) % 60) 
        mins = int((currentTicks / 60000) % 60)
        hrs = int((currentTicks / 3600000)) 
        time = f"{hrs:02d}:{mins:02d}:{secs:02d}:{millisec:03d}"    # Any time over
        
        return time

    def eventCheck(self, event, status):
        """
        Checks for any user input, and acts accordingly.
        """
        # For debugging purposes
        if event.type == pygame.KEYDOWN:
            pass

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_object_id == "#quit_button":
                status = 0
                self.disable()

            elif event.ui_object_id == "#hidden_button":
                if event.ui_element.is_selected:
                    event.ui_element.unselect()
                    # event.ui_element.set_text(" ")
                else:
                    for coord in self.tileBtns:
                        self.tileBtns[coord].unselect()

                    if len(self.wrongBtns) > 0:
                        for coord in self.wrongBtns:
                            self.wrongBtns[coord].unselect()

                    event.ui_element.select()
                    self.selectedBtn = event.ui_element

                    # Get selected btn's coordinates
                    if self.selectedBtn in self.tileBtns.values():
                        # Will only ever have one element inside, since all btns are unique
                        tempKeys = [
                            key for key in self.tileBtns if self.tileBtns[key] == self.selectedBtn]
                    elif self.selectedBtn in self.wrongBtns.values():
                        tempKeys = [
                            key for key in self.wrongBtns if self.wrongBtns[key] == self.selectedBtn]

                    self.selectedCoords = tempKeys[0]

            elif event.ui_object_id == "#num_button":
                inputNum = event.ui_element.text
                self.placeNum(inputNum)
                # if event.ui_element.is_selected:
                #     event.ui_element.unselect()
                # else:
                #     for btn in self.numBtns:
                #         btn.unselect()

                #     event.ui_element.select()

        elif event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
            if event.ui_object_id == "#hidden_button":
                print("Hover Test 1")
            elif event.ui_object_id == "#wrong_button":
                print("Hover Test 2")

        elif event.type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
            if event.ui_object_id == "#shown_button":
                pass

        return status


def main():
    pass


if __name__ == "__main__":
    main()
