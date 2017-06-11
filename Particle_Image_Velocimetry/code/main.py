# Demonstration of PIV code to process images and solve for vector field

import matplotlib
import matplotlib.pyplot
import numpy
import sys
import time

import piv

# Default parameters
maskfilename = ''
windowSize = numpy.array([64, 32, 16])
overlap = 0.5
scaling = 1
dt = 1
outputFileBase = 'VectorField'
threshold_g = 3  # number of standard deviations from mean at which cutoff for global filter is set
threshold_l = 3  # number of neighborhood standard deviations from neighborhood mean at which cutoff for local filter is set
window_l = 5  # size of window defining neighborhood for local filter.

if len(sys.argv) == 3:
    imageAfilename = sys.argv[1]
    imageBfilename= sys.argv[2]
elif len(sys.argv) == 4:
    imageAfilename = sys.argv[1]
    imageBfilename= sys.argv[2]
    maskfilename = sys.argv[3]
else:
    print "Usage:"
    print "  python %s <imageAfilename> <imageBfilename> [maskfilename]" % sys.argv[0]
    exit()


# Instantiate the vector field object and solve for velocity field
try:
    t0 = time.time()
    v = piv.VectorField(imageAfilename, imageBfilename, maskfilename)
    print "Size of image: %d x %d" % (v.imageA.sx1, v.imageA.sx2)
    v.MultiPass(windowSize, overlap, threshold_g, threshold_l, window_l)
    v.Scaling(scaling, dt)
    v.Save(outputFileBase)
    t1 = time.time()
    print "Elapsed processing time: %f seconds" % (t1-t0)
except Exception, e:
    print 'ERROR: %s' % e
    exit()

# Load saved .txt files and plot

u2 = numpy.transpose(numpy.loadtxt(outputFileBase+'_u1.txt'))
u1 = numpy.transpose(numpy.loadtxt(outputFileBase+'_u2.txt'))
x1 = numpy.transpose(numpy.loadtxt(outputFileBase+'_x1.txt'))
x2 = numpy.transpose(numpy.loadtxt(outputFileBase+'_x2.txt'))

u1_masked = numpy.ma.array(u1, mask=numpy.isnan(u1))
cmap = matplotlib.cm.jet
cmap.set_bad('w',1.)

matplotlib.pyplot.figure()
matplotlib.pyplot.pcolor(x2, x1, u1_masked)
matplotlib.pyplot.colorbar()
matplotlib.pyplot.axis('equal')
matplotlib.pyplot.show(block=False)

u2_masked = numpy.ma.array(u2, mask=numpy.isnan(u2))
matplotlib.pyplot.figure()
matplotlib.pyplot.pcolor(x2, x1, u2_masked)
matplotlib.pyplot.colorbar()
matplotlib.pyplot.axis('equal')
matplotlib.pyplot.show(block=False)
