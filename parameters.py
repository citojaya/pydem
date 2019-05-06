import math
import numpy as np

counter = 0

# Simulation conditions
timeStep = 1.0e-6
totalTime = 0.0
zMin = 0
zMax = 100.0

# Particle property
sfc = 0.4
rf = 0.001
dens = 830.0
ymod = 1.0e7
pois = 2.9e-1
dmpn = 20.0E-4
ha = 0.0 #6.5e-21
gravity = 9.81
largestParDia = 2.0e-3

# Fluid property
fvisc = 1.7894e-05 #(kg/m-s)
fdens = 1.225 #(kgm-3)
por = 0.8
fvel = np.array([0.0,0.0,0.0])

#Electrostatic force parameters
Vi = 4.7 #Work function of wall (Volt)
Vj = 4.52 #Work function of particle (Volt)
eps = 8.885e-12 #permitivity of air (C^2/N.m^2)
chargingConst = 1.e-4 # charging constant (C.m^-2.V^-1)


refLength = largestParDia
refDensity = dens
lengthFactor = 1.0/refLength
volumeFactor = pow(lengthFactor,3)
massFactor = 6.0/(math.pi*pow(refLength,3)*refDensity)
timeFactor = np.sqrt(gravity/refLength)
densityFactor = 6.0/(math.pi*refDensity)
forceFactor = 6.0/(gravity*math.pi*pow(refLength,3)*refDensity)
pressureFactor = 6.0/(gravity*math.pi*refLength*refDensity)
StressFactor = pressureFactor
energyFactor = 6.0/(gravity*math.pi*pow(refLength,4)*refDensity)
momentFactor = energyFactor
powerFactor = 6.0/(pow(gravity,1.5)*math.pi*pow(refLength,3.5)*refDensity)
velocityFactor = 1.0/np.sqrt(refLength*gravity)
accFactor = 1.0/gravity
angVelFactor = np.sqrt(refLength/gravity)
angAccFactor = refLength/gravity
freqFactor = np.sqrt(refLength/gravity)
inertiaFactor = 6.0/(math.pi*pow(refLength,5)*refDensity)

cutGap = 1.2*largestParDia*lengthFactor

dsmaxCff = sfc*(2.0-pois)/(2.0*(1.0-pois))

dens = dens*densityFactor
ymod = ymod*pressureFactor
timeStep = timeStep*timeFactor
ha = ha*forceFactor*lengthFactor
elasticMod = ymod/(1.0-pow(pois,2))

fvisc = fvisc*massFactor/(lengthFactor*timeFactor)
fdens = fdens*densityFactor
fvel = fvel*velocityFactor

zMin = zMin*lengthFactor
zMax = zMax*lengthFactor