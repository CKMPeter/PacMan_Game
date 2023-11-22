from email.mime import image
from shutil import move
from tkinter import *
from tkinter import filedialog, ttk
from tokenize import String
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
from variable import *


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
goal_score = goal_point(level)


#widely used var
eaten_ghost = [False, False, False, False]
ghost_img = []

# bonus Var
history = []
mode = 0
cheat_code = ['','','','']


#initial start location
#PacMan inital
PacMan = player('pacman',(row // 2) * num1 - num1, (column // 2) * num2 + (7 * num2), 0)
player.add_frame(PacMan)
player.powerup(PacMan)
direction = 0
player_imgs.append(PacMan.imgs[0])

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
spooked_img = Image.open('assets/ghost/powerup.png').resize((30, 30))
dead_img = Image.open('assets/ghost/dead.png').resize((30, 30))

#Begin program
#start GUI
root =Tk()
root.title('PAC MAN')
root.configure(background= 'Black')
root.geometry('1350x800') #level 1650x800
#root.geometry('1650x800')


#score initial
score_display = StringVar()
score_display.set("score: 0")

status_display = StringVar()
current_status = "Chosing mode"
status_display.set(str(current_status))



topFrame = Canvas(root, bg = "Black", width = WIDTH, height = HEIGHT)
topFrame.pack(padx = 200,side=LEFT)

rightFrame = Frame(root, bg = "Black", width = 50, height = HEIGHT)
rightFrame.pack(side=LEFT)

topFrame1 = Frame(rightFrame, bg = "Black", width = WIDTH // 4 + 20, height = HEIGHT // 4)
topFrame1.pack()

logoFrame = Image.open('assets/logo/pacman.jpg').resize((WIDTH // 2 + 20, HEIGHT // 4))
logoFrame = ImageTk.PhotoImage(logoFrame)
logo = Label(topFrame1, bg = 'Black' ,image= logoFrame)
logo.image = logoFrame
logo.pack()

topFrame2 = Frame(rightFrame, bg = "Black", width = WIDTH // 4 + 20, height = HEIGHT // 4)
topFrame2.pack()

score_frame = Label(topFrame2, textvariable= score_display, font= font, bg = 'Black', fg = 'White')
score_frame.pack()

game_status = Label(topFrame2, textvariable= status_display, font = font, bg = 'Black', fg = 'White')
game_status.pack()

botFrame1 = Frame(rightFrame, bg = "Black", width = 50, height = HEIGHT // 2)
botFrame1.pack(side=LEFT)

botFrame2 = Frame(rightFrame, bg = "Black", width = 50, height = HEIGHT // 2)



#function
topFrame.spooked = ImageTk.PhotoImage(spooked_img)
topFrame.dead = ImageTk.PhotoImage(dead_img)
#draw random
def draw_random(index):
    global PacMan, life
    
    #life display 
    if life >= 1:
        topFrame.life = ImageTk.PhotoImage(player_imgs[0])
        topFrame.create_image(WIDTH - 20, HEIGHT - 50, image = topFrame.life, anchor = CENTER)
    if life >= 2:
        topFrame.life1 = ImageTk.PhotoImage(player_imgs[0])
        topFrame.create_image(WIDTH - 55, HEIGHT - 50, image = topFrame.life1, anchor = CENTER)
    if life >= 3:
        topFrame.life2 = ImageTk.PhotoImage(player_imgs[0])
        topFrame.create_image(WIDTH - 90, HEIGHT - 50, image = topFrame.life2, anchor = CENTER)
    #power_up indication
    if PacMan.powerup == True:
        topFrame.create_oval(num1 * 3, HEIGHT - 50, num1 * 3, HEIGHT - 50, outline = color, width= 20)
        
    status_display.set(str(current_status) + str(loading[index]))
    
        

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
    solve_button = Button(botFrame1, font = font ,text = "Solve", command = solve_pacman)
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
   
def update_score(scor):
    global score_display
    score_display.set("score: " + str(scor))
    
def update_game_status(state):
    global current_status
    current_status = state
    
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
       
def change_ghost_direction(A):
    global direction
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
        if A.name == 'pacman':
            direction = temp[random.randint(0,len(temp)-1)]
            change_direction_player()
        else:
            A.cdirection = temp[random.randint(0,len(temp)-1)]
        print (A.state)
        A.state = 1
    if A.name == 'pacman':
        move_player()
    else:
        move_ghost(A)

    
  
# going throught each frame of the pacman cycle
def update_player(frame) : 
    global state, PacMan, count, flicker
    topFrame.img = ImageTk.PhotoImage(PacMan.imgs[frame])
    topFrame.create_image(PacMan.x, PacMan.y, image=topFrame.img, anchor= CENTER)

# create each ghost on the screen
def ghost_instance():
    topFrame.img1 = ImageTk.PhotoImage(blinky.imgs[0]) 
    topFrame.img2 = ImageTk.PhotoImage(pinky.imgs[0])
    topFrame.img3 = ImageTk.PhotoImage(inky.imgs[0])
    topFrame.img4 = ImageTk.PhotoImage(clyde.imgs[0])    

def draw_ghost(A, B):
     #if (not PacMan.powerup and not A.dead) or (eaten_ghost[A.id]): 
     global PacMan, eaten_ghost, life, hit
     if PacMan.powerup != True:
        topFrame.create_image(A.x, A.y, image= B, anchor=CENTER)
        if (A.center_x // num1 == PacMan.center_x // num1 and A.center_y // num2 == PacMan.center_y // num2 and hit == False):
           life -= 1
           hit = True
     else:
        if (A.center_x // num1 == PacMan.center_x // num1 and A.center_y // num2 == PacMan.center_y // num2):
            eaten_ghost[A.id] = True
        if eaten_ghost[A.id] == True :
            topFrame.create_image(A.x, A.y, image= topFrame.dead, anchor = CENTER)
        else:
            topFrame.create_image(A.x, A.y, image= topFrame.spooked, anchor = CENTER)
            
         
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
    global PacMan, mode, goal_score
    PacMan.state = -1
    mode = 1
    goal_score = goal_point(level)
    print (goal_score)
    
#end Function
def print_history():
    print("--------------------------")
    for i in range (len(history)):
        print(f"{i +1}: ", history[i])    
    # print(blinky.center_x // num2)
    # print(blinky.center_y // num1)
    # print(num1)
    # print(num2)
    # print(num3)
    # print(row)
    # print(column)
    
def start_game():
    global start, moving
    if moving == 1:
        moving = 0
    start = 1
    PacMan.state = 1
    update_game_status('Playing')
    # key bind
    bA = root.bind("a", move_left)
    bL =root.bind("<Left>",move_left)
    bS = root.bind("s", move_down)
    bDw = root.bind("<Down>",move_down)
    bW = root.bind("w", move_up)
    bU = root.bind("<Up>",move_up)
    bD = root.bind("d", move_right)
    bR = root.bind("<Right>",move_right)
    bP = root.bind("p", pause)
    
def solve_pacman():
    global moving, start
    moving = 1
    start = 1
    PacMan.state = 1
    update_game_status('Solving')

# Initialize the player animation
# change the direction of the player
#main 
def main():
    global PacMan, flicker_time, flicker, frame, count, score, state, powerup_counter, life, eaten_ghost, hit, mode, start, index
    if mode == 0 :
        #update board
        topFrame.delete('all')
        draw_board()
        draw_ghost(blinky, topFrame.img1)
        draw_ghost(pinky, topFrame.img2)
        draw_ghost(inky, topFrame.img3)
        draw_ghost(clyde, topFrame.img4)
        if index == 4:
            index = 0
        if start != -1:
            
            change_ghost_direction(blinky)
            change_ghost_direction(pinky)
            change_ghost_direction(inky)
            change_ghost_direction(clyde)
            if moving == 1 :
                change_ghost_direction(PacMan)
            else:
                move_player()
            PacMan.turn_allowed = check_position(PacMan)
            blinky.turn_allowed = check_position(blinky)
            
            #sum score and update score
            score = check_collison(score)
            update_score(score)
            if score == goal_score:
                update_game_status('WIN!')
                start = -1
            if life == 0:
                start = -1
                update_game_status('Game Over!')
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
                index += 1
                flicker = True
                count = 0
                hit = False

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
            draw_random(index)  
            

            
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
ghost_instance()
main()
    
root.mainloop()