# Holds the visualisation code:
# Idea is you will see a white room with lots of bouncy balls 

import pygame
import time
import numpy as np

pygame.init()

# Initialise any colours we may want to use
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#create room
from room import Room
our_Room = Room(800,600)

# Create the room (a display window)
gameDisplay = pygame.display.set_mode((our_Room.width,our_Room.height))
gameDisplay.fill(white) 

#create ball
from ball import Ball
our_Ball = Ball(1, 75, np.array([400,300]), np.array([5,0]))
pygame.draw.circle(gameDisplay, black, (round(our_Ball.pos[0]),round(our_Ball.pos[1])), our_Ball.rad)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    our_Ball.play2D(0.1)
    pygame.draw.circle(gameDisplay, black, (round(our_Ball.pos[0]),round(our_Ball.pos[1])), our_Ball.rad)
    pygame.display.update()
    time.sleep(0.01)
    gameDisplay.fill(white)