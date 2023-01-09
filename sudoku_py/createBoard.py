# createBoard.py - stores functions for web scraping an online sudoku generator website for boards
from bs4 import BeautifulSoup
import requests
import json

# Convert format obtained from website (1d list of 81 elem) to format for this program (2d 9x9 list)
def boardConvert(string : str) -> list:
    numList = [str(i) for i in range(10)] 
    output = ["*" if i == "0" else i for i in string if i in numList]
    output = [output[0 + (9 * i):9 + (9 * i)] for i in range(9)]
    return output

# Process of obtaining info on a board
def getBoard(boardID : int = 0, lvl : str = "3"):
    # Grab html code with requests library
    url = "http://www.sudoku9x9.com/mobile/?level=" + str(lvl)
    page = requests.get(url)
    code = BeautifulSoup(page.content, "html.parser")

    results = code.find_all("script")
    # for index, elem in enumerate(results):        # ...for debugging/testing
    #     print(f"-----Index {index}: \n{elem}")

    boardInfo = (results[6]).prettify()      # Where sudoku board info is stored in html/javascript code
    boardInfo = boardInfo.replace("\n", "")
    # print(temp.prettify())
    boardInfo = boardInfo.split(";")

    # Dict structure for info pertaining to a single board
    outputInner = {
        "boardID" : boardID,
        "board" : boardConvert(boardInfo[0]),
        "answer" : boardConvert(boardInfo[1]),
        "solved" : False
    }

    return outputInner

# Creates boards.json file with 5 boards per level
def create(): #numBoards : int = 10, lvl : str = "3"):
    print("Obtaining and writing boards to JSON file...")     # for debugging purposes, remove later
    output = {}

    for lvl in range(1, 6):
        outputLvl = []      # List holding multiple dicts, each representing info for a single board of a certain lvl

        for boardID in range(1, 6):
            outputInner = getBoard(boardID, lvl)
            outputLvl.append(outputInner)

        output[lvl] = outputLvl

    output["Current Boards"] = {  # Keeps track of current boardID (values) per difficulty lvl (keys)
        '1' : 1,
        '2' : 1,
        '3' : 1,
        '4' : 1,
        '5' : 1
    }

    with open("boards.json", 'w') as fh:
        output = json.dumps(output)
        fh.write(output)

def addFive(lvl : str):
    outputLvl = []

    try:
        with open("boards.json", 'r') as fh:
            reader = fh.read()
            database = json.loads(reader)
    except FileNotFoundError:
        print("Error, check createBoard.py line 120; either something attempted to add boards before \
              .json file even existed, or something unknown happened...")
        assert True == False

    for boardID in range(1, 6):
        outputInner = getBoard(boardID, lvl)
        outputLvl.append(outputInner)

    database[lvl] = outputLvl            # Overwrite old boards with new ones
    database["Current Boards"][lvl] = 1  # Reset boardID counter

    with open("boards.json", 'w') as fh2:
        output = json.dumps(database)
        fh2.write(output)

# --------------------#
# Test/Debug
# --------------------#
def main():
    create()
    addFive("1")

if __name__ == "__main__":   
    main()
                





