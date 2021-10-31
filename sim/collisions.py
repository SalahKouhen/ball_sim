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
                #Specifically we add M to ball 1's momentum and minus it from ball 2
                #M is a * (cos theta, sin theta) for some a 
                #cos theta is the x distance between the centres divided by the length between them
                #I calculated (by conserving kinetic energy) that a * (1/m1 + 1/m2) = 2(u2 cos + v2 sin - u1 cos - v1 sin) 
                #The velocity is then updated by adding and subtracting M/relevant m
                vdis = balls[j].pos - balls[i].pos
                #print(vdis)
                dist = (vdis[0]**2+vdis[1]**2)**0.5
                #print(dist)
                vtrig = vdis/dist
                #print(vtrig)
                a =  2/(1/balls[j].mass + 1/balls[i].mass) * np.dot((balls[j].vel - balls[i].vel),vtrig) 
                #print(a)
                vM = a * vtrig
                #print(vM)
                #print(balls[i].vel)
                balls[i].vel += vM/balls[i].mass
                balls[j].vel -= vM/balls[j].mass
                #print(balls[i].vel)

                #Need to stop balls intersecting
                #Idea is we compare x and y pos of centres to what they should be and correct by adding half that distance to each
                #I think the signs should be mixed this way due to down being positive for y
                growth = (balls[i].rad + balls[j].rad)/math.sqrt((balls[i].pos[0]-balls[j].pos[0])**2+(balls[i].pos[1]-balls[j].pos[1])**2) - 1 
                #correct (wanted dist/real dist) - 1 tells you how much longer each triangle side should be 
                balls[i].pos[0] -= growth*0.5*(balls[j].pos[0]-balls[i].pos[0])
                balls[j].pos[0] += growth*0.5*(balls[j].pos[0]-balls[i].pos[0])
                balls[i].pos[1] -= growth*0.5*(balls[j].pos[1]-balls[i].pos[1])
                balls[j].pos[1] += growth*0.5*(balls[j].pos[1]-balls[i].pos[1])
                