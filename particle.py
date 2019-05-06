
import math
import numpy as np
import parameters as var

class Particle:
    dia = var.largestParDia*var.lengthFactor
    
    pos = np.array([0.0,0.0,0.0])
    force = np.array([0.0,0.0,0.0])
    momentum = np.array([0.0,0.0,0.0])
    angVel = np.array([0.0,0.0,0.0])
    vel = np.array([0.0,0.0,0.0])

    charge = 0.0

    def __init__(self, pos):
        self.mass = (4./3.)*math.pi*pow(0.5*self.dia,3)*var.dens
        self.pos = pos
        self.elasticMod = var.ymod/(1.0-pow(var.pois,2))
        
    def resetForces(self):
        self.force = 0.0*self.force
        self.force[2] = -self.mass
        self.momentum = 0.0*self.momentum

    def move(self):
        dxDot = self.force[0]*var.timeStep/self.mass
        dyDot = self.force[1]*var.timeStep/self.mass
        dzDot = self.force[2]*var.timeStep/self.mass
                    
        self.vel[0] += dxDot
        self.vel[1] += dyDot
        self.vel[2] += dzDot

        dx = self.vel[0]*var.timeStep
        dy = self.vel[1]*var.timeStep
        dz = self.vel[2]*var.timeStep

        # print(dx,dy,dz)
        self.pos[0] += dx
        self.pos[1] += dy
        self.pos[2] += dz
   
