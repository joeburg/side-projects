import sys
import time
import yaml

import containerExt

if len(sys.argv) < 2:
    print 'Usage:'
    print '  %s <yaml file>'% sys.argv[0]
    exit()
else:
    inputfile = sys.argv[1]
    f = open(inputfile)
    fields = yaml.load(f)
    f.close()

# check which fields are empty; it's verbose but necessary to make
# it easy as possible for the user if there is a mistake
if fields['inputfile'] == None:
    fields['inputfile'] = ''
if fields['outputfile'] == None:
    fields['outputfile'] = ''
if fields['savefreq'] == None:
    fields['savefreq'] = -1
if fields['datatype'] == None:
    raise RuntimeError, "'datatype' must be specified in .yml file to instantiate "+\
          "the correct containter object."
if fields['mass'] == None:
    raise RuntimeError, "'mass' must be specified in .yml file"
if fields['Nparticles'] == None:
    raise RuntimeError, "'Nparticles' must be specified in .yml file"
if fields['length'] == None:
    raise RuntimeError, "'length' must be specified in .yml file"
if fields['temp0'] == None:
    raise RuntimeError, "'temp0' must be specified in .yml file"
if fields['h'] == None:
    raise RuntimeError, "'h' (time step) must be specified in .yml file"
if fields['Nsteps'] == None:
    raise RuntimeError, "'Nsteps' must be specified in .yml file"

# instantiate a container object and run a simulation
if fields['datatype'] == 'double':
    t0 = time.time()
    containerExt.containerDouble(fields['Nparticles'],fields['mass'],\
                                 fields['length'],fields['temp0'],\
                                 fields['Nsteps'],fields['inputfile'])\
                                 .RunSimulation(fields['savefreq'],fields['outputfile'])                      
    print 'Time elapsed %.4f seconds.' %(time.time()-t0)

elif fields['datatype'] == 'float':
    t0 = time.time()
    containerExt.containerFloat(fields['Nparticles'],fields['mass'],\
                                 fields['length'],fields['temp0'],\
                                 fields['Nsteps'],fields['inputfile'])\
                                 .RunSimulation(fields['savefreq'],fields['outputfile'])                      
    print 'Time elapsed %.4f seconds.' %(time.time()-t0)

