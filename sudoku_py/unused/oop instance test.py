class Board:
    Spaces = [[0]*9,
              [0]*9,
              [0]*9,
              [0]*9,
              [0]*9,
              [0]*9,
              [0]*9,
              [0]*9,
              [0]*9]

    def display(self):
        print(self.Spaces)

A = Board()

print(Board.Spaces)

##A.display()
##
Board.Spaces[0][1] = 1
##

print(Board.Spaces)
A.display()

print

if A.Spaces[1][4] == A.Spaces[0][4]:
    print(True)

if A.Spaces[1][4] is A.Spaces[0][4]:
    print(False) 
