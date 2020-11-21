# Deals with ball to ball madness
import math
import numpy as np

def collide(balls):
    '''Function to handle ball to ball collisions
    TBA: GLANCING BLOWS DON'T CURRENTLY WORK

    :param balls: array containing all the balls in the room
    :returns:  updates the velocities of the balls and their positions appropriately
    '''
    #First we have to check if any of the balls are touching 
    for i in range(len(balls)):
        for j in range(i+1,len(balls)):
            if math.sqrt((balls[i].pos[0]-balls[j].pos[0])**2+(balls[i].pos[1]-balls[j].pos[1])**2) <= balls[i].rad + balls[j].rad:
                
                #most basic thing I can do:
                #balls[i].vel *= -balls[i].elast*balls[j].elast
                #balls[j].vel *= -balls[i].elast*balls[j].elast

                #If two balls collide then they are going to exchange momentum
                #They are only going to be able to do this along the line between their centres <- why? Because otherwise there would be torques involved
                #and I am assuming that doesn't happen
                #So the momentum goes up for one ball and down for the other by some vector M
                #Specifically we add M to ball 1's momentum and minus if from ball 2
                #M is (a*cos theta, b*sin theta) for some a and b that depend on conservation of energy
                #cos theta is the x distance betwee the centres divided by the length between them
                #I calculated that a = (u2 - u1) 2/ (cos theta (1/m1 + 1/m2)) similar for b but with v and sin
                #The velocity is then updated by adding and subtracting M/relevant m
                vdis = balls[j].pos - balls[i].pos
                dist = (vdis[0]**2+vdis[1]**2)**0.5
                vtrig = vdis/dist
                vM = 2/(1/balls[j].mass+1/balls[i].mass)*(balls[j].vel - balls[i].vel)
                balls[i].vel += vM/balls[i].mass
                balls[j].vel -= vM/balls[j].mass

                #Need to stop balls intersecting
                #Idea is we compare x and y pos of centres to what they should be and correct by adding half that distance to each
                #I think the signs should be mixed this way due to down being positive for y
                growth = (balls[i].rad + balls[j].rad)/math.sqrt((balls[i].pos[0]-balls[j].pos[0])**2+(balls[i].pos[1]-balls[j].pos[1])**2) - 1
                balls[i].pos[0] -= growth*0.2*(balls[j].pos[0]-balls[i].pos[0])
                balls[j].pos[0] += growth*0.2*(balls[j].pos[0]-balls[i].pos[0])
                balls[i].pos[1] -= growth*0.2*(balls[j].pos[1]-balls[i].pos[1])
                balls[j].pos[1] += growth*0.2*(balls[j].pos[1]-balls[i].pos[1])
                