# settings.py - for any global variables/constants used in other modules, kept in one file for convenience's sake
import pygame

# ----------------#
# General Game Constants
# ----------------#
WIN_WIDTH = 1280
WIN_HEIGHT = 720      # (width, height)
TITLE = "Sudoku Game"
WIN_ICON = "img/sudoku.png"
FPS = 60

KEY_CHECK = [pygame.K_1,
             pygame.K_2,
             pygame.K_3,
             pygame.K_4,
             pygame.K_5,
             pygame.K_6,
             pygame.K_7,
             pygame.K_8,
             pygame.K_9]

DEBUG_WIN_LEFT = 340
DEBUG_WIN_TOP = 160
DEBUG_WIN_WIDTH = 600
DEBUG_WIN_LENGTH = 300
DEBUG_WIN_POS = (DEBUG_WIN_LEFT, DEBUG_WIN_TOP)
DEBUG_WIN_DIM = (DEBUG_WIN_WIDTH, DEBUG_WIN_LENGTH)

# ----------------#
# Level Select Menu Constants
# ----------------#
HEIGHT_PADDING = 10
LBTN_WIDTH = 300
LBTN_HEIGHT = 60  # Padding for top + bottom = 10 + 10
LBTN_DIM = (LBTN_WIDTH, LBTN_HEIGHT)

# Text UILabel Settings
LTITLE_TXT = "Sudoku Prototype"
LTITLE_LEFT = 0      # 0, since using centerx anchor
LTITLE_TOP = 100
LTITLE_WIDTH = 500
LTITLE_HEIGHT = 100
LTITLE_POS = (LTITLE_LEFT, LTITLE_TOP)
LTITLE_DIM = (LTITLE_WIDTH, LTITLE_HEIGHT)

LSUBTITLE_TXT = "Choose your level:"
LSUBTITLE_LEFT = 0   # 0, since using centerx anchor
LSUBTITLE_TOP = 195
LSUBTITLE_WIDTH = 200
LSUBTITLE_HEIGHT = 50
LSUBTITLE_POS = (LSUBTITLE_LEFT, LSUBTITLE_TOP)
LSUBTITLE_DIM = (LSUBTITLE_WIDTH, LSUBTITLE_HEIGHT)

# All buttons -> centered horiz., starts from vert. middle and continues downwards to bottom of screen
SAFE_BTN_LEFT = 0             # Determines alignment of all menu buttons
SAFE_BTN_TOP = 330            # Determines vert. start of col. of buttons
SAFE_BPOS = (SAFE_BTN_LEFT, SAFE_BTN_TOP)

EASY_BTN_LEFT = SAFE_BTN_LEFT
EASY_BTN_TOP = SAFE_BTN_TOP + (LBTN_HEIGHT + HEIGHT_PADDING)
EASY_BPOS = (EASY_BTN_LEFT, EASY_BTN_TOP)

MED_BTN_LEFT = EASY_BTN_LEFT
MED_BTN_TOP = EASY_BTN_TOP + (LBTN_HEIGHT + HEIGHT_PADDING)
MED_BPOS = (MED_BTN_LEFT, MED_BTN_TOP)

HARD_BTN_LEFT = MED_BTN_LEFT
HARD_BTN_TOP = MED_BTN_TOP + (LBTN_HEIGHT + HEIGHT_PADDING)
HARD_BPOS = (HARD_BTN_LEFT, HARD_BTN_TOP)

ASIN_BTN_LEFT = HARD_BTN_LEFT
ASIN_BTN_TOP = HARD_BTN_TOP + (LBTN_HEIGHT + HEIGHT_PADDING)
ASIN_BPOS = (ASIN_BTN_LEFT, ASIN_BTN_TOP)

# ----------------#
# In-Game Play Constants
# ----------------#
# Sudoku Grid UIImage
GRID_IMG = "img/grid.png"
GRID_TOP = 25         # Relative to center
GRID_LEFT = 0
GRID_WIDTH = 600
GRID_LENGTH = 600
GRID_POS = (GRID_LEFT, GRID_TOP)
GRID_DIM = (GRID_WIDTH, GRID_LENGTH)

