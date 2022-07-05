import os

from tkinter import *
import random


def show_solution():
    for cell in range(len(game.board)):
        buttons[cell].configure(relief='sunken')
        if game.board[cell] == 0:
            buttons[cell].configure(text=" ")
        elif game.board[cell] == 9:
            buttons[cell].configure(text="M")
        else:
            buttons[cell].configure(text=game.board[cell])


def cord_converter(x, width):
    row = x // width
    column = x % width
    return {"row": row, "column": column}


def end_game(win):

    # print(cells_to_find[0])
    frame = Frame(root, height=100, width=100, padx=1, pady=1)
    if win:
        label = Label(frame, text="You won")
    else:
        label = Label(frame, text="You lost")
    label.grid(row=0)
    frame.grid(row=2, column=game.width //
               2 - 2, columnspan=4, rowspan=4)
    # restart = Button(frame, height=1, width=10,
    #                  # tbd
    #                  text="Restart", padx=1, pady=1, command=restat)
    # restart.grid(row=1)
    endgame = Button(frame, height=1, width=10,
                     text="Quit", padx=1, pady=1, command=root.destroy)
    endgame.grid(row=2)
    show_solution()


def hit(x, viseted=[],):
    if game.board[x] == 0:
        buttons[x].configure(text=" ")
    else:
        buttons[x].configure(text=game.board[x])
    # print(viseted)
    buttons[x].configure(relief='sunken')

    if x not in viseted:
        cells_to_find[0] -= 1
        viseted.append(x)
        if game.board[x] == 9:
            end_game(False)
        elif game.board[x] == 0:
            neighbours = get_neighbours(game.width, game.height, x)
            for neighbour in neighbours:
                hit(neighbour, viseted)
        if cells_to_find[0] == 0:
            end_game(True)

######################################


def for_button(x):
    if v.get() == 1:
        hit(x)
    else:
        if buttons[x].cget("relief") != 'sunken':
            if buttons[x].cget("bg") == "red":
                buttons[x].configure(bg="SystemButtonFace")
            else:
                buttons[x].configure(bg="red")
            print(buttons[x].cget("bg"))
    return(x)


####################################


def get_neighbours(width, height, x):
    neighbours = [x - width - 1, x -
                  width, x - width + 1, x - 1, x + 1, x + width - 1, x +
                  width, x + width + 1]
    neighbours = [i for i in neighbours if i < height*width]
    neighbours = [i for i in neighbours if i >= 0]

    if x % width == 0:

        neighbours = [i for i in neighbours if i %
                      width != width - 1]

    if x % width == width - 1:

        neighbours = [i for i in neighbours if i %
                      width != 0]

    return neighbours


class Board():
    def __init__(self, height=8, width=10, mines=8):
        self.height = height
        self.width = width
        self.mines = mines
        self.board = []
        # self.visible_board = [" " for _ in range(self.width*self.height)]

    def print_board(self, board):
        i = 1
        for cell in board:
            print(cell, end="|")
            if i % self.width == 0:
                print("\n")
            i += 1

    def create_board(self):
        board = [0 for _ in range(self.width*self.height)]
        mines = random.sample(
            [i for i in range(self.width*self.height)], self.mines)
        for mine in mines:
            board[mine] = 9
            neighbours = get_neighbours(self.width, self.height, mine)
            for neighbour in neighbours:

                if board[neighbour] != 9:
                    board[neighbour] = board[neighbour] + 1
        game.board = board

        return board


width = 10
height = 8
mines = 4
cells_to_find = [width*height - mines]

game = Board(mines=mines)

game.create_board()
print(game.board)

get_neighbours(game.width, game.height, 10)


root = Tk()

v = IntVar(root, "1")

R1 = Radiobutton(root, text="mine", value=1, variable=v
                 )
R1.grid(row=0, column=game.width)


R2 = Radiobutton(root, text="flag",  value=2, variable=v,
                 )
R2.grid(row=1, column=game.width)

buttons = []
for i in range(game.height * game.width):
    cords = cord_converter(i, game.width)
    cell = Button(root, height=1,
                  width=3, text=" ", command=lambda x=i: for_button(x))
    cell.grid(row=cords.get("row"), column=cords.get("column"))
    buttons.append(cell)
root.mainloop()
