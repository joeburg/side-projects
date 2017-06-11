# ------------------------------------------------------------------------
# Model a gas using the Lennard-Jones potential and periodic boundary conditions
#
# Implementation from:
#   University of Illinois: PHY466/MSE485 Atomic Scale Simulations
# ------------------------------------------------------------------------


import numpy
import math
import random
import time

# Everyone will start their gas in the same initial configuration.
# ------------------------------------------------------------------------

def InitPositionCubic(N,L):
  position = numpy.zeros((N,3)) + 0.0  # N lists with 3 elements inside
  Ncube = 1                            # position is an ARRAY
  while(N > (Ncube*Ncube*Ncube)):
    Ncube += 1
  if(Ncube**3 != N):
    print "CubicInit Warning: Your particle number",N, \
          "is not a perfect cube; this may result " \
          "in a lousy initialization"
  rs = float(L)/Ncube
  roffset = float(L)/2 - rs/2
  added = 0
  for x in range(0, Ncube):
    for y in range(0, Ncube):
      for z in range(0, Ncube):
        if(added < N):
          position[added, 0] = rs*x - roffset # the added list ''0'' element.
          position[added, 1] = rs*y - roffset 
          position[added, 2] = rs*z - roffset 
          added += 1
  return position

def InitVelocity(N,T0,mass=1.):
  initNDIM = 3
  velocity = numpy.zeros((N,3)) + 0.0 # generate N lists with 3 elements.
  random.seed(1)
  netP = numpy.zeros((3,)) + 0. # generate 1 list with 3 elements.
  netE = 0.0
  for n in range(0, N):
    for x in range(0, initNDIM):
      newP = random.random()-0.5 # generate a random number from -0.5 to 0.5.
      netP[x] += newP
      netE += newP*newP
      velocity[n, x] = newP
  netP *= 1.0/N
  vscale = math.sqrt(3*N*T0/(mass*netE))
  for n in range(0, N):
    for x in range(0, initNDIM):
      velocity[n, x] = (velocity[n, x] - netP[x]) * vscale # gaurantee the added total velocity is zero.
  return velocity


# You may adjust the gas properties here.
# ------------------------------------------------------------------------

# mass
M = 48.0

# number of Particles
N = 64
##N = 512

# box side length
L = 4.2323167
##L = 8.4646344

# temperature
T0 = 0.728


# Routines to ensure periodic boundary coditions.
# ------------------------------------------------------------------------

def PutInBox(Ri):

  # Ri[0] is the x coordinate of the ith particle.
  # Similarly, Ri[1] (or Ri[2]) is the y (or z) coordinate.

  # Using periodic boundary conditions, redefine Ri so that it is in a box
  # of side length L centered about about the origin.

  return (Ri-(numpy.round(Ri/L)*L))

def Distance(Ri,Rj):

  # Again, Ri is the position vector of the ith particle.
  # return the distance between particle i and j according to the minimum
  # image convention.

  d=numpy.sqrt(numpy.sum(PutInBox(Ri-Rj)**2))
  return d

def Displacement(Ri, Rj):

  # Return the displacement of the ith particle relative to the jth 
  # particle according to the minimum image convention. Unlike the 'Distance'
  # function above, here you are returning a vector.

  dis=PutInBox(Ri-Rj)
  return dis


# The Verlet time-stepping algorithm, 'h' is the time step.
# ------------------------------------------------------------------------

h=0.01
def VerletNextR(r_t,v_t,a_t):
  
  r_t_plus_h = [0.0, 0.0, 0.0]
  r_t_plus_h[0] = r_t[0] + v_t[0]*h + 0.5*a_t[0]*h*h
  r_t_plus_h[1] = r_t[1] + v_t[1]*h + 0.5*a_t[1]*h*h
  r_t_plus_h[2] = r_t[2] + v_t[2]*h + 0.5*a_t[2]*h*h
  return r_t_plus_h

def VerletNextV(v_t,a_t,a_t_plus_h):

  v_t_plus_h = [0.0, 0.0, 0.0]  
  v_t_plus_h[0]=v_t[0]+0.5*(a_t[0]+a_t_plus_h[0])*h # velocity Verlet mothed.
  v_t_plus_h[1]=v_t[1]+0.5*(a_t[1]+a_t_plus_h[1])*h
  v_t_plus_h[2]=v_t[2]+0.5*(a_t[2]+a_t_plus_h[2])*h
  return v_t_plus_h

