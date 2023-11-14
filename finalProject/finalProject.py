from email.mime import image
from shutil import move
from tkinter import *
from tkinter import filedialog, ttk
from tracemalloc import start
from turtle import update, width
from PIL import Image, ImageTk, GifImagePlugin

import time
import math
import random
import msvcrt

from threading import *
from function import *
from os import walk
from board import *
from player import *
from style import *


#Variable
#var change depend on level (Manually)

level = level1 #import the boards matrix from board.py
row = len(level) #32
column = len(level[0]) #56
WIDTH = column * 20 #1300
HEIGHT = row * 20 #850
num1 = (HEIGHT - 50) // row #vertical
num2 = (WIDTH // column)
num3 = (num1 + num2) // 5 # 10
player_imgs = []

color = 'Blue'

#widely used var
score = 0
desired_fps = 25
frame = 0
count = 0 #use for PacMan animation looping 
speed = 5
frame = 0
state = -1
start = -1
flicker_time = 0
powerup_counter = 0 
start_up = 0

eaten_ghost = [False, False, False, False]
ghost_img = []
# bonus Var

history = []
mode = 0
cheat_code = ['','','','']

flicker = False
#initial start location
#PacMan inital
PacMan = player('pacman',(row // 2) * num1 - num1, (column // 2) * num2 + (7 * num2), 0)
player.add_frame(PacMan)
player.powerup(PacMan)
direction = 0

#Ghost inital
blinky = ghost('blinky',num1 * 3, num2 * 2 + num3, 0)
ghost.add_info(blinky, "red", 0, True)
ghost.target(blinky, PacMan.x, PacMan.y)

#(row // 2) * num1 + num1, (column // 2) * num2 - num2
pinky = ghost('pinky',num1 * 3, num2 * 2 + num3, 1)
ghost.add_info(pinky, "pink", 1, True)
ghost.target(pinky, PacMan.x, PacMan.y)

inky = ghost('inky',num1 * 3, num2 * 2 + num3, 2)
ghost.add_info(inky, "blue", 2, True)
ghost.target(inky, PacMan.x, PacMan.y)

clyde = ghost('clyde',num1 * 3, num2 * 2 + num3, 3)
ghost.add_info(clyde, "orange", 3, True)
ghost.target(clyde, PacMan.x, PacMan.y)

#state of ghost
spooked_img = Image.open('ghost/powerup.png').resize((30, 30))
dead_img = Image.open('ghost/dead.png').resize((30, 30))

#Begin program
#start GUI
root =Tk()
root.title('PAC MAN')
root.configure(background= 'Black')
root.geometry('1350x800') #level 1650x800
#root.geometry('1650x800')
topFrame = Canvas(root, bg = "Black", width = WIDTH, height = HEIGHT)
topFrame.pack(padx = 200,side=LEFT)

rightFrame = Frame(root, bg = "Black", width = 50, height = HEIGHT)
rightFrame.pack(side=LEFT)

topFrame1 = Frame(rightFrame, bg = "Black", width = WIDTH // 2 + 20, height = HEIGHT // 2)
topFrame1.pack()

logoFrame = Image.open('logo/pacman.jpg').resize((WIDTH // 2 + 20, HEIGHT // 4))
logoFrame = ImageTk.PhotoImage(logoFrame)
logo = Label(topFrame1, bg = 'Black' ,image= logoFrame)
logo.image = logoFrame
logo.pack()

botFrame1 = Frame(rightFrame, bg = "Black", width = 50, height = HEIGHT // 2)
botFrame1.pack(side=LEFT)

botFrame2 = Frame(rightFrame, bg = "Black", width = 50, height = HEIGHT // 2)

#function
#draw random
def draw_random(): #sua ham nay
    global PacMan
    if PacMan.powerup == True:
        topFrame.create_oval((WIDTH % 2) + num2, 750, (WIDTH % 2) + num2, 750, outline = color, width= 15)
        

#init a board
def draw_board():
    for i in range(len(level)) :
        for j in range (len(level[i])) :
            if level[i][j] == 1 : #create normal point
                topFrame.create_oval((j* num2 + (0.5 * num2), i * num1 + (0.5 * num1), j* num2 + (0.5 * num2) , i * num1 + (0.5 * num1)), outline = "white", width = 4)
            if level[i][j] == 2 and not flicker: #create Special point
                topFrame.create_oval((j* num2 + (0.5 * num2), i * num1 + (0.5 * num1), j* num2 + (0.5 * num2) , i * num1 + (0.5 * num1)), outline = "white", width = 10)
            if level[i][j] == 3 : #create line vertical
                topFrame.create_line((j* num2 + (0.5 * num2), i * num1, j* num2 + (0.5 * num2) , i * num1 + num1), fill = color, width= 5)    
            if level[i][j] == 4 : # create line horizontal
                topFrame.create_line((j* num2 , i * num1 + (0.5 * num1), j* num2 + num2, i * num1 + (0.5 * num1)), fill = color, width= 5)  
            if level[i][j] == 5 : # create corner 1
                topFrame.create_arc((j* num2 - (num2 * 0.5) , i * num1 + (0.5 * num1), j* num2 + (0.5 * num2), i * num1 + 1.5 * num1), outline = color , width= 5, start = 0, extent = 90, style = ARC) 
            if level[i][j] == 6 : # create corner 2
               topFrame.create_arc((j* num2 + (.5 * num2) , i * num1 + (1.65 * num1), j* num2 + (1.5 * num2) , i * num1 + (.5 * num1)), outline = color , width= 5, start = 180, extent = -90, style = ARC)    
            if level[i][j] == 7 : # create corner 3 
               topFrame.create_arc((j* num2 + (num2 * 0.5) , i * num1 - (1 * num1), j* num2 + (num2 * 1.65) , i * num1 + (0.5 * num1)), outline = color , width= 5, start = 180, extent = 90, style = ARC)  
            if level[i][j] == 8 : # create corner 4
               topFrame.create_arc((j* num2 + (num2 * 0.5) , i * num1 - (0.5 * num1), j* num2 - (num2 * 0.65) , i * num1 + (0.5 * num1)), outline = color , width= 5, start = 0, extent = -90, style = ARC)  
            

            if level[i][j] == 9 : # create the white line
                topFrame.create_line((j* num2 , i * num1 + (0.5 * num1), j* num2 + num2, i * num1 + (0.5 * num1)), fill = "white", width= 2)    

# GUI function
def draw_panel():
    # First page
    play_button = Button(botFrame1, font = font ,text = "Play", command = start_game)
    play_button.pack(pady = 20)
    algorithm_text = StringVar()
    algorithms_combobox = ttk.Combobox(botFrame1, font = font,width = 20, textvariable = algorithm_text)
    algorithms_combobox['values'] = ('Depth First Search',
                                     'Breadth First Search',
                                     'Uniform Cost Search',
                                     'Greedy Search',
                                     'A-star Search')
    algorithms_combobox.current(0)
    algorithms_combobox.pack()
    solve_button = Button(botFrame1, font = font ,text = "Solve", command = root.destroy)
    solve_button.pack(pady = 20)
    exit_button = Button(botFrame1, font = font ,text = "Stop", command = root.destroy)
    exit_button.pack(pady = 20)
    exit_button = Button(botFrame1, font = font ,text = "Edit Mode", command = switch_edit_mode)
    exit_button.pack(pady = 20)
    exit_button = Button(botFrame1, font = font ,text = "Exit", command = root.destroy)
    exit_button.pack(pady = 20)

    # Second page
    confirm_button = Button(botFrame2, font = font ,text = "Confirm", command = root.destroy)
    confirm_button.pack(pady = 20)
    back_button = Button(botFrame2, font = font ,text = "Back", command = switch_main_mode)
    back_button.pack(pady = 20)
    
def switch_edit_mode():
    botFrame1.forget()
    botFrame2.pack(side=LEFT)
    
def switch_main_mode():
    botFrame2.forget()
    botFrame1.pack(side=LEFT)
    
# Core Function
#draw initil player
def draw_initial_player():
    global PacMan, state, frame, turn_allowed, blinky, pinky, inky, clyde
    PacMan.turn_allowed = check_position(PacMan)
    if PacMan.cdirection == 0: #Right
        for i in range (0, 4):  
            PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = 0)
    if PacMan.cdirection == 1: # Left
        for i in range (0, 4):
            PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = 180)    
    if PacMan.cdirection == 2: #Up
        for i in range (0, 4):  
            PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = 90)
    if PacMan.cdirection == 3: #Down
        for i in range (0, 4):  
            PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = -90)
            
    update_player(frame)
      
# change the direction of the Pacman
def change_direction_player(): 
    global PacMan, state, frame, direction, Cdirection, turn_allowed
    PacMan.turn_allowed = check_position(PacMan)
    if direction == PacMan.cdirection:
        return
    if direction == 0 and PacMan.turn_allowed[0]: #Right
        for i in range (0, 4):  
             if PacMan.cdirection == 1 : 
                PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = 180)
             if PacMan.cdirection == 2:
                PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = -90)
             if PacMan.cdirection == 3:
                PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = 90)
        PacMan.cdirection = 0
        PacMan.state = 1
         
    if direction == 1 and PacMan.turn_allowed[1]: #Left
        for i in range (0, 4):  
             if PacMan.cdirection == 0: 
                PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = 180)
             if PacMan.cdirection == 2:
                 PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = 90)
             if PacMan.cdirection == 3:
                 PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = -90)
        PacMan.cdirection = 1
        PacMan.state = 1
        
    if direction == 2  and PacMan.turn_allowed[2]: #Up
       for i in range (0, 4):  
             if PacMan.cdirection == 3: 
                PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = 180)
             if PacMan.cdirection == 1:
                 PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = -90)
             if PacMan.cdirection == 0:
                 PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = 90)
       PacMan.cdirection = 2
       PacMan.state = 1
        
    if direction == 3 and PacMan.turn_allowed[3]: #Down
       for i in range (0, 4):  
             if PacMan.cdirection == 2: 
                PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = 180)
             if PacMan.cdirection == 1:
                 PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = 90)
             if PacMan.cdirection == 0:
                 PacMan.imgs[i] = PacMan.imgs[i].rotate(angle = -90)
       PacMan.cdirection = 3
       PacMan.state = 1
       
