import random
import subprocess
import sys
from tkinter import Button, CENTER, Frame, HORIZONTAL, Label, Message, \
    messagebox, N, PhotoImage, Scale, SOLID, Tk, Toplevel


root = Tk()
root.title("Minesweeper - Aleks Angelov")
rw, rh = root.winfo_screenwidth(), root.winfo_screenheight()
rx, ry = (rw / 2) - 270, (rh / 2) - 324
root.geometry('%dx%d+%d+%d' % (540, 648, rx, ry))
root.resizable(False, False)

gamelost = PhotoImage(file="images/gamelost.gif")
gamewon = PhotoImage(file="images/gamewon.gif")
leftclick = PhotoImage(file="images/leftclick.gif")
newgame = PhotoImage(file="images/newgame.gif")
redmine_broken = PhotoImage(file="images/redmine_broken.gif")
tile_flagged = PhotoImage(file="images/tile_flagged.gif")
tile_mine_flag = PhotoImage(file="images/tile_mine_flag.gif")
tile_mine_nomine = PhotoImage(file="images/tile_mine_nomine.gif")
tile_mine = PhotoImage(file="images/tile_mine.gif")
tile_unsure = PhotoImage(file="images/tile_unsure.gif")
tile = PhotoImage(file="images/tile.gif")


class TileStruct():
    valuestatus, coverstatus = 0, 0
    """
        Legend:

        valuestatus:
        -1 - mine tile
        0 - empty tile
        1-8 - non-mine tile with 1-8 adjacent mines
        9 - first clicked tile

        coverstatus:
        -1 - opened status
        0 - default (empty) status
        1 - flagged status
        2 - unsure (?) status
    """
    value = Label()
    cover = Button()


tiles = []
for i in range(0, 18):
    tl = []
    for j in range(0, 18):
        tl.append(TileStruct())
    tiles.append(tl)

closedsafetiles, mines, time, timer_enabled, = 256, 40, -1, False

mines_left = Label(root, text="Mines left:", font=("Microsoft Sans Serif", 12))
mines_left_value = Label(root, font=("Microsoft Sans Serif", 18), anchor=N)


# Prompts the user to create a new game
def new_game_click():
    if messagebox.askyesno("New Game", "Do you really want to start a new game?"):
        root.destroy()
        subprocess.call("minesweeper.pyw", shell=True)


new_game = Button(root, image=newgame, command=new_game_click)


# Updates the time past value
def timer_tick():
    if timer_enabled:
        global time
        time += 1
        time_past_value.configure(text=time)
        root.after(1000, timer_tick)


time_past = Label(root, text="Time past:", font=("Microsoft Sans Serif", 12))
time_past_value = Label(root, text="0", font=("Microsoft Sans Serif", 18), anchor=N)

field = Frame(root)
field.place(height=518, width=518, x=12, y=119)


# Execute events when a tile is pressed/released
def leftdown(e):
    x, y = e.widget._x, e.widget._y

    if tiles[x][y].coverstatus != 1:
        new_game.config(image=leftclick)

        global timer_enabled
        if not timer_enabled:
            tiles[x][y].valuestatus = 9
            create_new_mines()


def leftup(e):
    x, y = e.widget._x, e.widget._y

    if tiles[x][y].coverstatus != 1:
        global timer_enabled
        if not timer_enabled:
            timer_enabled = True
            timer_tick()
        tiles[x][y].cover.destroy()
        tiles[x][y].coverstatus = -1

        if tiles[x][y].valuestatus == -1:
            game_lost(x, y)
        else:
            new_game.config(image=newgame)
            global closedsafetiles
            closedsafetiles -= 1
            if tiles[x][y].valuestatus == 0:
                open_tile(x, y)
            if closedsafetiles <= 0:
                game_won()


def rightdown(e):
    global mines
    x, y = e.widget._x, e.widget._y

    if tiles[x][y].coverstatus == 0:
        if mines > 0:
            tiles[x][y].cover.config(image=tile_flagged)
            tiles[x][y].coverstatus = 1

            mines -= 1
            mines_left_value.config(text=mines)
    elif tiles[x][y].coverstatus == 1:
        tiles[x][y].cover.config(image=tile_unsure)
        tiles[x][y].coverstatus = 2

        mines += 1
        mines_left_value.config(text=mines)
    else:
        tiles[x][y].cover.config(image=tile)
        tiles[x][y].coverstatus = 0

        # Generates the 16x16 game field

