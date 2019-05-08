import os
import sys

import re
from optparse import OptionParser, OptionValueError

import numpy as np
import force as fc
import contact as cn
from particle import Particle

import glob
import vtk
from vtk.util import numpy_support
import parameters as var


def simulate(count):
  part.resetForces()
  cn.checkZContact(part, fc)
  fc.elecForce(part)
# fc.dragForce(part)

  part.move()
  
  var.totalTime += var.timeStep
  
  if(var.counter%500 == 0):
    
    fout = open("particle.dat", "a")
    fout.write("TIME = "+str(round(var.totalTime/var.timeFactor, 4))+"\n")
    line = str(round(part.pos[0]*1e3,3))+" "+\
        str(round(part.pos[1]/var.lengthFactor*1e3,3))+" "+\
        str(round(part.pos[2]/var.lengthFactor*1e3,3))+" "+\
        str(round(part.vel[0]/var.velocityFactor,3))+" "+\
        str(round(part.vel[1]/var.velocityFactor,3))+" "+\
        str(round(part.vel[2]/var.velocityFactor,3))+" "+\
        str(round(part.dia*1e3/var.lengthFactor,4))
    fout.write(line+"\n")

    fout.close()
    print(str(round(var.totalTime/var.timeFactor, 4)),\
      str(round(part.pos[2]/var.lengthFactor*1e3,3)),\
      str(var.maxESForce/var.forceFactor),
      str(var.maxVWForce/var.forceFactor))
    
  var.counter += 1

  

# parse command line
p = OptionParser(usage="""usage: %prog [options] Testing for forces used in CFD+DEM model

""")
p.add_option("-v", action="store_true", dest="verbose",  help="Verbose")
(opts, args) = p.parse_args()

# Get the arguments
if len(args) != 1:
  print ("Program must be called with 1 argument")
  p.print_help()
  sys.exit(1)
(iterations) = args[0]


# Boundary
zMin = 0
zMax = 100e-3*var.lengthFactor


# Set particle center
part = Particle(np.array([0.0,0.0,3.0e-3*var.lengthFactor]))
# print("Particle center", part.getCenter())

count = 0

# Simulation loop
for i in range(int(iterations)):
  simulate(count)
  count += 1




print("DONE")
