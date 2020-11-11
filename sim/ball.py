# Holds the ball class:
import numpy as np
from room import Room

class Ball:
    ''' Class to represent a bouncy ball. 
    Fields:
        - index:       Index of this ball
        - rad:         The shape of a ball, is a ball. What is it's radius?
        - pos:         Where the ball is
        - vel:         How fast it's going (only in vertical direction for now)
        - elast:       How bouncy the ball is
        - colour:      Array ie (255,255,255) to give the colour of the ball in RGB
        - room:        What room it is in 
        TBA
        - mass:        How massive the ball is
        - vel:         Speed (in any direction)

     Methods:
        - __init__:    Initialise all the fields of the class
        - play:        Step the ball forward in time
    '''
    def __init__(self, index: int, rad: int, pos, vel, elast, colour, room: Room) -> None:
        self.index = index
        self.rad = rad # all in pixels
        self.pos = pos
        self.vel = vel
        self.room = room
        self.elast = elast
        self.colour = colour
        

    def play2D(self, dt: float) -> None:
        '''Method to play forward the ball

        :param dt: size of time step 
        :returns: updates the value of position 
        '''
        #Updates position and velocity under gravity
        self.pos = np.array([ self.vel[0]*dt+self.pos[0], 0.5*10*dt**2 + self.vel[1]*dt + self.pos[1] ]) 
        self.vel = np.array([ self.vel[0] , 10*dt + self.vel[1] ])

        #Basic bounce when hits one of four walls
        if self.rad + self.pos[1] > self.room.height: #floor
            self.vel[1] = -self.elast*self.room.elast[2]*self.vel[1]
            self.pos[1] = self.room.height - self.rad
        elif self.pos[1] - self.rad  < 0: #ceiling
            self.vel[1] = -self.elast*self.room.elast[0]*self.vel[1]
            self.pos[1] = self.rad           

        if self.rad + self.pos[0] > self.room.width: #right wall
            self.vel[0] = -self.elast*self.room.elast[1]*self.vel[0]
            self.pos[0] = self.room.width - self.rad
        elif self.pos[0] - self.rad  < 0: #left wall
            self.vel[0] = -self.elast*self.room.elast[3]*self.vel[0]
            self.pos[0] = self.rad  

        #Friction
        if self.rad + self.pos[1] == self.room.height: #floor
            var = -np.sign(self.vel[0])*10*self.room.fric*dt
            if abs(var) > abs(self.vel[0]):
                var = -self.vel[0]
            self.vel[0] =  var + self.vel[0]