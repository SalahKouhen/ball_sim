# Holds the visualisation code:
# Idea is you will see a white room with lots of bouncy balls 

#TBA
# generalisation to shapes other than a circle

import pygame
import pygame.freetype
import time
import numpy as np
import math
from threading import Timer

pygame.init()

# Initialise any colours we may want to use
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#text
myfont =pygame.freetype.Font(None, 15)
controlstext, rect = myfont.render("Controls: a - add mode, d - draw mode, i - infect mode", black) #string, colour
addmodetext, rect = myfont.render("Add mode. Click to add a ball!", black) 
drawmodetext, rect = myfont.render("Draw mode. Click two places to add a wall!", black) 
infectmodetext, rect = myfont.render("Infect mode. Click a ball to infect it!", black) 

#create room
from room import Room
our_Room = Room(1000,600,1*np.array([1,1,1,1]),0.8,np.array([0,0])) #width: int, height: int, elast, fric, gravity

# Create the room (a display window)
gameDisplay = pygame.display.set_mode((our_Room.width,our_Room.height))
gameDisplay.fill(white) 

#create balls
from ball import Ball

balls = []
balls.append(Ball(4, 15, np.array([our_Room.width/2,3*our_Room.height/4]), np.array([10,30]), np.array([0,0]), 1, 1, blue, our_Room))
balls.append(Ball(5, 15, np.array([our_Room.width/4,3*our_Room.height/4]), np.array([-30,0]), np.array([0,0]), 1, 1, blue, our_Room))
balls.append(Ball(6, 15, np.array([3*our_Room.width/4,3*our_Room.height/4]), np.array([10,0]), np.array([0,0]), 1, 1, blue, our_Room))
#balls.append(Ball(7, 15, np.array([our_Room.width/2,our_Room.height/4]), np.array([10,25]), np.array([0,0]), 1, 1, green, our_Room))
#balls.append(Ball(8, 15, np.array([our_Room.width/4,our_Room.height/4]), np.array([-30,0]), np.array([0,0]), 0.1, 1, blue, our_Room))
#balls.append(Ball(9, 5, np.array([3*our_Room.width/4,our_Room.height/4]), np.array([10,11]), np.array([0,0]), 1, 1, black, our_Room))

clicked_balls = []
infected_balls = []
recovered_balls = []
recoverytimes = []

#create walls

from wall import Wall

walls = []
#walls.append(Wall(np.array([our_Room.width/4,our_Room.height/2]),np.array([3*our_Room.width/4,our_Room.height/2])))

#mode flags
addFlag = 0
drawFlag = 0
infectFlag = 0

#parameters for infection (when have settings can change it there)
recovertime = 3000 # in milliseconds
infectionrate = 0.5 # chance that infection is passed on

#pygame event that allows balls to recover
recover_event = pygame.USEREVENT + 1

def recover(ballIndex):
    infected_balls.remove(ballIndex)
    recovered_balls.append(ballIndex)

#import function for dealing with collisions
from collisions import collide

while True:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            posDown = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            #for b in balls:
            #    if math.sqrt((b.pos[0]-pos[0])**2+(b.pos[1]-pos[1])**2) <= b.rad:
            #        clicked_balls.append(balls.index(b))

            if addFlag == 1:
                if all(math.sqrt((b.pos[0]-pos[0])**2+(b.pos[1]-pos[1])**2) > b.rad + 15 for b in balls):
                    newVel = np.array([float(pos[0]),float(pos[1])]) - np.array([float(posDown[0]),float(posDown[1])]) 
                    balls.append(Ball(1, 15, np.array([float(pos[0]),float(pos[1])]), newVel, np.array([0,0]), 1, 1, blue, our_Room))

            if drawFlag == 1:
                dpos =  np.array([float(posDown[0]),float(posDown[1])])
                upos =  np.array([float(pos[0]),float(pos[1])])
                walls.append(Wall(dpos, upos))

            if infectFlag == 1:
                for b in balls:
                    if math.sqrt((b.pos[0]-pos[0])**2+(b.pos[1]-pos[1])**2) <= b.rad:                       
                        b.colour = red
                        infected_balls.append(balls.index(b))
                        recoverytimes.append([balls.index(b),pygame.time.get_ticks() + recovertime])   

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and drawFlag == 0 and infectFlag == 0:
                # adding mode
                addFlag = (addFlag + 1)%2

            if event.key == pygame.K_d and addFlag == 0 and infectFlag == 0:
                # drawing mode
                drawFlag = (drawFlag + 1)%2

            if event.key == pygame.K_i and addFlag == 0 and drawFlag == 0 :
                # infect mode
                infectFlag = (infectFlag + 1)%2

    #find out if any collisions occoured 
    collide(balls,walls,infected_balls,recovered_balls,infectionrate,recoverytimes,recovertime)

    for i in infected_balls:
        balls[i].colour = red 

    for i in recoverytimes:
        if i[1] < pygame.time.get_ticks():
            recovered_balls.append(i[0])

    for i in recovered_balls:
        balls[i].colour = black


    #Funk around with gravity
    #our_Room.spinShipCrash(1/2000)

    # draw balls

    for i in range(len(balls)):
        balls[i].play2D(0.1)
        pygame.draw.circle(gameDisplay, balls[i].colour, (round(balls[i].pos[0]),round(balls[i].pos[1])), balls[i].rad)
    
    # draw walls

    for i in range(len(walls)):
        pygame.draw.line(gameDisplay, walls[i].colour, walls[i].startp, walls[i].endp)

    # text

    if addFlag == 0 and drawFlag == 0 and infectFlag == 0:
        gameDisplay.blit(controlstext, (our_Room.width/40, our_Room.height/80))

    if addFlag == 1:
        gameDisplay.blit(addmodetext, (our_Room.width/40, 7*our_Room.height/8)) 

    if drawFlag == 1:
        gameDisplay.blit(drawmodetext, (our_Room.width/40, 7*our_Room.height/8)) 

    if infectFlag == 1:
        gameDisplay.blit(infectmodetext, (our_Room.width/40, 7*our_Room.height/8)) 

    for i in clicked_balls:
        ballinfo, rect = myfont.render(str(np.dot(balls[i].vel,balls[i].vel)), black)
        gameDisplay.blit(ballinfo, (round(balls[i].pos[0]),round(balls[i].pos[1]))) #ball 1 label text

    '''
    #Bug fixing, labels each ball with properties it has
    for i in range(n):
        ball1info, rect = myfont.render(str(np.dot(balls[i].vel,balls[i].vel)), black)
        gameDisplay.blit(ball1info, (round(balls[i].pos[0]),round(balls[i].pos[1]))) #ball 1 label text
    '''

    pygame.display.update()
    time.sleep(0.01)
    gameDisplay.fill(white)