def change_ghost_direction(A): #need fixing
    A.turn_allowed = check_position(A)
    temp = []
    count_temp = 0 
    for i in range(4):
             if A.turn_allowed[i] == True :
                 temp.append(i)
                 count_temp += 1
             if count_temp > 2 :
                 A.state = -1
    if A.state == -1 :
        A.cdirection = temp[random.randint(0,len(temp)-1)]
        print (A.state)
        A.state = 1
    move_ghost(A)

    
  
# going throught each frame of the pacman cycle
def update_player(frame) : 
    global state, PacMan, count, flicker
    topFrame.img = ImageTk.PhotoImage(PacMan.imgs[frame])
    topFrame.create_image(PacMan.x, PacMan.y, image=topFrame.img, anchor= CENTER)

# create each ghost on the screen
def draw_blinky(A):
     topFrame.img1 = ImageTk.PhotoImage(A.imgs[0]) 
     #if (not PacMan.powerup and not A.dead) or (eaten_ghost[A.id]): 
     topFrame.create_image(A.x, A.y, image= topFrame.img1, anchor=CENTER)
def draw_pinky(A):
     topFrame.img2 = ImageTk.PhotoImage(A.imgs[0])
     topFrame.create_image(A.x, A.y, image= topFrame.img2, anchor=CENTER)
