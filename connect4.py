from tkinter import *
from tkinter import messagebox
from threading import Thread
from time import sleep

root = Tk()
root.title('Main Window')
root.title('Connect4')
root.geometry('640x650+300+0')
root.configure(background = 'grey11')
root.resizable(False, False)

Label(root, text = 'Connect4', bg = 'grey11', font = ('Copper Black', 55), fg = 'LightYellow').place(x = 150, y = 50)
Label(root, text = 'Player 1',bg = 'grey11', font = ('Copper Black', 22), fg = 'cyan').place(x = 30, y = 380)
Label(root, text = 'Player 2',bg = 'grey11', font = ('Copper Black', 22), fg = 'MediumPurple1').place(x = 430, y = 380)
player1_entry = Entry(root, font = 15, bg = 'grey15', fg = 'white')
player1_entry.place(x = 30, y = 430, width = 150, height = 30)
player1_entry.insert(0, 'Player 1')
player2_entry = Entry(root, font = 15, bg = 'grey15', fg = 'white')
player2_entry.place(x = 430, y = 430, width = 150, height = 30)
player2_entry.insert(0, 'Player 2')
Label(root, text = 'Time', fg = 'red', bg = 'grey11',font =  ('Copper Black', 25)).place(x = 270, y = 190)
time_var = IntVar()
time_list = [10,20,30,60,90,120,150,180]
for i in range(8):
     Radiobutton(root, text = time_list[i], variable = time_var, value = time_list[i], bg = 'grey11', fg = 'red').place(x = 30 + 75*i, y = 280)
time_var.set(30)

game = Toplevel(root)
game.withdraw()
game.title('Connect4')
game.geometry('1270x635+0+0')
game.configure(background = 'grey21')
game.resizable(False, False)

def clear_outlines():
    for i in range(6):
        for j in range(7):
            board.itemconfig(str(i)+'#'+str(j), outline = 'grey21', width = 0)

def release(event2):
    global tag_name, old_coord, column_coin_count, moved, gt, stop
    x_coordinate = event2.x
    y_coordinate = event2.y
    board.unbind('<ButtonRelease-1>')
    board.unbind('<B1-Motion>')
    if (350 <= x_coordinate <= 875) and (20 <= y_coordinate <= 490) :
        moved = not moved
        column_number = (x_coordinate - 350)//75
        column_coin_count[column_number].append(int(tag_name[0]))
        row_number = len(column_coin_count[column_number])-1
        if row_number > 5:
            column_coin_count[column_number].pop()
            board.coords(tag_name, old_coord[0], old_coord[1], old_coord[2], old_coord[3])
        else:
            board.coords(tag_name, 360+column_number*75, 415-row_number*75, 415+column_number*75, 470-row_number*75)
            add(column_number,tag_name,l)
            
            if check(l):
                for k in check(l)[1]:
                    board.itemconfig(ltn[k[0]][k[1]],  outline = 'gold', width = 6)
                stop = False
                if check(l)[0] == '1':
                    messagebox.showinfo('Congragulations', player1_entry.get()+' wins')
                else:
                    messagebox.showinfo('Congragulations', player2_entry.get()+' wins')
                return
            elif timer_flag:
                stop = False
                winner_name = (lambda tf: player1_entry.get() if tf == 1 else player2_entry.get())(timer_flag)
                messagebox.showinfo('Congragulations', winner_name+' wins')
                return
            try:
                tag_name = list_tag_name[list_tag_name.index(tag_name)+1]
            except IndexError:
                stop = False
                messagebox.showinfo('Game over Draw')
                return
            old_coord = board.coords(tag_name)
    else:
        board.coords(tag_name, old_coord[0], old_coord[1], old_coord[2], old_coord[3])
    board.bind('<B1-Motion>', move)

