
import numpy as np
import constants as var

# def crossProd():
# def projVec():

def projVec(v, n, tp):
  if(tp == 0):
    tV1 = np.cross(n,v)
    tV2 = -n
    vec = np.cross(tV2,tV1)

  else:
    tV1 = np.cross(n,v)
    tV2 = -n
    tV3 = np.cross(tV2,tV1)
    temp = 0
    if(np.linalg.norm(v) != 0.0):
      temp = np.sqrt((tV3[0]*tV3[0]+tV3[1]*tV3[1]+tV3[2]*tV3[2])/
                            (v[0]*v[0]+v[1]*v[1]+v[2]*v[2]))
    vec = temp*tV3
  return vec


def surfaceContactForce(part, nrmDisp, uVec):
  rStar = 0.5*part.dia
  ipRVec = -0.5*part.dia*uVec
  rotVel = np.cross(part.angVel, ipRVec)
  ipCntPntVel = np.add(part.vel, rotVel)

  relVel = part.vel
  nrmVel = np.dot(relVel, uVec)
  cntPntVel = ipCntPntVel

  nrmCntForce = part.elasticMod*np.sqrt(rStar*nrmDisp)*nrmDisp
  nrmDampForce = -var.dmpn*part.elasticMod*np.sqrt(rStar*nrmDisp)*nrmVel

  cntPntDisp = var.timeStep*cntPntVel
  tipCntPntDisp = projVec(cntPntDisp, uVec, 0)
  slidingDisp = np.linalg.norm(tipCntPntDisp)

  disp = tipCntPntDisp
  dsmax = var.dsmaxCff*nrmDisp

  dd = np.linalg.norm(disp)
  dti = np.linalg.norm(tipCntPntDisp)
  fdt = var.sfc*nrmCntForce

  fdtVec = np.array([0,0,0])

  if(dd<1e-6):
    dd = 0.0
  if(dti < 1e-6):
    dti = 0.0

  if(dd >= dsmax):
    disp = (dsmax/dd)*disp
    if(dti != 0):
      fdtVec = -fdt/dti*tipCntPntDisp
    else:
      fdtVec = 0.0*fdtVec
  else:
    if(dd != 0.0):
      fdt = fdt*(1.0 - pow((1.0 - dd/dsmax),1.5))
      fdtVec = -fdt/dd*disp
    else:
      fdtVec = 0.0*fdtVec

  nrmForce = (nrmCntForce + nrmDampForce)
  totalForce = nrmForce*uVec
  totalForce = np.add(totalForce,fdtVec)
  momentum = np.cross(ipRVec, totalForce)
  rotMom = 0.5*var.rf*part.dia*nrmCntForce*part.angVel
  momentum = np.add(momentum, rotMom)

  part.force = np.add(part.force, totalForce)
  part.momentum = np.add(part.momentum, momentum)


  


  print("part.elasticMod", cntPntDisp)

def dragForce():
  print("dragForce")

def pWallVWForce(part, gap, uVec):
  print("pWallVWForce")

def esForce():
  print("eSForce")

def move(part):
  print("move")





