# Runs a simulation of a patch of air at a particle level using the classes ball and room:
# Idea is you will see oxygen, nitrogen and carbon dioxide floating around

### TBA 
# Output of the maxwell distribution 

import pygame
import pygame.freetype
import time
import numpy as np

pygame.init()

# Initialise any colours we may want to use
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
purple = (128,0,128)

#text
myfont =pygame.freetype.Font(None, 30)
text_surface, rect = myfont.render("Air Sim!", (0, 100, 0)) #string, colour


#create room
from room import Room
our_Room = Room(1000,600,1*np.array([1,1,1,1]),0.8,np.array([0,0])) #width: int, height: int, elast, fric, gravity

# Create the room (a display window)
gameDisplay = pygame.display.set_mode((our_Room.width,our_Room.height))
gameDisplay.fill(white) 

#Element list: rad in 10pm, mass in amu, colour
O2 = [30,32,red]
N2 = [31,28,blue]
Ar = [36,39,purple]
CO2 = [33,44,black]

#create balls
from ball import Ball
n = 9 #number of balls
balls = []
balls.append(Ball(1, O2[0], np.array([our_Room.width/2,our_Room.height/2]), np.array([-30,-10]), np.array([0,0]), O2[1], 1, O2[2], our_Room))
balls.append(Ball(1, N2[0], np.array([our_Room.width/2,our_Room.height/4]), np.array([-30,20]), np.array([0,0]), N2[1], 1, N2[2], our_Room))
balls.append(Ball(1, N2[0], np.array([our_Room.width/2,3*our_Room.height/4]), np.array([-30,0]), np.array([0,0]), N2[1], 1, N2[2], our_Room))
balls.append(Ball(1, CO2[0], np.array([our_Room.width/4,our_Room.height/2]), np.array([-30,0]), np.array([0,0]), CO2[1], 1, CO2[2], our_Room))
balls.append(Ball(1, N2[0], np.array([our_Room.width/4,our_Room.height/4]), np.array([-30,10]), np.array([0,0]), N2[1], 1, N2[2], our_Room))
balls.append(Ball(1, N2[0], np.array([our_Room.width/4,3*our_Room.height/4]), np.array([-30,0]), np.array([0,0]), N2[1], 1, N2[2], our_Room))
balls.append(Ball(1, Ar[0], np.array([3*our_Room.width/4,our_Room.height/2]), np.array([-30,20]), np.array([0,0]), Ar[1], 1, Ar[2], our_Room))
balls.append(Ball(1, N2[0], np.array([3*our_Room.width/4,our_Room.height/4]), np.array([-30,0]), np.array([0,0]), N2[1], 1, N2[2], our_Room))
balls.append(Ball(1, N2[0], np.array([3*our_Room.width/4,3*our_Room.height/4]), np.array([-30,-10]), np.array([0,0]), N2[1], 1, N2[2], our_Room))


#import function for dealing with collisions
from collisions import collide

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    #find out if any collisions occoured 
    collide(balls)

    #Funk around with gravity
    our_Room.spinShipCrash(1/2000)

    for i in range(n):
        balls[i].play2D(0.1)
        pygame.draw.circle(gameDisplay, balls[i].colour, (round(balls[i].pos[0]),round(balls[i].pos[1])), balls[i].rad)
    
    gameDisplay.blit(text_surface, (40, 250)) #hello world text output

    '''
    #Bug fixing, labels each ball with properties it has
    for i in range(n):
        ball1info, rect = myfont.render(str(np.dot(balls[i].vel,balls[i].vel)), black)
        gameDisplay.blit(ball1info, (round(balls[i].pos[0]),round(balls[i].pos[1]))) #ball 1 label text
    '''

    pygame.display.update()
    time.sleep(0.01)
    gameDisplay.fill(white)