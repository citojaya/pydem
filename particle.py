import numpy as np

class Particle:
    dia = 140.0e-6
    dens = 830.0
    youngs = 1.0e7
    pois = 2.9e-1
    damp = 0.3
    ha = 6.5e-19

    cent = np.array([0,0,0])

    def __init__(self, cent):
        self.cent = cent
    
    def getCenter(self):
        return self.cent

    # def setCenter(ct):
    #     cent = ct
