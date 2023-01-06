#Web Scraping Sudoku Bot Prototype

from bs4 import BeautifulSoup
# from selenium import webdriver
import requests
import json

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# import time

# options = Options()
# options.headless = False

# # Test from documentation for selenium (chromium driver)
# driver = webdriver.Chrome()
# driver.get("https://www.sudokuweb.org/")
# assert "Sudoku" in driver.title  # Webpage tab title; makes sure webpage is correct
# elem = driver.find_elements(By.CLASS_NAME, "sedy")
# print(elem)
# elem.clear()
# # elem.send_keys("pycon")
# # elem.send_keys(Keys.RETURN)
# # assert "No results found." not in driver.page_source
# # driver.close()
# # print(elem)
# driver.close()

#Old sudoku website(sudokuweb.org)
# for rowIndex in range(9):
#     row = []
#     rowVisible = []

#     idStrR = "line"
#     if rowIndex != 0:
#         idStrR += str(rowIndex)

#     rowScrape = soup.find("tr", id = idStrR)
#     print("-rowScrape:\n", rowScrape)

#     for colIndex in range(9):
#         idStrC = "right"
#         if [rowIndex, colIndex] != [0, 0]:
#             idStrC += str(colIndex + (9 * rowIndex))

#         colScrape = rowScrape.find(id = idStrC)
#         print(f"---colScrape{idStrC}:\n", colScrape)

#         print(f"---colScrape{idStrC} Prettified:\n", colScrape.prettify())
#         if 'class="volz"' in colScrape.prettify():
#             num = colScrape.find("span", class_ = "true")
#             num = int(num.text.strip())
            
#             rowVisible.append("_")
#             row.append(num)
#         else:
#             num = colScrape.find("span")
#             num = int(num.text.strip())
            
#             rowVisible.append("*")
#             row.append(num)
    
#     board.append(row)
#     visible.append(rowVisible)

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
    # for index, elem in enumerate(results):        # ...for debugging
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
    output = {}

    for lvl in range(1, 6):
        outputLvl = []      # List holding multiple dicts, each representing info for a single board of a certain lvl

        for boardID in range(1, 6):
            outputInner = getBoard(boardID, lvl)
            outputLvl.append(outputInner)

        output[lvl] = outputLvl

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

    for boardID in range(1, 6):
        outputInner = getBoard(boardID, lvl)
        outputLvl.append(outputInner)

    database[lvl] = outputLvl

    with open("boards.json", 'w') as fh2:
        output = json.dumps(database)
        fh2.write(output)

def main():
    create()
    addFive("1")

if __name__ == "__main__":   # Running this file for debugging functions in this module
    main()
                





