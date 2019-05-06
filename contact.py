
import numpy as np
import parameters as var

def checkZContact(part, fc):
    # Contact with zMin
    gap = -(var.zMin - part.pos[2]) - part.dia*0.5
    uVec = np.array([0,0,1.0])
    if(gap < 0): #If contact exists calculate contact force
       fc.surfaceContactForce(part, -gap, uVec)

    if(gap < part.dia):
        fc.esForce(part, gap)
    if(gap < 100e-9*var.lengthFactor):
        fc.pWallVWForce(part, gap, uVec)
    

    # Contact with zMax wall
    gap = var.zMax - part.pos[2] - part.dia*0.5
    uVec = np.array([0,0,-1.0])

    if(gap < part.dia):
        fc.esForce(part, gap)

    if(gap < 0): #If contact exists calculate contact force
        fc.surfaceContactForce(part, -gap, uVec)
    if(gap < 100.e-9*var.lengthFactor):
        fc.pWallVWForce(part, gap, uVec)
    