def create_new_field():
    mines_left.place(height=48, width=96, x=9, y=9)
    mines_left_value.place(height=48, width=96, x=9, y=54)
    new_game.place(height=96, width=96, x=225, y=12)
    time_past.place(height=48, width=96, x=431, y=9)
    time_past_value.place(height=48, width=96, x=431, y=54)

    for i1 in range(0, 18):
        tiles[i1][0].coverstatus = -1
        tiles[i1][17].coverstatus = -1
    for j1 in range(1, 17):
        tiles[0][j1].coverstatus = -1
        tiles[17][j1].coverstatus = -1

    l, t = 0, 0

    for i1 in range(1, 17):
        for j1 in range(1, 17):
            tiles[i1][j1].value = Label(field, font=("Consolas", 20, "bold"), bd=1, relief=SOLID)
            tiles[i1][j1].value.place(height=32, width=32, x=l, y=t)

            tiles[i1][j1].cover = Button(field, image=tile, bd=1)
            tiles[i1][j1].cover.bind("<ButtonPress-1>", leftdown)
            tiles[i1][j1].cover.bind("<ButtonRelease-1>", leftup)
            tiles[i1][j1].cover.bind("<ButtonPress-3>", rightdown)
            tiles[i1][j1].cover._x = i1
            tiles[i1][j1].cover._y = j1
            tiles[i1][j1].cover.place(height=32, width=32, x=l, y=t)

            l += 32

        l = 0
        t += 32

        # Populates the game field with mines

def create_new_mines():
    m = mines

    while m > 0:
        x = random.randint(1, 16)
        y = random.randint(1, 16)
        if tiles[x][y].valuestatus == 0:
            tiles[x][y].valuestatus = -1
            m -= 1

    for i1 in range(1, 17):
        for j1 in range(1, 17):
            if tiles[i1][j1].valuestatus != -1:
                tiles[i1][j1].valuestatus = 0
                if tiles[i1 - 1][j1 - 1].valuestatus == -1:
                    tiles[i1][j1].valuestatus += 1
                if tiles[i1 - 1][j1].valuestatus == -1:
                    tiles[i1][j1].valuestatus += 1
                if tiles[i1 - 1][j1 + 1].valuestatus == -1:
                    tiles[i1][j1].valuestatus += 1
                if tiles[i1][j1 - 1].valuestatus == -1:
                    tiles[i1][j1].valuestatus += 1
                if tiles[i1][j1 + 1].valuestatus == -1:
                    tiles[i1][j1].valuestatus += 1
                if tiles[i1 + 1][j1 - 1].valuestatus == -1:
                    tiles[i1][j1].valuestatus += 1
                if tiles[i1 + 1][j1].valuestatus == -1:
                    tiles[i1][j1].valuestatus += 1
                if tiles[i1 + 1][j1 + 1].valuestatus == -1:
                    tiles[i1][j1].valuestatus += 1

            if tiles[i1][j1].valuestatus > 0:
                tiles[i1][j1].value.config(text=tiles[i1][j1].valuestatus)
                if tiles[i1][j1].valuestatus == 1:
                    tiles[i1][j1].value.config(foreground="blue")
                elif tiles[i1][j1].valuestatus == 2:
                    tiles[i1][j1].value.config(foreground="darkgreen")
                elif tiles[i1][j1].valuestatus == 3:
                    tiles[i1][j1].value.config(foreground="red")
                elif tiles[i1][j1].valuestatus == 4:
                    tiles[i1][j1].value.config(foreground="purple")
                elif tiles[i1][j1].valuestatus == 5:
                    tiles[i1][j1].value.config(foreground="brown")
                elif tiles[i1][j1].valuestatus == 6:
                    tiles[i1][j1].value.config(foreground="cyan")
                elif tiles[i1][j1].valuestatus == 7:
                    tiles[i1][j1].value.config(foreground="black")
                elif tiles[i1][j1].valuestatus == 8:
                    tiles[i1][j1].value.config(foreground="gray")


# Executes if a game is lost
def game_lost(x, y):
    new_game.config(image=gamelost)
    tiles[x][y].value.config(image=redmine_broken)
    global timer_enabled
    timer_enabled = False

    for i1 in range(1, 17):
        for j1 in range(1, 17):
            if tiles[i1][j1].coverstatus != -1:
                if tiles[i1][j1].valuestatus == -1:
                    if tiles[i1][j1].coverstatus == 1:
                        tiles[i1][j1].cover.config(image=tile_mine_flag)
                    else:
                        tiles[i1][j1].cover.config(image=tile_mine)
                else:
                    if tiles[i1][j1].coverstatus == 1:
                        tiles[i1][j1].cover.config(image=tile_mine_nomine)

    if messagebox.askyesno("Game Lost", "Sorry, you lost this game. Do you want to start a new one?"):
        root.destroy()
        subprocess.call("minesweeper.pyw", shell=True)
    else:
        sys.exit()


