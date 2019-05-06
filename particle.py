
import numpy as np
import constants as var

class Particle:
    dia = 140.0e-6

    pos = np.array([0,0,0])
    force = np.array([0,0,0])
    momentum = np.array([0,0,0])
    angVel = np.array([0,0,0])
    vel = np.array([0,0,0])

    def __init__(self, pos):
        self.pos = pos
        self.elasticMod = var.ymod/(1.0-pow(var.pois,2))
        
    def resetForces(self):
        self.force = 0.0*self.force
        self.force[2] = -9.81
        self.momentum = 0.0*self.momentum
    # def getCenter(self):
    #     return self.pos

    # def setCenter(ct):
    #     cent = ct
