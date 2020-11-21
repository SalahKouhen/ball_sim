#Holds the room class:
import numpy as np
import math

class Room:
    ''' Class to represent the room our balls are in. 
    Fields:
        - width:       width of room
        - height:      height of room
        - gravity:     strength of gravity in room

     Methods:
        - __init__:    Initialise all the fields of the class
    '''
    def __init__(self, width: int, height: int, elast, fric, gravity,time=0) -> None:
        self.width = width # both are in pixels
        self.height = height
        self.elast = elast # [up wall, right wall, down wall, left wall]
        self.fric = fric
        self.gravity = gravity
        self.time = time
        self.gravStrength = (self.gravity[0]**2+self.gravity[1]**2)**0.5

    def spinShipCrash(self, freq): # if updates every 0.005 secs then freq of 1/200 will rotate grav every second
        self.time += 1
        self.gravity = np.array([self.gravStrength*math.cos(2*math.pi*freq*self.time),self.gravStrength*math.sin(2*math.pi*freq*self.time)])