# Executes if a game is won
def game_won():
    new_game.config(image=gamewon)
    global timer_enabled
    timer_enabled = False

    mines_num = 0
    mines_left_value.config(text=mines_num)

    for i1 in range(1, 17):
        for j1 in range(1, 17):
            if tiles[i1][j1].coverstatus != -1 and tiles[i1][j1].coverstatus != 1:
                tiles[i1][j1].cover.config(image=tile_mine)

    if messagebox.askyesno("Game Won", "Congratulations, you won the game!. Do you want to start a new one?"):
        root.destroy()
        subprocess.call("minesweeper.pyw", shell=True)
    else:
        sys.exit()


# Opens all empty tiles and the closest non-mine tiles, around a clicked empty
# tile
def open_tile(x, y):
    global closedsafetiles

    if tiles[x - 1][y - 1].coverstatus != -1:
        tiles[x - 1][y - 1].cover.destroy()
        tiles[x - 1][y - 1].coverstatus = -1
        closedsafetiles -= 1
        if tiles[x - 1][y - 1].valuestatus == 0:
            open_tile(x - 1, y - 1)

    if tiles[x - 1][y].coverstatus != -1:
        tiles[x - 1][y].cover.destroy()
        tiles[x - 1][y].coverstatus = -1
        closedsafetiles -= 1
        if tiles[x - 1][y].valuestatus == 0:
            open_tile(x - 1, y)

    if tiles[x - 1][y + 1].coverstatus != -1:
        tiles[x - 1][y + 1].cover.destroy()
        tiles[x - 1][y + 1].coverstatus = -1
        closedsafetiles -= 1
        if tiles[x - 1][y + 1].valuestatus == 0:
            open_tile(x - 1, y + 1)

    if tiles[x][y - 1].coverstatus != -1:
        tiles[x][y - 1].cover.destroy()
        tiles[x][y - 1].coverstatus = -1
        closedsafetiles -= 1
        if tiles[x][y - 1].valuestatus == 0:
            open_tile(x, y - 1)

    if tiles[x][y + 1].coverstatus != -1:
        tiles[x][y + 1].cover.destroy()
        tiles[x][y + 1].coverstatus = -1
        closedsafetiles -= 1
        if tiles[x][y + 1].valuestatus == 0:
            open_tile(x, y + 1)

    if tiles[x + 1][y - 1].coverstatus != -1:
        tiles[x + 1][y - 1].cover.destroy()
        tiles[x + 1][y - 1].coverstatus = -1
        closedsafetiles -= 1
        if tiles[x + 1][y - 1].valuestatus == 0:
            open_tile(x + 1, y - 1)

    if tiles[x + 1][y].coverstatus != -1:
        tiles[x + 1][y].cover.destroy()
        tiles[x + 1][y].coverstatus = -1
        closedsafetiles -= 1
        if tiles[x + 1][y].valuestatus == 0:
            open_tile(x + 1, y)

    if tiles[x + 1][y + 1].coverstatus != -1:
        tiles[x + 1][y + 1].cover.destroy()
        tiles[x + 1][y + 1].coverstatus = -1
        closedsafetiles -= 1
        if tiles[x + 1][y + 1].valuestatus == 0:
            open_tile(x + 1, y + 1)

            # Prompts the user to choose the number of mines

def choose_difficulty():
    def start():
        global closedsafetiles, mines
        mines = difficulty_scale.get()
        mines_left_value.config(text=mines)
        closedsafetiles -= mines
        difficulty_window.destroy()
        root.deiconify()

    difficulty_window = Toplevel()
    difficulty_window.title("Minesweeper - Aleks Angelov")
    difficulty_window.geometry('%dx%d+%d+%d' % (324, 150, (rw / 2 - 162), (rh / 2 - 75)))
    difficulty_window.resizable(False, False)
    difficulty_window.iconbitmap("images/minesweeper.ico")

    difficulty_info = Message(difficulty_window, justify=CENTER, text="Number of Mines (Default is 40)", width=120)
    difficulty_info.place(x=108, y=9)

    difficulty_scale = Scale(difficulty_window, orient=HORIZONTAL, from_=10, to=232, length=300)
    difficulty_scale.set(40)
    difficulty_scale.place(x=9, y=48)

    difficulty_min = Label(difficulty_window, text="10")
    difficulty_min.place(x=9, y=87)

    difficulty_max = Label(difficulty_window, text="232")
    difficulty_max.place(x=290, y=87)

    difficulty_start = Button(difficulty_window, command=start, text="Start!")
    difficulty_start.place(width=75, x=123, y=105)


root.withdraw()
root.iconbitmap("images/minesweeper.ico")

create_new_field()
choose_difficulty()

root.mainloop()
