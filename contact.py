
import numpy as np
import parameters as var

def checkZContact(part, fc):
    # Contact with zMin
    gap = -(var.zMin - part.pos[2]) - part.dia*0.5
    uVec = np.array([0,0,1.0])
    if(gap < 0): #If contact exists calculate contact force
        fc.surfaceContactForce(part, -gap, uVec)
        if(part.zMinContact == False):
            fout1 = open("particle_charge.dat","a")
            fc.charge(part, gap)
            line = str(round(var.totalTime/var.timeFactor,4))+" "+\
               str(round(part.charge*1e9,5))+" "+str(round(1e3*part.voltage, 10))
            fout1.write(line+"\n")
            print(line)
            fout1.close()
            part.zMinContact = True
    else:
        part.zMinContact = False

    if(gap < 100e-9*var.lengthFactor):
        fc.pWallVWForce(part, gap, uVec)
    
    if(gap < part.dia*2.0):
        fc.esForce(part, gap, uVec)


    # Contact with zMax wall
    gap = var.zMax - part.pos[2] - part.dia*0.5
    uVec = np.array([0,0,-1.0])

    if(gap < part.dia):
        fc.esForce(part, gap)

    if(gap < 0): #If contact exists calculate contact force
        fc.surfaceContactForce(part, -gap, uVec)
        if(part.zMaxContact == False):
            fc.charge(part, gap)
            part.zMaxContact = True
    else:
        var.zMaxContact = False
    if(gap < 100.e-9*var.lengthFactor):
        fc.pWallVWForce(part, gap, uVec)
    



