# Program to process data from steady state heat equation

import numpy
import pylab
from scipy import stats
import sys

##################################################################################

def Load_input_file(inputfile):
    f = open(inputfile)
    i = 0
    for line in f:
        line = line.strip().split()
        if i == 0:
            length = float(line[0])
            width = float(line[1])
            h = float(line[2])
            i += 1
        else:
            T_c = int(line[0])
            T_h = int(line[1])
    f.close()
    return length, width, h, T_c, T_h

def Load_solution_file(solnfile):
    # use numpy to read columns in file
    temps = numpy.loadtxt(solnfile, dtype=numpy.float64)
    return temps

def Get_mesh(length, width, h):
    x_coords = numpy.arange(0, length+h, h)
    y_coords = numpy.arange(0, width+h, h)
    x_coords, y_coords = numpy.meshgrid(x_coords,y_coords)
    return x_coords, y_coords

def Add_Boundary(length, width, h, T_c, T_h, temps):
    # mesh shape
    nx = int(length/h + 1)
    ny = int(width/h + 1)
    
    # make arrays for lower boundary (T_c)
    T_l = []
    for i in range(int(length/h+1)):
        T_l.append(-T_c*(numpy.exp(-10*numpy.power(i*h - length/2,2))-2))
    T_l = numpy.array(T_l)
     
    # make arrays for upper boundary (T_h)
    T_u = numpy.empty(length/h+1)
    T_u.fill(T_h)

    # add boundary arrays to interior arrays
    temps = numpy.append(T_l,temps)
    temps = numpy.append(temps,T_u)
    temps = temps.reshape(ny,nx)
    return temps

def Compute_Isoline(temps,x_coords,y_coords,Tavg,h):
    y_iso = []
    for i in range(len(temps[0])):
        # find where Tavg will be in each column
        posR = numpy.searchsorted(temps[:,i],Tavg)
        # find line between bounding points to estimate y_avg
        m = (temps[posR,i]-temps[posR-1,i-1]) / (posR*h - (posR-1)*h)
        b = -m*(posR*h) + temps[posR,i]
        y_avg = (Tavg - b)/m
        y_iso.append(y_avg)
    return y_iso
    
def Pseudocolor_plot(x_coords,y_coords,temps,Tavg,y_iso,length,width,h):
    # generate x coords for isoline plot
    x_iso = numpy.arange(0,length+h,h)

    # create pseudocolor plot with isoline 
    pylab.figure(1)
    pylab.plot(x_iso,y_iso,'k-',linewidth=2.5)
    pylab.pcolor(x_coords,y_coords,temps)
    pylab.colorbar()
    pylab.axis([0,length,-0.2,width+0.2])
    pylab.show(block=False)

##################################################################################
#import data from command line

##if len(sys.argv) < 3:
##  print "Usage:"
##  print "   python %s <input file> <solution file>" % sys.argv[0]
##  exit()
##
##inputfile = sys.argv[1]
##solnfile = sys.argv[2]

##inputfile = 'input_h.txt'
##solnfile = 'solution018.txt'
##
inputfile = 'input2.txt'
solnfile = 'solution2_158.txt'

print 'Input file processed: %s' %inputfile

#main program
length, width, h, T_c, T_h = Load_input_file(inputfile)

temps = Load_solution_file(solnfile)
temps = Add_Boundary(length,width,h,T_c,T_h,temps)

x_coords, y_coords = Get_mesh(length, width, h)

Tavg = numpy.mean(temps)
print 'Mean Tempurature: %.5f' %Tavg

y_iso = Compute_Isoline(temps,x_coords,y_coords,Tavg,h)

Pseudocolor_plot(x_coords,y_coords,temps,Tavg,y_iso,length,width,h)

