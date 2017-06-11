#Purpose: develop a Truss class for loading and analyzing a 2D truss using
#the method of joints.
#Joe Burg

import math
import numpy
import pylab
import scipy.linalg
import scipy.sparse
import scipy.sparse.linalg
import scipy.sparse.linalg.dsolve.umfpack
import warnings

class Truss:
    """
    Truss class for loading and analyzing a 2D truss using the method
    of joints.
    """

    def __init__(self,joints_file,beams_file):
        """
        Initializes an instance of the Truss class by loading the truss
        data from specified files.
        """
        #catch warnings as exceptions
        warnings.filterwarnings('error', category=scipy.sparse.linalg.dsolve.umfpack.UmfpackWarning)
        
        self.joints = {}
        self.beams = {}
        self.N_zerodisp = 0 #number of rigid supports
        
        #create lists for x and y joint coords, so min and max coords
        #can be obtain for plot range
        self.jointsx = []
        self.jointsy = []

        self.LoadData(joints_file,beams_file)
        self.InitializeArrays()

        #check if the truss geometry is overdetermined/underdetermined ie
        #if there are more/less variables than equations; if so raise
        #a RuntimeError
        if self.Nvar > self.Neqn:
            raise RuntimeError, "Truss geometry not suitable for static "+\
                   "equilibrium analysis (overdetermiend system)"
        elif self.Nvar < self.Neqn:
            raise RuntimeError, "Truss geometry not suitable for static "+\
                   "equilibrium analysis (underdetermined system)"

        self.PopulateArrays()
        self.PlotGeometry()
        self.ComputeForce()


    def LoadData(self, filename1,filename2):
        """
        Loads the joint coordintates, external forces on each joint, locations
        of rigid supports, and beam data which specifies the joints on either
        side of the beams.
        """
        f = open(filename1)
        #ignore first line
        f.readline()
        for line in f:
            line = line.strip().split()
            self.joints[int(line[0])] = [float(line[1]),float(line[2]),\
                                    float(line[3]),float(line[4]),int(line[5])]
            self.jointsx.append(float(line[1]))
            self.jointsy.append(float(line[2]))
            if int(line[5]):
                self.N_zerodisp += 1
        f.close()

        f = open(filename2)
        #ignore first line
        f.readline()
        for line in f:
            line = line.strip().split()
            self.beams[int(line[0])] = [int(line[1]),int(line[2])]
        f.close()
        
    def PlotGeometry(self):
        """
        Plots the geometry of the truss.
        """
        for beam in self.beams:
            Ja = self.beams[beam][0]
            Jb = self.beams[beam][1]
            #plots each beam using the joint coordinates
            pylab.plot([self.joints[Ja][0],self.joints[Jb][0]],\
                       [self.joints[Ja][1],self.joints[Jb][1]],'b-')
        pylab.axis([min(self.jointsx)-0.5,max(self.jointsx)+0.5,\
                    min(self.jointsy)-0.5,max(self.jointsy)+0.5])
        #save plot to file
        pylab.savefig('truss.png')

    def InitializeArrays(self):
        """
        Initializes data strcutres to construct sparse matrix.  Computes
        the number of variables and number of equations.
        """
        self.row = []
        self.col = []
        self.data = []
        self.Nvar = len(self.beams)+self.N_zerodisp*2 #number of variables 
        self.Neqn = len(self.joints)*2 #size of array; number of eqns
        self.xyforces = numpy.zeros(self.Neqn,dtype=numpy.float64)

    def PopulateArrays(self):
        """
        Populates the data array as a sparse matrix in COO format.  Populates
        the external force array.
        """
        #force components due to beams
        for beam in self.beams:
            Ja = self.beams[beam][0]
            Jb = self.beams[beam][1]
            x1 = self.joints[Ja][0]
            y1 = self.joints[Ja][1]
            x2 = self.joints[Jb][0]
            y2 = self.joints[Jb][1]
            theta = self.ComputeAngle(x1,y1,x2,y2)

            #x components of beam force for both joints (Ja,Jb)
            #for consistency, take the absolute value of sin/cos
            #and compare coordinates to assign +/-
            if x1 < x2:
                self.row.append(2*Ja-2)
                self.col.append(beam-1)
                self.data.append(-abs(math.cos(theta)))

                self.row.append(2*Jb-2)
                self.col.append(beam-1)
                self.data.append(abs(math.cos(theta)))
                
            else:
                self.row.append(2*Ja-2)
                self.col.append(beam-1)
                self.data.append(abs(math.cos(theta)))

                self.row.append(2*Jb-2)
                self.col.append(beam-1)
                self.data.append(-abs(math.cos(theta)))

            #y components of beam force for both joints (Ja,Jb)
            if y1 < y2:
                self.row.append(2*Ja-1)
                self.col.append(beam-1)
                self.data.append(-abs(math.sin(theta)))

                self.row.append(2*Jb-1)
                self.col.append(beam-1)
                self.data.append(abs(math.sin(theta)))
                
            else:
                self.row.append(2*Ja-1)
                self.col.append(beam-1)
                self.data.append(abs(math.sin(theta)))

                self.row.append(2*Jb-1)
                self.col.append(beam-1)
                self.data.append(-abs(math.sin(theta)))

        #reaction force components due to fixed supports and
        #possible non-zero external forces at each joint
        N_R = 0
        for joint in self.joints:
            #reaction forces
            if self.joints[joint][4]:
                N_R += 1
                self.row.append(2*joint-2)
                self.col.append(len(self.beams)-1+N_R)
                self.data.append(1)

                N_R += 1
                self.row.append(2*joint-1)
                self.col.append(len(self.beams)-1+N_R)
                self.data.append(1)

            #external forces (negative since we substract from both
            #side of eqn)
            self.xyforces[2*joint-2] = -self.joints[joint][2]
            self.xyforces[2*joint-1] = -self.joints[joint][3]

    def ComputeAngle(self,x1,y1,x2,y2):
        """
        Computes and returns the angle between two joints.
        """
        #to aviod division by 0, compute deltax
        if x2-x1 == 0:
            return math.pi/2
        elif y2-y1 == 0:
            return 0.0
        else:
            return math.atan((y2-y1)/(x2-x1))

    def ComputeForce(self):
        """
        Computes the beam forces for the truss.
        """
        self.row = numpy.array(self.row)
        self.col = numpy.array(self.col)
        self.data = numpy.array(self.data)

        #construct sparse matrix from COO formated arrays 
        self.sparsedata = scipy.sparse.coo_matrix((self.data,(self.row,self.col)),\
                                                  shape=(self.Neqn,self.Neqn)).tocsr()

        #check if det(sparsedata)=0 which implies the matrix is not invertible
        #and thus singular; if so, raise a RuntimeError
        if scipy.linalg.det(self.sparsedata.todense()) == 0:
            raise RuntimeError, "Cannot solve the linear system, unstable truss?"
    
        self.beamforces = scipy.sparse.linalg.spsolve(self.sparsedata,self.xyforces)

    def __repr__(self):
        txt = ' Beam       Force\n'
        txt += '-----------------\n'
        for beam in self.beams:
            txt += '%5s  %10.3f\n' % (beam,self.beamforces[beam-1])
        return txt
        

a = Truss('truss1/joints.dat', 'truss1/beams.dat')
print a
