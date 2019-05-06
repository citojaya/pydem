
import numpy as np

def checkZContact(part, fc, zMin, zMax):
    # Contact with zMin
    gap = -(zMin - part.pos[2]) - part.dia*0.5
    uVec = np.array([0,0,1.0])
    if(gap < 0): #If contact exists calculate contact force
       fc.surfaceContactForce(part, -gap, uVec)

    if(gap < 100e-9):
        fc.pWallVWForce(part, gap, uVec)
    # Contact with zMax wall
    gap = zMax - part.pos[2] - part.dia*0.5
    uVec = np.array([0,0,-1.0])
    if(gap < 0): #If contact exists calculate contact force
        fc.surfaceContactForce(part, -gap, uVec)
    if(gap < 100.e-9):
        fc.pWallVWForce(part, gap, uVec) 