# Compute the forces
# ------------------------------------------------------------------------

def Potential(r):
  # Lennard-Jones potential
  r6=r**6; r12=r6**2
  return 4*(1.0/r12-1.0/r6)

def GetForce(Ri,Rj):
  
  #calculate the force between particle i and j
  r=Distance(Ri,Rj)
  Disp=Displacement(Ri,Rj)
  r2=r*r
  r2i=1.0/r2
  r6i=r2i**3
  F=numpy.zeros(3)
  for i in range(0,3):
    F[i]=24*r6i*r2i*(2*r6i-1)*Disp[i]
  return F
# ------------------------------------------------------------------------

def InternalForce(i, R):

  # We want to return the force on atom 'i' when we are given a list of 
  # all atom positions in 'R'. Note R[0] is the position vector of the 
  # 1st atom. And R[0][0] is the x coordinate of the 1st atom. It may
  # be convenient to use the 'Displacement' function above. For example,
  # D = Displacement( R[0], R[1] ) would give the position of the 1st atom
  # relative to the 2nd. And D[0] would then be the x coordinate of this 
  # displacement. Use the Lennard-Jones pair interaction. Be sure to avoid 
  # computing the force of an atom on itself. 

  F = [0.0, 0.0, 0.0]

  # <-- find force on ith atom here -->
  for j in range (0,N):
    if j != i:
      dF= GetForce(R[i],R[j]) #R[i] is the ith list with 3 elements inside 
                              #R[i,1] ,R[i,2] and R[i,3].      
      for k in range(0,3):
        F[k]+= dF[k]
 
  return F


# Some instantaneous properties of the system.
# ------------------------------------------------------------------------

def ComputeEnergy(R, V):

  totalKE = 0.0
  totalU  = 0.0

  # Find the total kinetic and potential energies of the system. Here
  # R and V are the position and velocities of all the atoms in the gas
  # as described in the 'InternalForce' routine.

  # <-- find totalKE, totalU. -->
  for i in range(0,N):
    totalKE += 0.5*M*(V[i,0]*V[i,0]+V[i,1]*V[i,1]+V[i,2]*V[i,2])
    for j in range(0,i):
      totalU += Potential(Distance(R[i],R[j])) 
  totalE = totalKE + totalU
  return totalU, totalKE, totalE


# Main Loop.  
# ------------------------------------------------------------------------

# R, V, and A are the position, velocity, and acceleration of the atoms
# respectively. nR, nV, and nA are the _next_ positions, velocities, etc.
# You can adjust the total number of timesteps here. 


def WriteSoln(R,V,N):
  filename = "solution0.dat"
  f = open(filename, 'a')
  f.write('0\n')
  for i in range(N):
    f.write('%.30f  %.30f  %.30f  %.30f  %.30f  %.30f\n' \
            %(R[i][0],R[i][1],R[i][2],V[i][0],V[i][1],V[i][2]))
  f.close()

t0 = time.time()

R = numpy.zeros((N,3)) + 0.0
V = numpy.zeros((N,3)) + 0.1
A = numpy.zeros((N,3))

nR = numpy.zeros((N,3))
nV = numpy.zeros((N,3))

R = InitPositionCubic(N, L)
V = InitVelocity(N, T0, M)

##WriteSoln(R,V,N)

steps = 1000
##steps = 10
for t in range(0,steps):
  
  computedE =  ComputeEnergy(R,V)

  print '%d %.10f %.10f %.10f' %(t, computedE[0],computedE[1],computedE[2])

  for i in range(0,len(R)):
    
    F    = InternalForce(i, R)
    A[i] = [ F[0]/M, F[1]/M, F[2]/M ]
    
    nR[i] = VerletNextR( R[i], V[i], A[i] )

  for i in range(0,len(R)):
    
    nF = InternalForce(i, nR)
    nA = [ nF[0]/M, nF[1]/M, nF[2]/M ]
  
    nV[i] = VerletNextV( V[i], A[i], nA )
    
  R = nR.copy()
  V = nV.copy()

elapsedtime = time.time() - t0
print 'Elapsed time %.4f seconds.' %elapsedtime
