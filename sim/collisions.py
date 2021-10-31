# Deals with ball to ball madness
import math
import numpy as np
import pygame

def collide(balls,walls, infected_balls,recovered_balls,infectionrate,recoverytimes,recovertime):
    '''Function to handle ball to ball collisions

    :param balls: array containing all the balls in the room
    :param walls: array containing all the walls in the room
    :param infected: array containing which balls are infected
    :returns:  updates the velocities of the balls and their positions appropriately
    '''
    
    #Basic bounce when hits one of four walls
    for i in range(len(balls)):
        if balls[i].rad + balls[i].pos[1] > balls[i].room.height: #floor
            balls[i].vel[1] = -balls[i].elast*balls[i].room.elast[2]*balls[i].vel[1]
            balls[i].pos[1] = balls[i].room.height - balls[i].rad
        elif balls[i].pos[1] - balls[i].rad  < 0: #ceiling
            balls[i].vel[1] = -balls[i].elast*balls[i].room.elast[0]*balls[i].vel[1]
            balls[i].pos[1] = balls[i].rad           

        if balls[i].rad + balls[i].pos[0] > balls[i].room.width: #right wall
            balls[i].vel[0] = -balls[i].elast*balls[i].room.elast[1]*balls[i].vel[0]
            balls[i].pos[0] = balls[i].room.width - balls[i].rad
        elif balls[i].pos[0] - balls[i].rad  < 0: #left wall
            balls[i].vel[0] = -balls[i].elast*balls[i].room.elast[3]*balls[i].vel[0]
            balls[i].pos[0] = balls[i].rad 
    
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

                if (j not in recovered_balls and i not in recovered_balls): 
                    randomnum = np.random.rand()
                    if randomnum<infectionrate:                    
                        if (j in infected_balls and i not in infected_balls):
                            infected_balls.append(i)
                            recoverytimes.append([i,pygame.time.get_ticks() + recovertime])  
                        if (i in infected_balls and j not in infected_balls):
                            infected_balls.append(j)
                            recoverytimes.append([j,pygame.time.get_ticks() + recovertime])  
                              
    for i in range(len(walls)):
        for j in range(len(balls)):
            balltowallvect = balls[j].pos - walls[i].startp
            wallvect = walls[i].endp - walls[i].startp
            # idea is find component of vector to ball from wall start point along the wall and use pythag to get distance to ball
            lenballtowallvect = (balltowallvect[0]**2 + balltowallvect[1]**2)**0.5
            lenwall = (wallvect[0]**2 + wallvect[1]**2)**0.5
            lenalongwall = np.dot(balltowallvect,wallvect)/lenwall
            if lenalongwall > 0: # component positive means to the right of start
                balltowallvectend = balls[j].pos - walls[i].endp # now check to the left of end
                lenalongwallleft = np.dot(balltowallvectend,wallvect)/lenwall
                if lenalongwallleft < 0:
                    lenballtowall = (lenballtowallvect**2 - lenalongwall**2)**0.5
                    if lenballtowall <= balls[j].rad + 1:
                        tangent = wallvect/lenwall
                        normal = 0*tangent
                        normal[0] = -tangent[1]
                        normal[1] = tangent[0]

                        print(tangent)
                        print(normal)
                        #move the ball away from the wall so collision stops
                        if np.dot(normal,balls[j].vel) <= 0:
                            balls[j].pos += 0.5*balls[j].rad*normal
                        else:
                            balls[j].pos += -0.5*balls[j].rad*normal
                                  
                        newvel = np.dot(balls[j].vel,tangent)*tangent -  np.dot(balls[j].vel,normal)*normal
                        balls[j].vel = newvel             

            # Want to make it so collision with end points of line is like colliding with a ball
            if math.sqrt((walls[i].startp[0]-balls[j].pos[0])**2+(walls[i].startp[1]-balls[j].pos[1])**2) <= 1 + balls[j].rad:
                vdis = balls[j].pos - walls[i].startp
                dist = (vdis[0]**2+vdis[1]**2)**0.5
                unitvect = vdis/dist
                normalvect = 0*unitvect
                normalvect[0] = -unitvect[1]
                normalvect[1] = unitvect[0]
                
                #move the ball away from the wall so collision stops
                balls[j].pos += 0.5*balls[j].rad*unitvect

                newvel = -np.dot(balls[j].vel,unitvect)*unitvect +  np.dot(balls[j].vel,normalvect)*normalvect
                balls[j].vel = newvel   

            if math.sqrt((walls[i].endp[0]-balls[j].pos[0])**2+(walls[i].endp[1]-balls[j].pos[1])**2) <= 1 + balls[j].rad:
                vdis = balls[j].pos - walls[i].endp
                dist = (vdis[0]**2+vdis[1]**2)**0.5
                unitvect = vdis/dist
                normalvect = 0*unitvect
                normalvect[0] = -unitvect[1]
                normalvect[1] = unitvect[0]
                
                #move the ball away from the wall so collision stops
                balls[j].pos += 0.5*balls[j].rad*unitvect

                newvel = -np.dot(balls[j].vel,unitvect)*unitvect +  np.dot(balls[j].vel,normalvect)*normalvect
                balls[j].vel = newvel   
