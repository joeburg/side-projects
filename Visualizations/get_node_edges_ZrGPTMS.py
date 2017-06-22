#Purpose: find the bonds, angles in Zr/GPTMS .xyz outpuf file from simulation 

from Tkinter import Tk
from tkFileDialog import askopenfilename
Tk().withdraw()

from pylab import *
from scipy import *
from numpy import *
import numpy as np
import math


################################################################################
################################################################################
def distance(x1,x2,y1,y2,z1,z2):
    d = ((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)**0.5
    return d

def magnitude(x,y,z):
    mag = (x**2 + y**2 + z**2)**0.5
    return mag

def dist(dx,dy,dz):
    d = (dx**2+dy**2+dz**2)**0.5
    return d

################################################################################
################################################################################
#import data
filename = askopenfilename()
print "Working with file:", filename

atom_data = []
with open(filename) as inputfile:
    for line in inputfile:
        atom_data.append(line.strip().split( ))

#access number of atoms from file and remove first 2 lines 
N_atoms = int(atom_data[0][0])
atom_data = atom_data[2:]

#transpose data into columns
atom_data = [list(x) for x in zip(*atom_data)]

for i in range(len(atom_data)):
    for j in range(N_atoms):
        atom_data[i][j] = float(atom_data[i][j])

#create first column to index the atoms (0 to N_atoms-1)
atom_index = []
for i in range(N_atoms):
    atom_index.append(i)

#access column to get specific data
atom_type = atom_data[0]
x_coord = atom_data[1]
y_coord = atom_data[2]
z_coord = atom_data[3]

x_min = min(x_coord)
x_max = max(x_coord)
Lx = x_max - x_min

y_min = min(y_coord)
y_max = max(y_coord)
Ly = y_max - y_min

z_min = min(z_coord)
z_max = max(z_coord)
Lz = z_max - z_min


print ''
print 'Data imported!'

################################################################################
#write index and atom type to file (node data)

node_data = []
for i in range(len(atom_type)):
    if atom_type[i]==1:
        node_data.append([str(atom_index[i]),'O'])
    elif atom_type[i]==2:
        node_data.append([str(atom_index[i]),'Si'])
    elif atom_type[i]==3:
        node_data.append([str(atom_index[i]),'C'])
    elif atom_type[i]==4:
        node_data.append([str(atom_index[i]),'Zr'])
    elif atom_type[i]==5:
        node_data.append([str(atom_index[i]),'Q'])

node_data = [['Id','Label']]+node_data
        
dataFile1 = open(filename[:-4]+"_nodes.csv", 'w')
for eachitem in node_data:
    dataFile1.write(",".join(eachitem)+'\n')

dataFile1.close()

print ''
print "Nodes finished!"

################################################################################
#get bonds and make them edges: [source, target]

print ''
print 'Finding bonds...'

edge_data = []
for i in range(N_atoms):
    index1 = atom_index[i]
    atom1 = atom_type[i]
    x1 = x_coord[i]
    y1 = y_coord[i]
    z1 = z_coord[i]
    for j in range(i+1,N_atoms):
        index2 = atom_index[j]
        atom2 = atom_type[j]
        x2 = x_coord[j]
        y2 = y_coord[j]
        z2 = z_coord[j]

        dx = abs(x1-x2)
        dy = abs(y1-y2)
        dz = abs(z1-z2)

        #determine C-C bonds (only bonded on chains); cutoff 2.0A
        if atom1==3 and atom2==3:
            d = dist(dx,dy,dz)
            if d<=2.0:
                edge = [str(index1),str(index2)]
                if edge not in edge_data:
                    edge_data.append(edge)

            #account for PBCs
            if dx > Lx-2.0:
                d = dist(dx+Lx,dy,dz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx-Lx,dy,dz)
                if d <= 2.0:                       
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

            if dy > Ly-2.0:
                d = dist(dx,dy+Ly,dz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx,dy-Ly,dz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

            if dz > Lz-2.0:
                d = dist(dx,dy,dz+Lz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx,dy,dz-Lz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)                  

        #determine C-Q bonds (next to each other in chain); cutoff 2.0A
        elif (atom1==3 and atom2==5) or (atom1==5 and atom2==3):
            d = dist(dx,dy,dz)
            if d<=2.0:
                edge = [str(index1),str(index2)]
                if edge not in edge_data:
                    edge_data.append(edge)

            #account for PBCs
            if dx > Lx-2.0:
                d = dist(dx+Lx,dy,dz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx-Lx,dy,dz)
                if d <= 2.0:                       
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

            if dy > Ly-2.0:
                d = dist(dx,dy+Ly,dz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx,dy-Ly,dz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

            if dz > Lz-2.0:
                d = dist(dx,dy,dz+Lz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx,dy,dz-Lz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

        #determine C-Si bonds (next to each other in chain); cutoff 2.3A
        elif (atom1==3 and atom2==1) or (atom1==1 and atom2==3):
            d = dist(dx,dy,dz)
            if d<=2.3:
                edge = [str(index1),str(index2)]
                if edge not in edge_data:
                    edge_data.append(edge)

            #account for PBCs
            if dx > Lx-2.3:
                d = dist(dx+Lx,dy,dz)
                if d <= 2.3:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx-Lx,dy,dz)
                if d <= 2.3:                       
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

            if dy > Ly-2.3:
                d = dist(dx,dy+Ly,dz)
                if d <= 2.3:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx,dy-Ly,dz)
                if d <= 2.3:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

            if dz > Lz-2.3:
                d = dist(dx,dy,dz+Lz)
                if d <= 2.3:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx,dy,dz-Lz)
                if d <= 2.3:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

        #determine Si-O bonds; cutoff at 2.0A; as a slight overestimate, we can say
        # that if the difference in the x-coords is <= 2.0 (we assume that y and z
        # coord are 0) then we will calculate the distance 
        elif (atom1==1 and atom2==2) or (atom1==2 and atom2==1):
            d = dist(dx,dy,dz)
            if d<=2.0:
                edge = [str(index1),str(index2)]
                if edge not in edge_data:
                    edge_data.append(edge)

            #account for PBCs
            if dx > Lx-2.0:
                d = dist(dx+Lx,dy,dz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx-Lx,dy,dz)
                if d <= 2.0:                       
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

            if dy > Ly-2.0:
                d = dist(dx,dy+Ly,dz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx,dy-Ly,dz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

            if dz > Lz-2.0:
                d = dist(dx,dy,dz+Lz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx,dy,dz-Lz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)


        #determine Q-Q bonds; cuttoff at 2.0A; take difference in x-coord <=2.0
        elif (atom1==5 and atom2==5):
            d = dist(dx,dy,dz)
            if d<=2.0:
                edge = [str(index1),str(index2)]
                if edge not in edge_data:
                    edge_data.append(edge)

            #account for PBCs
            if dx > Lx-2.0:
                d = dist(dx+Lx,dy,dz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx-Lx,dy,dz)
                if d <= 2.0:                       
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

            if dy > Ly-2.0:
                d = dist(dx,dy+Ly,dz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx,dy-Ly,dz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

            if dz > Lz-2.0:
                d = dist(dx,dy,dz+Lz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx,dy,dz-Lz)
                if d <= 2.0:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)           


        #determine Zr-O bonds; cutoff at 2.3A (Note: clustering affect will
        # change the amount of calculated bonds - some atoms within cutoff that
        # arnt actually bonded - source of error)
        elif (atom1==2 and atom2==4) or (atom1==4 and atom2==2):
            d = dist(dx,dy,dz)
            if d<=2.3:
                edge = [str(index1),str(index2)]
                if edge not in edge_data:
                    edge_data.append(edge)

            #account for PBCs
            if dx > Lx-2.3:
                d = dist(dx+Lx,dy,dz)
                if d<=2.3:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx-Lx,dy,dz)
                if d<=2.3:                       
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

            if dy > Ly-2.3:
                d = dist(dx,dy+Ly,dz)
                if d<=2.3:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx,dy-Ly,dz)
                if d<=2.3:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

            if dz > Lz-2.3:
                d = dist(dx,dy,dz+Lz)
                if d<=2.3:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)

                d = dist(dx,dy,dz-Lz)
                if d<=2.3:
                    edge = [str(index1),str(index2)]
                    if edge not in edge_data:
                        edge_data.append(edge)
                        

