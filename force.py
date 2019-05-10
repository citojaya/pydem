import math
import numpy as np
import parameters as var

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
    temp = 0.0
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
  nrmDampForce = -var.dmpn*var.elasticMod*np.sqrt(rStar*nrmDisp)*nrmVel

  cntPntDisp = var.timeStep*cntPntVel
  tipCntPntDisp = projVec(cntPntDisp, uVec, 0)
  slidingDisp = np.linalg.norm(tipCntPntDisp)

  disp = tipCntPntDisp
  dsmax = var.dsmaxCff*nrmDisp

  dd = np.linalg.norm(disp)
  dti = np.linalg.norm(tipCntPntDisp)
  fdt = var.sfc*nrmCntForce

  fdtVec = np.array([0.0,0.0,0.0])

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

  # print("part.elasticMod", cntPntDisp)

def dragForce(part):
  relVelMag = np.linalg.norm(np.subtract(var.fvel,part.vel))
  Re = var.por*part.dia*relVelMag*var.fdens/var.fvisc

  beta = 0.0
  dCoeff = 0.0
  #-- Standard equations --
  if(Re < 1000):
		dCoeff = 24.*(1.+0.15*pow(Re, 0.687))/Re
  else:
		dCoeff = 0.44

  # Yi He paper
  if(var.por <= 0.8):
    beta = 150.*(1.-var.por)*(1.-var.por)*var.fvisc/(var.por*pow(part.dia,2))\
                + 1.75*(1.-var.por)*var.fdens*relVelMag/part.dia
  elif(var.por > 0.8):
    beta = (3.0/4.0)*dCoeff*relVelMag*var.fdens*(1.0-var.por)*pow(var.por,-2.7)/part.dia

  partVol = (4./3.)*math.pi*pow(0.5*part.dia,3)

  # particle fluid force
  pfF = np.subtract(var.fvel, part.vel)*partVol*beta/(1.0-var.por)
  # print("fluid vel",var.fvel)

  #pressure gradient
  pG = np.array([0.0,0.0,0.0])
  pGF = -pG*math.pi*pow(part.dia,3)/6.0

  #Update forces on particles
  part.force += pfF + pGF
  part.force[2] += partVol*var.fdens

  # print("dragForce", relVelMag)

def pWallVWForce(part, vGap, uVec):
  vGapMn = 1.0e-9*var.lengthFactor
  if(vGap < vGapMn):
    vGap = vGapMn

    fv = -var.ha*part.dia*0.5/(6.*vGap*vGap)
    var.maxVWForce = max(var.maxVWForce,-fv)
    # print("VANDERWAAL FORCE",fv/var.forceFactor)

    part.force[0] += uVec[0]*fv
    part.force[1] += uVec[1]*fv
    part.force[2] += uVec[2]*fv  

def esForce(part, vGap, uVec):
    gap = max(vGap/var.lengthFactor, 0.01e-6)
    esF = part.charge*part.charge/(4.0*math.pi*var.eps*gap)
    var.maxESForce = max(var.maxESForce,esF)
    # print("ELC FORCE , MG FORCE",esF, part.mass/var.forceFactor)
    
    # part.force[0] += uVec[0]*esF
    # part.force[1] += uVec[1]*esF
    # part.force[2] += uVec[2]*esF  

def charge(part, gap):
  velMag = np.linalg.norm(part.vel)
  parR = part.dia*0.5
  ymod = var.ymod
  dens = var.dens

  z0 = 1.0e-6

  k0 = z0/(4.*math.pi*var.eps*pow(parR/var.lengthFactor,2)) #constant
  
  vDash = k0*part.charge

  emod = (1.0-var.pois*var.pois)/ymod
  S = 1.36*pow(emod, 2.0/5.0)*pow(dens,2.0/5.0)*pow(parR*2.0,2)*pow(velMag,4.0/5.0)
  S = S/(var.lengthFactor*var.lengthFactor)
  
  part.cntArea = S
 
  deltaV = var.Vi - var.Vj - vDash
  part.voltage = abs(vDash)
  
  # deltaQ = S*deltaV*var.rel_perm*var.eps/z0 #(Matsusaka et al, 2000)
  deltaQ = var.chargingConst*S*deltaV #(thesis)
  
  part.charge += deltaQ
  # print("charge",part.charge)





