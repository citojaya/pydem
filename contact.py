
import numpy as np
import parameters as var

def checkZContact(part, fc):
    # Contact with zMin
    gap = -(var.zMin - part.pos[2]) - part.dia*0.5
    uVec = np.array([0,0,1.0])
    if(gap < 0): #If contact exist calculate force
        fc.surfaceContactForce(part, -gap, uVec)
        if(var.incontact == False):
            fc.charge(part, gap)
            fout1 = open("particle_charge.dat","a")
            line = str(round(var.totalTime/var.timeFactor,4))+" "+\
            str(round(1e3*part.pos[2]/var.lengthFactor,3))+" "+\
            str(round(part.charge*1e12,5))  
            fout1.write(line+"\n")
            fout1.close()
            print(line)
            var.incontact = True
    else:
        var.incontact = False

    if(gap < 100e-9*var.lengthFactor):
        fc.pWallVWForce(part, gap, uVec)
    

    # Contact with zMax wall
    gap = var.zMax - part.pos[2] - part.dia*0.5
    uVec = np.array([0,0,-1.0])

    if(gap < part.dia):
        fc.charge(part, gap)

    if(gap < 0): #If contact exists calculate contact force
        fc.surfaceContactForce(part, -gap, uVec)
        if(var.incontact == False):
            fc.esForce(part, gap)
            var.incontact = True
    else:
        var.incontact = False
    if(gap < 100.e-9*var.lengthFactor):
        fc.pWallVWForce(part, gap, uVec)
    