def draw_inky(A):
     topFrame.img3 = ImageTk.PhotoImage(A.imgs[0])
     topFrame.create_image(A.x, A.y, image= topFrame.img3, anchor=CENTER)
def draw_clyde(A):
     topFrame.img4 = ImageTk.PhotoImage(A.imgs[0])
     topFrame.create_image(A.x, A.y, image= topFrame.img4, anchor=CENTER)
  
# moving the pacman
def move_player():
    if PacMan.state == 1:
        if PacMan.cdirection == 0:
            PacMan.x += speed
            PacMan.center_x = PacMan.x + 5
        if PacMan.cdirection == 1:
            PacMan.x -= speed
            PacMan.center_x = PacMan.x + 5
        if PacMan.cdirection == 2:
            PacMan.y -= speed
            PacMan.center_y = PacMan.y + 6
        if PacMan.cdirection == 3:
            PacMan.y += speed
            PacMan.center_y = PacMan.y + 6
            
    update_player(frame)

#moving the ghost
def move_ghost(A):
    if A.state == 1:
        if A.cdirection == 0:
                A.x += speed
                A.center_x = A.x + 5
        if A.cdirection == 1:
                A.x -= speed
                A.center_x = A.x + 5
        if A.cdirection == 2:
                A.y -= speed
                A.center_y = A.y + 6
        if A.cdirection == 3:
                A.y += speed
                A.center_y = A.y + 6

