# Purpose: program to verify that a maze solution is valid

import numpy
import sys

###########################################################################
def LoadData(mazefile):
    """Loads maze as numpy array and finds dimensions"""
    f = open(mazefile)
    dim = f.readline().split()
    ni = int(dim[0])
    nj = int(dim[1])
    maze = numpy.ones([ni,nj],dtype=int)
    
    for line in f:
        line = line.strip().split()
        maze[int(line[0])][int(line[1])] = 0
    f.close()
    return maze, ni

def RunSolution(solutionfile,maze,ni):
    """Runs solution steps and compares to values in maze array;
    returns if the solution is valid"""
    f = open(solutionfile)
    for line in f:
        line = line.strip().split()
        row = int(line[0])
        col = int(line[1])

        #ensure that each step does not go through a wall
        #this also ensures that the maze was properly entered
        if not maze[row][col]:
            print 'Invalid solution: a wall was crossed!'
            return
    f.close()
    
    #if the last row is reached then the solution is correct
    if row == ni-1:
        print 'Valid Solution!'
    else:
        print 'Invalid solution: end of maze not reached!'

###########################################################################
# Analyze the command line arguments and setup the corresponding parameters
if len(sys.argv) < 3:
    print 'Usage:'
    print '  python %s <maze file> <solution file>' % sys.argv[0]
    exit()

mazefile = sys.argv[1]
solutionfile = sys.argv[2]

#main program
maze, ni = LoadData(mazefile)
RunSolution(solutionfile,maze,ni)

