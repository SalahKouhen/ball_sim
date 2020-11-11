# Deals with ball to ball madness
import math

def collide(balls):
    '''Function to handle ball to ball collisions
    TBA: Kinetic energy conservation

    :param balls: array containing all the balls in the room
    :returns:  updates the velocities of the balls and their positions appropriately
    '''
    #First we have to check if any of the balls are touching 
    for i in range(len(balls)):
        for j in range(i+1,len(balls)):
            if math.sqrt((balls[i].pos[0]-balls[j].pos[0])**2+(balls[i].pos[1]-balls[j].pos[1])**2) <= balls[i].rad + balls[j].rad:
                #then if they do, update their velocities, may need to update their positions as well to make visual better/ avoid balls sticking
                # currently collisions are completely elastic which is kind of an infinite mass limit, need to make kinetic energy be conserved
                balls[i].vel *= -balls[i].elast*balls[j].elast
                balls[j].vel *= -balls[i].elast*balls[j].elast