def check_position(A) :
    turn = [False, False, False, False]
    if A.center_x // row < row :
        if A.cdirection == 0: 
            if level[A.center_y // num1][(A.center_x + num3 - 1) // num2] >= 3 :
                A.state = -1
                print (f'{A.name} contact right')
            if level[A.center_y // num1][(A.center_x - num2) // num2] < 3:
                turn[1] = True
                
        if A.cdirection == 1:
            if level[A.center_y // num1][(A.center_x - num2 + 1) // num2] >= 3 :
                A.state = -1 
                print(f'{A.name} contact left')
            if level[A.center_y // num1][(A.center_y + num3) // num2] < 3:
                turn[0] = True
                
        if A.cdirection == 2:
            if level[(A.center_y - num1) // num1][(A.center_x) // num2] >= 3 :
                A.state = -1
                print(f'{A.name} contact up')
            if level[(A.center_y + num3) // num1][(A.center_x) // num2] < 3:
                turn[3] = True
                
        if A.cdirection == 3:
            if level[(A.center_y + num3) // num1][(A.center_x) // num2] >= 3 :
                A.state = -1
                print (f'{A.name} contact Down')
            if level[(A.center_y - num1) // num1][(A.center_x) // num2] < 3:
                turn[2] = True
                
                
        if A.cdirection == 2 or A.cdirection == 3 :
            if num2 - num3 <= A.center_x % num2 <= num2 + num3 :
                if level[(A.center_y + num3) // num1][(A.center_x) // num2] < 3 :
                    turn[3] = True
                if level[(A.center_y - num3) // num1][(A.center_x) // num2] < 3 :
                    turn[2] = True
            if num1 - num3 <= A.center_y % num1 <= num1 + num3 :
                if level[(A.center_y) // num1][(A.center_x + num2) // num2] < 3 :
                    turn[0] = True
                if level[(A.center_y) // num1][(A.center_x - num2) // num2] < 3 :
                    turn[1] = True
            
        if A.cdirection == 0 or A.cdirection == 1 :
            if num2 - num3 <= A.center_x % num2 <= num2 + num3 :
                if level[(A.center_y + num1) // num1][(A.center_x) // num2] < 3 :
                    turn[3] = True
                if level[(A.center_y - num1) // num1][(A.center_x) // num2] < 3 :
                    turn[2] = True
            if num1 - num3 <= A.center_y % num1 <= num1 + num3 :
                if level[(A.center_y) // num1][(A.center_x + num2) // num2] < 3 :
                    turn[0] = True
                if level[(A.center_y) // num1][(A.center_x - num2) // num2] < 3 :
                    turn[1] = True
    else: 
        turn [0] = True
        turn [1] = True
    return turn

def check_collison(scor):
    global PacMan, level
    if  0 < PacMan.x < 650 :
        if level[PacMan.center_y // num1][PacMan.center_x//num2] == 1:
            level[PacMan.center_y // num1][PacMan.center_x//num2] = 0
            scor += 10
        if level[PacMan.center_y// num1][PacMan.center_x//num2] == 2:
            level[PacMan.center_y// num1][PacMan.center_x//num2] = 0
            PacMan.powerup = True
            scor += 50
    return scor

# movement control
def move_left(event):
    global direction, PacMan
    PacMan.state = 1
    direction = 1
    print("Key A is pressed")
    history.append("A")
    change_direction_player()
def move_right(event):
    global direction, PacMan
    PacMan.state = 1
    direction = 0
    print("Key D is pressed")
    history.append("D")
    change_direction_player()
def move_up(event):
    global direction, PacMan
    PacMan.state = 1
    direction = 2
    print("Key W is pressed")
    history.append("W")
    change_direction_player()
    
def move_down(event):
    global direction, PacMan
    PacMan.state = 1
    direction = 3
    print("Key S is pressed")
    history.append("S")
    change_direction_player()
    
# other control    
def pause(event):
    global PacMan, mode
    PacMan.state = -1
    mode = 1
    
#end Function
def print_history():
    print("--------------------------")
    for i in range (len(history)):
        print(f"{i +1}: ", history[i])    
    print(blinky.center_x // num2)
    print(blinky.center_y // num1)
    print(num1)
    print(num2)
    print(num3)
    print(row)
    print(column)
    
def start_game():
    global start, state
    start = 1
    PacMan.state = 1
    

# key bind
root.bind("a", move_left)
root.bind("<Left>",move_left)
root.bind("s", move_down)
root.bind("<Down>",move_down)
root.bind("w", move_up)
root.bind("<Up>",move_up)
root.bind("d", move_right)
root.bind("<Right>",move_right)
root.bind("p", pause)

# Initialize the player animation
# change the direction of the player
#main 
def main():
    global PacMan, flicker_time, flicker, frame, count, score, state, powerup_counter
    if mode == 0 :
        #update board
        topFrame.delete('all')
        draw_board()
        draw_blinky(blinky)
        draw_pinky(pinky)
        draw_inky(inky)
        draw_clyde(clyde)
        if start != -1:
            move_player()
            change_ghost_direction(blinky)
            PacMan.turn_allowed = check_position(PacMan)
            blinky.turn_allowed = check_position(blinky)
            change_ghost_direction(pinky)
            change_ghost_direction(inky)
            change_ghost_direction(clyde)
            #check for turn avarible
            score = check_collison(score)
            #print("power up: ", PacMan.powerup)

            #debug console
            # for i in range (0, 4):
            #     print(PacMan.turn_allowed[i])
            for i in range (0, 4):
                print(blinky.turn_allowed[i])
            print("y: ",blinky.center_y // num1, " x: ", blinky.center_x // num2, "state: ", blinky.state, "cdirec: ", blinky.cdirection)
            print("------------------------------------------")
            # #main functionality
      
            frame = (frame + 1) % len(PacMan.imgs)
            if count < 19: # control the cycle of PacMan
                count += 1
                if count > 1:
                    flicker = False
            else:
                flicker = True
                count = 0

            for i in range (0, 4):
                if direction == i and PacMan.turn_allowed[i]:
                    change_direction_player()
            if blinky.state == 1:
                blinky.turn_allowed = check_collison(blinky)

            if PacMan.powerup == True and powerup_counter < 100:
                powerup_counter += 1
            elif PacMan.powerup == True and powerup_counter >= 100:
                powerup_counter = 0
                PacMan.powerup = False
                eaten_ghost = [False, False, False, False]

            draw_random()       
        else:
            draw_initial_player()
        root.after(1000 // desired_fps, main)
    else:
        print('program has been stopped!')
        slide_arr(history)
        print_history()
    
# draw_board()
draw_panel()
# draw_initial_player()

main()
    
root.mainloop()