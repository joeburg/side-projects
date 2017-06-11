#Purpose: program to evaluatet E_pot for a 1D Coulomb chain
#The charge on atoms alternate between +1 and -1
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
rc('mathtext', default='regular')


def Epotential(N):
    R0 = 1;
    E = 0;
    for i in range(1,N+1):
        for j in range(i+1,N+1):
            if (i-j)%2 == 1: 
                q = -1
            else: 
                q = 1
            rij = float(abs(R0*(i-j))) 
            if rij != 0: 
                E = E + q/rij
    return E/N

N = input("What value of N do you want to evaluate E(N)/N? ")
print Epotential(N)

#This program uses the Epotential function above to find 
#when E approaches -ln(2) to both 2 and 3 significant digits 


#E(N)/N within 2 significant digits of -ln(2)
N2 = 1
while Epotential(N2) > -0.685:
    N2 = N2 + 1

print "For E(N)/N within 2 significant digits of -ln(2): N = "+str(N2)
print "E(N)/N ="+str(Epotential(N2))

#E(N)/N within 3 significant digits of -ln(2) 
N3 = N2
while Epotential(N3) > -0.6925:
    N3 = N3 + 1;

print "For E(N)/N within 3 siginifcant digits of -ln(2): N = "+str(N3)
print "E(N)/N ="+str(Epotential(N3))


#plot E(N)/N versus N
E_n = []
N = []
for i in range(1,500):
    E_n = E_n + [Epotential(i)]
    N = N + [i]

plt.figure()
plt.plot(N, E_n)
plt.xlabel('N (atoms)')
plt.ylabel('E(N)/N')
plt.savefig('E_vs_N.png')
    
print "All done!"
