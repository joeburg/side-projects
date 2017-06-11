# Program to process data from steady state heat equation

import matplotlib.pyplot
import numpy
import sys

##################################################################################

def Load_solution_file(solnfile):
    f = open(solnfile)
    length, width, h = f.readline()
    T_c, T_h = f.readline()
    f.close()
    return length, width, h, T_c, T_h

def Load_input_file(inputfile):
    # remove first line that has description (x, y, T)
    f = open(inputfile)
    f.readline()
    f.close()

    # use numpy to read columns in file
    x_coords = numpy.loadtxt(inputfile, dtype=numpy.int32, usecols=(0))
    y_coords = numpy.loadtxt(inputfile, dtype=numpy.int32, usecols=(1))
    temps = numpy.loadtxt(inputfile, dtype=numpy.float64, usecols=(2))

    return x_coords, y_coords, temps

def Add_Boundary(length,width,h,T_c,T_h,x_coords,y_coords,temps):
    # shift y coords up one to add boundary
    y_coords = numpy.add(1,y_coords)

    # make arrays for lower boundary (T_c)
    LBCx = pylab.arange(0, length+h, h)
    LBCy = pylab.zeros((1,length/h+1))

    T_l = []
    for i in range(length/h+1):
        T_l.append(-T_c*(numpy.exp(-10*numpy.power(i - length/2))-2))
    T_l = numpy.array(T_l)
     
    # make arrays for upper boundary (T_h)
    UBCx = pylab.arange(0, length+h, h)
    UBCy = pylab.empty(length/h+1)
    UBCy.fill(width-1)
    
    T_u = numpy.empty(length/h+1)
    T_u.fill(T_h)

    # add boundary arrays to interior arrays
    x_coords = numpy.append(LBCx,x_coords)
    x_coords = numpy.append(x_coords,UBCx)

    y_coords = numpy.append(LBCy,y_coords)
    y_coords = numpy.append(y_coords,UBCy)

    temps = numpy.append(T_l,temps)
    temps = numpy.append(T_u,temps)

    return x_coords, y_coords, temps
    
def Pseudocolor_plot(x_coords,y_coords,temps,Tavg,length,width):
    x_coords, y_coords = pylab.meshgrid(x_coords, y_coords)
    pylab.pcolor(x_coords,y_coords,temps)
    pylab.pcolor(x_coords,y_coords,temps)
    pylab.colorbar()
    pylab.axis([0,length,width-0.2,width+0.2])
    pylab.show(block=False)

##################################################################################
#import data from command line

if len(sys.argv) < 3:
  print "Usage:"
  print "   python %s <input file> <solution file>" % sys.argv[0]
  exit()

inputfile = sys.argv[1]
solnfile = sys.argv[2]

print 'Input file processed: %s' %inputfile

#main program
length, width, h, T_c, T_h = Load_solution_file(solnfile)

x_coords, y_coords, temps = Load_input_file(inputfile)

x_coords, y_coords, temps = Add_Boundary(length,width,h,T_c,\
                                         T_h,x_coords,y_coords,temps)

Tavg = numpy.mean(temps)
print 'Mean Tempurature: %.5f' %Tavg 

Pseudocolor_plot(x_coords,y_coords,temps,Tavg,length,width)