##        #determine C-C bonds (only bonded on chains); cutoff 2.0A
##        if atom1==3 and atom2==3:
##            if abs(index1-index2)<10:
##                d = distance(x1,x2,y1,y2,z1,z2)
##                if d<=2.0:
##                    edge = [str(index1),str(index2)]
##                    if edge not in edge_data:
##                        edge_data.append(edge)
##
##        #determine C-Q bonds (next to each other in chain); cutoff 2.0A
##        elif (atom1==3 and atom2==5) or (atom1==5 and atom2==3):
##            if abs(index1-index2)==1:
##                d = distance(x1,x2,y1,y2,z1,z2)
##                if d<=2.0:
##                    edge = [str(index1),str(index2)]
##                    if edge not in edge_data:
##                        edge_data.append(edge)
##
##        #determine C-Si bonds (next to each other in chain); cutoff 2.3A
##        elif (atom1==3 and atom2==1) or (atom1==1 and atom2==3):
##            if abs(index1-index2)==1:
##                d = distance(x1,x2,y1,y2,z1,z2)
##                if d<=2.3:
##                    edge = [str(index1),str(index2)]
##                    if edge not in edge_data:
##                        edge_data.append(edge)
##
##        #determine Si-O bonds; cutoff at 2.0A; as a slight overestimate, we can say
##        # that if the difference in the x-coords is <= 2.0 (we assume that y and z
##        # coord are 0) then we will calculate the distance 
##        elif (atom1==1 and atom2==2) or (atom1==2 and atom2==1):
##            if abs(x1-x2)<=2.0:
##                d = distance(x1,x2,y1,y2,z1,z2)
##                if d<=2.0:
##                    edge = [str(index1),str(index2)]
##                    if edge not in edge_data:
##                        edge_data.append(edge)
##                
##        #determine Q-Q bonds; cuttoff at 2.0A; take difference in x-coord <=2.0
##        elif (atom1==5 and atom2==5):
##            if abs(x1-x2)<=2.0:
##                d = distance(x1,x2,y1,y2,z1,z2)
##                if d<=2.0:
##                    edge = [str(index1),str(index2)]
##                    if edge not in edge_data:
##                        edge_data.append(edge)
##
##        #determine Zr-O bonds; cutoff at 3.0A
##        elif (atom1==2 and atom2==4) or (atom1==4 and atom2==2):
##            if abs(x1-x2)<=3.0:
##                d = distance(x1,x2,y1,y2,z1,z2)
##                if d<=3.0:
##                    edge = [str(index1),str(index2)]
##                    if edge not in edge_data:
##                        edge_data.append(edge)

edge_data = [['Source','Target']] + edge_data

dataFile2 = open(filename[:-4]+"_edges.csv", 'w')
for eachitem in edge_data:
    dataFile2.write(",".join(eachitem)+'\n')

dataFile2.close()

print ''
print "Nodes finished!"

print 'All done!'