# UIProgressBar:
PBAR_TOP = 30         # Relative to top of root window
PBAR_LEFT = 0
PBAR_WIDTH = GRID_WIDTH - 100
PBAR_LENGTH = 35
PBAR_POS = (PBAR_LEFT, PBAR_TOP)
PBAR_DIM = (PBAR_WIDTH, PBAR_LENGTH)

# Left Outer Info UIPanel
# Relative to centery anchor; will add displacement later when adding more buttons underneath panel (e.g. pause btn)
INFO_PNL_TOP = -38
INFO_PNL_LEFT = 41    # Inner Panel -> + 4
INFO_PNL_WIDTH = 260  # Inner Panel -> - 8
INFO_PNL_LENGTH = 300  # Inner Panel -> - 8
INFO_PNL_POS = (INFO_PNL_LEFT, INFO_PNL_TOP)
INFO_PNL_DIM = (INFO_PNL_WIDTH, INFO_PNL_LENGTH)

# General UILabel dimensions (for labels within left info UIPanel)
PLBL_WIDTH = 210
PLBL_LENGTH = 40
PLBL_DIM = (PLBL_WIDTH, PLBL_LENGTH)

# Mode UILabel (within Left Info UIPanel)
MODE_LBL_TOP = 10
MODE_LBL_LEFT = 0     # Relative to centerx anchor (within UIPanel)
MODE_LBL_POS = (MODE_LBL_LEFT, MODE_LBL_TOP)

# Mistake Counter UILabel (within Left Info UIPanel)
MIST_LBL_TOP = 60
MIST_LBL_LEFT = 0     # Relative to centerx anchor (within UIPanel)
MIST_LBL_POS = (MIST_LBL_LEFT, MIST_LBL_TOP)

# Timer UILabel (within Left Info UIPanel)
TIMER_LBL_TOP = 110
TIMER_LBL_LEFT = 0    # Relative to centerx anchor (within UIPanel)
TIMER_LBL_POS = (TIMER_LBL_LEFT, TIMER_LBL_TOP)

# Instructions UILabel (within Left Info UIPanel)
INSTRUCT_LBL_TXT = ["Select a tile on the board, ",
                    "then type in a number or click ",
                    "the buttons to the right of ",
                    "the board to input a value."]
INSTRUCT_LBL_TOP = 160
INSTRUCT_LBL_LEFT = 0    # Relative to centerx anchor (within UIPanel)
INSTRUCT_LBL_LENGTH = 30
INSTRUCT_LBL_DIM = (PLBL_WIDTH, INSTRUCT_LBL_LENGTH)

# General UIButton dimensions (used for tile btns, side btns)
PBTN_WIDTH = 62
PBTN_LENGTH = 62
PBTN_DIM = (PBTN_WIDTH, PBTN_LENGTH)

# Side Number Select UIButton
NUM_CONFIG = [['1', '2', '3'],
              ['4', '5', '6'],
              ['7', '8', '9']]
NUM_BTN_TOP = -36.5    # relative to centery anchor
NUM_BTN_LEFT = 139  # relative to grid UIImage; x = 1079 relative to main window left anchor

# Side Image UIButton (e.g. pencil input btn, eraser delete btn, notes input btn (possibly...?))
IMG_1 = "#eraser_button"
IMG_2 = "#notes_button"
IMG_3 = "#pause_button"
IMG_4 = "#hint_button"
IMG_RCONFIG = [[IMG_1, IMG_2]]
IMG_RBTN_TOP = 100.5
# relative to grid UIImage; x = 1079 relative to main window left anchor
IMG_RBTN_LEFT = NUM_BTN_LEFT

IMG_LCONFIG = [[IMG_3, IMG_4]]
IMG_LBTN_TOP = 152
IMG_LBTN_LEFT = 0

# UIMessageDialogBox Messages
LOSE_MSG = "<body>                            \
                <p><b>You lost!</b></p>       \
            </body>"

WIN_MSG = "<body>                                  \
                   <p><b>You won the game!</b></p> \
           </body>"
