# simple-sudoku-prototype
A Sudoku game prototype written in Python that utilizes simple web scraping.

## Features:
- Obtains random valid sudoku boards through webscraping a sudoku generator website (with BeautifulSoup4), compiling them into a JSON for later use
- Interactive GUI made using pygame and pygame-gui
- Five levels of difficulty available to choose from: Safety, Easy, Normal, Hard, and [Asian](https://youtu.be/miD_TWmdGIY)

## To-dos:
- [ ] Fix collision problems with deselected mistake UIButtons when attempting to select them
- [ ] Implement eraser, pause, and hint buttons during gameplay
- [ ] Implement a Game Over and Main Menu screen
- [ ] Implement hints functionality and hint button during gameplay
- [ ] Work on prettying up GUI

## Credits:
- Sudoku board source: [Sudoku9x9](http://www.sudoku9x9.com/mobile/)