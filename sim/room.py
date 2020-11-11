#Holds the room class:

class Room:
    ''' Class to represent the room our balls are in. 
    Fields:
        - width:       width of room
        - height:      height of room
        TBA
        - gravity:     strength of gravity in room

     Methods:
        - __init__:    Initialise all the fields of the class
    '''
    def __init__(self, width: int, height: int, elast, fric) -> None:
        self.width = width # both are in pixels
        self.height = height
        self.elast = elast # [up wall, right wall, down wall, left wall]
        self.fric = fric
