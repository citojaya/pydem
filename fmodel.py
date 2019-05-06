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


def simulate(count, zMin ,zMax):
  part.resetForces()
  cn.checkZContact(part, fc, zMin, zMax)

  #   dragForce()
#   vwForce()
#   esForce()
  print("Cycle ", count)

  

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
zMax = 100

# Set particle center
part = Particle(np.array([0,0,0]))
# print("Particle center", part.getCenter())

count = 0

# Simulation loop
for i in range(int(iterations)):
  simulate(count, zMin, zMax)
  count += 1




print("DONE")
