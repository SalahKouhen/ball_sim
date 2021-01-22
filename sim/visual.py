# Holds the visualisation code:
# Idea is you will see a white room with lots of bouncy balls 

#### PROJECT GOALS ####
# See the difference in pressure caused by Bernoulli at a molecular level
# The current code will only be in 2D, there should be a sequel in 3D
# Home screen
# tools to interact with balls: 
#   - click to add ball specified by some sliders
#   - draw in a wall
#   - draw in a pressure measurement wall
#   - output distribution of velocities - how does this change for a substance with difference mass particles inside?
#   - virus transmission mode


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

#text
myfont =pygame.freetype.Font(None, 30)
text_surface, rect = myfont.render("Hello World!", (0, 100, 0)) #string, colour


#create room
from room import Room
our_Room = Room(1000,600,1*np.array([1,1,1,1]),0.8,np.array([0,0])) #width: int, height: int, elast, fric, gravity

# Create the room (a display window)
gameDisplay = pygame.display.set_mode((our_Room.width,our_Room.height))
gameDisplay.fill(white) 

#create balls
from ball import Ball
n = 9 #number of balls
balls = []
balls.append(Ball(1, 15, np.array([our_Room.width/2,our_Room.height/2]), np.array([-30,0]), np.array([0,0]), 1, 1, red, our_Room))
balls.append(Ball(2, 15, np.array([our_Room.width/4,our_Room.height/2]), np.array([30,0]), np.array([0,0]), 1, 1, blue, our_Room))
balls.append(Ball(2, 15, np.array([3*our_Room.width/4,our_Room.height/2]), np.array([10,-10]), np.array([0,0]), 1, 1, green, our_Room))
balls.append(Ball(2, 15, np.array([our_Room.width/2,3*our_Room.height/4]), np.array([10,30]), np.array([0,0]), 1, 1, green, our_Room))
balls.append(Ball(2, 15, np.array([our_Room.width/4,3*our_Room.height/4]), np.array([-30,0]), np.array([0,0]), 0.1, 1, blue, our_Room))
balls.append(Ball(2, 5, np.array([3*our_Room.width/4,3*our_Room.height/4]), np.array([10,0]), np.array([0,0]), 1, 1, black, our_Room))
balls.append(Ball(2, 15, np.array([our_Room.width/2,our_Room.height/4]), np.array([10,25]), np.array([0,0]), 1, 1, green, our_Room))
balls.append(Ball(2, 15, np.array([our_Room.width/4,our_Room.height/4]), np.array([-30,0]), np.array([0,0]), 0.1, 1, blue, our_Room))
balls.append(Ball(2, 5, np.array([3*our_Room.width/4,our_Room.height/4]), np.array([10,11]), np.array([0,0]), 1, 1, black, our_Room))

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