import sys

import airfoil

if len(sys.argv) < 2:
  print 'Usage:'
  print '  python %s <airfoil data directory>' % sys.argv[0]
  exit()

inputdir = sys.argv[1]

try:
  a = airfoil.Airfoil(inputdir)
except Exception, e:
  print 'ERROR: %s' % e
  exit()

print a