def move(event1):
    board.coords(tag_name, event1.x-27.5, event1.y-27.5, event1.x+27.5, event1.y+27.5)
    x_coordinate = event1.x
    y_coordinate = event1.y
    if (350 <= x_coordinate <= 874) and (20 <= y_coordinate <= 490):
        column_number = (x_coordinate - 350)//75
        row_number = 5-len(column_coin_count[column_number])
        clear_outlines()
        board.itemconfig(str(row_number)+'#'+str(column_number), outline = 'grey70', width = 6)
    else:
        clear_outlines()
    board.bind('<ButtonRelease-1>', release)

def create_widgets():
    global board, tag_name, old_coord, gt, timer_flag , stop, column_coin_count, list_tag_name, l, ltn, player1_time, player2_time, player2_entry_name, time_1, time_2, player_no, moved, change_dict
    timer_flag = 0
    stop = True
    board = Canvas(game, width = 1225, height = 490, bg = 'grey21')
    board.place(x = 20, y = 20)
    board.create_rectangle(340, 20, 885, 490, fill = 'grey45') #(x1, y1, x2, y2)
    column_coin_count = [[],[],[],[],[],[],[]]
    list_tag_name = []
    for i in range(21):
        for j in range(1,3):
            list_tag_name.append(str(j)+'_'+str(i))
    for i in range(6):
        for j in range(7):
            board.create_oval(360+j*75, 40+i*75, 415+j*75, 95+i*75, fill = 'grey21', tag = str(i)+'#'+str(j))
    tag_number_1 = 0
    board.create_oval(255, 40, 310, 95, fill = 'cyan', tags = '1_'+str(tag_number_1))
    for i in range(5):
        for j in range(4):
            tag_number_1 += 1
            board.create_oval(30+j*75, 115+i*75, 85+j*75, 170+i*75, fill = 'cyan', tags = '1_'+str(tag_number_1))
    tag_number_2 = 0
    board.create_oval(915, 40, 970, 95, fill = 'MediumPurple1', tags = '2_'+str(tag_number_2))
    for i in range(5):
        for j in range(4):
            tag_number_2 += 1
            board.create_oval(915+j*75, 115+i*75, 970+j*75, 170+i*75, fill = 'MediumPurple1', tags = '2_'+str(tag_number_2))        
    tag_name = list_tag_name[0]
    back_button = Button(game, text = 'Quit',font = 12 , command = quit_game_window, bg = 'grey45', fg = 'orange red', activebackground = 'orange red', activeforeground = 'grey45')
    back_button.place(x = 575, y = 550, width = 110, height = 55)
    player1_entry_name = player1_entry.get()
    player2_entry_name = player2_entry.get()
    player1_name_label = Canvas(game, width = 235, height = 65, bg = 'grey36')
    player1_name_label.place(x =190, y = 540)
    player1_name_label.create_text(100, 33, text = player1_entry_name, fill = 'cyan', font = 'Helvetica 20 bold')
    player2_name_label = Canvas(game, width = 235, height = 65, bg = 'grey36')
    player2_name_label.place(x = 835, y = 540)
    player2_name_label.create_text(100, 33, text = player2_entry_name, fill = 'MediumPurple1', font = 'Helvetica 20 bold')
    old_coord = board.coords(tag_name)
    time_1 = time_var.get()
    time_2 = time_var.get()
    player_no = 1
    change_dict = {1:2, 2:1}
    moved = False
    time = time_var.get()
    seconds_1 = time%60
    minutes_1 = time//60
    seconds_2 = time%60
    minutes_2 = time//60
    player1_time = Canvas(game, width = 140, height = 65, bg = 'grey18')
    player1_time.place(x = 50, y = 540)
    player1_time.create_text(70, 33, tag = 'player1_time', text = f' {minutes_1} : {seconds_1:02} ', fill = 'cyan', font = 'Helvetica 20 bold')
    player2_time = Canvas(game, width = 140, height = 65, bg = 'grey18')
    player2_time.place(x = 1070, y = 540)
    player2_time.create_text(70, 33,tag = 'player2_time' , text = f' {minutes_2} : {seconds_2:02} ', fill = 'cyan', font = 'Helvetica 20 bold')
    board.bind('<B1-Motion>', move)
    l=[]
    for i in range(6):
        l.append([])
        for j in range(7):
            l[i].append(0)
    ltn=[]
    for i in range(6):
        ltn.append([])
        for j in range(7):
            ltn[i].append(0)


