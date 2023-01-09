# simple-sudoku-prototype
A Sudoku game prototype written in Python that utilizes simple web scraping.

## Features:
- Obtains random valid sudoku boards by webscraping a sudoku generator website (with BeautifulSoup4), compiling them into a JSON for later use
- Interactive GUI made using pygame and pygame-gui
- Five levels of difficulty available to choose from: Safety, Easy, Normal, Hard, and [Asian](https://youtu.be/miD_TWmdGIY)

## To-dos:
- [ ] Fix collision problems with deselected mistake UIButtons when attempting to select them
- [ ] Add game over functionality
- [ ] Add simple keyboard support during gameplay
- [ ] Implement eraser, pause, and hint buttons during gameplay
- [ ] Implement additional screens:
  - [ ] Game Over
  - [ ] Main Menu 
- [ ] Implement hints functionality and hint button during gameplay
- [ ] Work on prettying up GUI
- [ ] Add step-by-step solving feature (game shows you how to solve board tile-by-tile, using various sudoku strategies like Hidden/Naked Singles, X-Wing, etc.)

## Credits:
- Sudoku board source: [Sudoku9x9](http://www.sudoku9x9.com/mobile/)
