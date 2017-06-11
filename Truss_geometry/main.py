#Purpose: gathers command line arguments, instantiates an instance
# of the Truss class and prints the instance to display the computed
# beam forces for the truss.
#Joe Burg

import sys
import truss

if len(sys.argv) < 3:
    print 'Usage:'
    print '  python %s <joints data file> <beams data file>' % sys.argv[0]
    exit()
    
joints_file = sys.argv[1]
beams_file = sys.argv[2]

try:
    a = truss.Truss(joints_file,beams_file)
except Exception, e:
    print 'ERROR: %s' % e
    exit()

print a