def timer():
    global time_1, time_2, player_no, moved, timer_flag
    while stop:
        if player_no == 1:
            colour = 'cyan'
            player_canvas = player1_time
            other_player_canvas = player2_time
            time_ = time_1
        elif player_no == 2:
            player_canvas = player2_time
            colour = 'MediumPurple1'
            other_player_canvas = player1_time
            time_ = time_2
        if time_ >= 0:
            seconds = time_%60
            minutes = time_//60
            player_canvas.itemconfig('player'+str(player_no)+'_time', text = f' {minutes} : {seconds:02} ', fill = colour)
            other_player_canvas.itemconfig('player'+str(change_dict[player_no])+'_time', fill = colour)
            sleep(1)
            if moved:
                player_no = change_dict[player_no]
                moved = not moved
                try:
                    timer()
                except:
                    pass
            else:
                if player_no == 1:
                    time_1 -= 1
                elif player_no == 2:
                    time_2 -= 1
                try:
                    timer()
                except:
                    pass
        else:
            timer_flag = change_dict[player_no]
            return

def quit_game_window():
    global stop
    if messagebox.askyesno('Quitting game window', 'Please confirm'):
        stop = False
        game.withdraw()
        root.deiconify()

def game_window():
    root.withdraw()
    game.deiconify()
    create_widgets()
    gt = Thread(target = timer)
    gt.start()

def check(l):
    for i in range(6):
        for j in range(7):
            if j<4 and l[i][j]==l[i][j+1]==l[i][j+2]==l[i][j+3]!=0:
                if l[i][j]==1:
                    return '1',((i,j),(i,j+1),(i,j+2),(i,j+3))
                elif l[i][j]==2:
                    return '2',((i,j),(i,j+1),(i,j+2),(i,j+3))
            elif i<3 and l[i][j]==l[i+1][j]==l[i+2][j]==l[i+3][j]!=0:
                if l[i][j]==1:
                    return '1',((i,j),(i+1,j),(i+2,j),(i+3,j))
                elif l[i][j]==2:
                    return '2',((i,j),(i+1,j),(i+2,j),(i+3,j))
            elif j<4 and i<3 and l[i][j]==l[i+1][j+1]==l[i+2][j+2]==l[i+3][j+3]!=0:
                if l[i][j]==1:
                    return '1',((i,j),(i+1,j+1),(i+2,j+2),(i+3,j+3))
                elif l[i][j]==2:
                    return '2',((i,j),(i+1,j+1),(i+2,j+2),(i+3,j+3))
            elif j>2 and i<3 and l[i][j]==l[i+1][j-1]==l[i+2][j-2]==l[i+3][j-3]!=0:
                if l[i][j]==1:
                    return '1',((i,j),(i+1,j-1),(i+2,j-2),(i+3,j-3))
                elif l[i][j]==2:
                    return '2',((i,j),(i+1,j-1),(i+2,j-2),(i+3,j-3))

def add(j,tn,l):
    n=int(tn[0])
    if l[0][j]==0:
        for i in range(-1,-len(l)-1,-1):
            if l[i][j]==0:
                l[i][j]=n
                ltn[i][j]=tn
                break

def game_thread():
    board.bind('<B1-Motion>', move)

create_widgets()
gt = Thread(target = game_thread)
gt.start()

Button(root, text = 'Start Game', command = game_window, height = 3, width = 25, font = ('Copper Black', 15), bg = 'grey21', fg = 'light green').place(x = 180, y = 550)
root.mainloop()

