# Holds the ball class:
import numpy as np

class Ball:
    ''' Class to represent a bouncy ball. 
    Fields:
        - index:       Index of this ball
        - rad:         The shape of a ball, is a ball. What is it's radius?
        - pos:         Where the ball is
        - vel:         How fast it's going (only in vertical direction for now)
        TBA
        - elast:       How bouncy the ball is
        - mass:        How massive the ball is
        - vel:         Speed (in any direction)

     Methods:
        - __init__:    Initialise all the fields of the class
        - play:        Step the ball forward in time
    '''
    def __init__(self, index: int, rad:int, pos, vel) -> None:
        self.index = index
        self.rad = rad # all in pixels
        self.pos = pos
        self.vel = vel

    def play2D(self, dt: float) -> None:
        '''Method to play forward the ball

        :param dt: size of time step 
        :returns: updates the value of position 
        '''
        self.pos = np.array([ self.vel[0]*dt+self.pos[0], 0.5*10*dt**2 + self.vel[1]*dt + self.pos[1] ]) 
        self.vel = np.array([ self.vel[0] , 10*dt + self.vel[1] ])

        #Basic bounce
        if self.rad + self.pos[1] > 600 or self.pos[1] - self.rad  < 0:
            self.vel[1] = -1*self.vel[1]

        if self.rad + self.pos[0] > 800  or self.pos[0] - self.rad < 0:
            self.vel[0] = -1*self.vel[0]