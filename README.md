# simple-sudoku-prototype
A Sudoku game prototype written in Python that utilizes simple web scraping.

## Features:
- Obtains random valid sudoku boards by webscraping a sudoku generator website (with BeautifulSoup4), compiling them into a JSON for later use
- Interactive GUI made using pygame and pygame-gui
- Five levels of difficulty available to choose from: Safety, Easy, Normal, Hard, and [Asian](https://youtu.be/miD_TWmdGIY)

## To-dos:
- [x] Fix collision problems with deselected mistake UIButtons when attempting to select them
- [x] Add game over functionality
- [x] Add simple keyboard support during gameplay
- [x] Implement additional buttons during gameplay:
  - [x] Erasing input
  - [x] Pausing gameplay (basic implementation for now, will expand on later)
  - [ ] Hints
  - [ ] Notes
- [ ] Implement additional screens:
  - [ ] Game Over
  - [ ] Main Menu 
- [ ] Implement hints functionality and hint button during gameplay
- [ ] Finish properly documenting code
- [ ] Work on prettying up GUI
- [ ] Add step-by-step solving feature (game shows you how to solve board tile-by-tile, using various sudoku strategies like Hidden/Naked Singles, etc.)

## Currently known bugs:
- Timer will continue to run in the background, even when the current game is paused
- Some tiles will randomly disappear when board is disabled after winning a game

## Credits:
- Sudoku board source: [Sudoku9x9](http://www.sudoku9x9.com/mobile/)
