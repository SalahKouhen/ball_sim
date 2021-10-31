# Holds the wall class:

class Wall:
    ''' Class to represent a wall. 
    Fields:
        - startp:      where the wall starts
        - endp:        where the wall ends
        - colour:      Array ie (255,255,255) to give the colour of the ball in RGB

     Methods:
        - __init__:    Initialise all the fields of the class
    '''

    def __init__(self, startp, endp, colour=(0,0,0)) -> None:
        self.startp = startp 
        self.endp = endp
        self.colour = colour      