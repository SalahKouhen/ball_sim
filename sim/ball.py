# Holds the ball class:
import numpy as np
from room import Room

class Ball:
    ''' Class to represent a bouncy ball. 
    Fields:
        - index:       Index of this ball
        - rad:         The shape of a ball, is a ball. What is it's radius?
        - pos:         Where the ball is
        - vel:         Speed (in any direction)
        - elast:       How bouncy the ball is
        - colour:      Array ie (255,255,255) to give the colour of the ball in RGB
        - room:        What room it is in 
        - mass:        How massive the ball is       

     Methods:
        - __init__:    Initialise all the fields of the class
        - play:        Step the ball forward in time
    '''
    def __init__(self, index: int, rad: int, pos, vel, force, mass, elast, colour, room: Room) -> None:
        self.index = index
        self.rad = rad # all in pixels
        self.pos = pos
        self.vel = vel
        self.force = force
        self.mass = mass
        self.room = room
        self.elast = elast
        self.colour = colour       

    def exertForce(self, newForce) -> None:
        self.force = newForce
        
    def play2D(self, dt: float) -> None:
        '''Method to play forward the ball

        :param dt: size of time step 
        :returns: updates the value of position 
        '''
        #Keep track of forces on ball
        self.force = self.room.gravity #Gravity

        #Friction
        fricForce = 0
        if self.rad + self.pos[1] == self.room.height: #floor
            var = self.force[1]/self.mass*self.room.fric*dt
            if abs(var) >= abs(self.vel[0]):
                self.vel[0] =  0
            elif(self.vel[0] > 0):
                self.vel[0] += -np.sign(self.vel[0])*self.force[1]/self.mass*self.room.fric*dt
        
        #Updates position and velocity under force
        self.pos = np.array([ 0.5*self.force[0]/self.mass*dt**2 + self.vel[0]*dt + self.pos[0], 0.5*self.force[1]/self.mass*dt**2 + self.vel[1]*dt + self.pos[1] ]) 
        self.vel = np.array([ self.force[0]/self.mass*dt + self.vel[0] , self.force[1]/self.mass*dt + self.vel[1] ])
        # Note positive direction in x is to the right and in y is downwards 

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

