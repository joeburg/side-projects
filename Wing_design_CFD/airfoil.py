#Purpose: create and Airfoil class that will handle the loading and basic
#processing of data associated with an airfoil at multiple angles of attack
#Joe Burg 

import copy
import glob
import math
import os

class Airfoil:
    """Handles the loading and processing of data associated with an airfoil\n"""+\
               """at multiple angles of attack."""
    
    def __init__(self,inputdir):
        """Initializes data and calls load_data() and process_data() methods."""
        
        self.inputdir = inputdir

        #raise exception if directory name does not end with '/'
        if self.inputdir[-1] != '/':
            raise Exception, 'Directory names must end with "/" to continue the path.'
        
        self.output = ''
        self.load_data(self.inputdir)
        self.process_data(self.filenames,self.angles_attack,self.xy_data,self.output)


    def load_data(self,inputdir):
        """Grabs pressure coefficent data and xy coordinate data filenames,\n"""+\
                 """calls the sort_data() method for the the pressure coeff\n"""+\
                 """filenames, and creates global lists to process within the class."""
        
        self.filenames = glob.glob('%s*.dat'%self.inputdir)

        #remove xy data file from filenames; if it's not in the directory, raise
        #an exception
        if os.path.exists('%sxy.dat'%self.inputdir):
            self.filenames.remove('%sxy.dat'%self.inputdir)
        else:
            raise Exception, 'Directory missing "xy.dat" file with coordinates for panels.'
        
        #ensure that the remaining filenames have the alpha*.dat format so they
        #can be processed property; if wrong filename format rasie an exception
        self.angles_attack = []
        for N_file in self.filenames:
            if 'alpha' not in N_file:
                raise Exception, 'Invalid file type in directory. Only "xy.dat" and '+\
                      '"alpha*.dat" (where * refers to the angle of attack) file types allowed.'
            else:
                #remove the angles from the file names and put in list
                self.angles_attack.append(float(N_file[len(self.inputdir)+5:-4]))

        #sort filenames via increasing angle of attack
        self.sort_data(self.filenames,self.angles_attack)

        #read xy coords and put into list to process
        xy_coord_file = open('%sxy.dat'%self.inputdir)
        self.xy_data = []        
        t=0
        for line in xy_coord_file:
            if t==0:
                #save filename in first line for output 
                self.inputdirname = line.strip()
            else:
                line = line.strip().split()
                self.xy_data.append([float(line[0]),float(line[1])])
            t += 1
        xy_coord_file.close()
        
    def sort_data(self,filenames,angles_attack):
        """Sorts the pressure coefficent filenames and angles in order of\n"""+\
                 """angle of attack."""
        
        #make deep copies of lists for comparison after sort
        angles_attack_0 = copy.deepcopy(self.angles_attack)
        filenames_0 = copy.deepcopy(self.filenames)
        self.angles_attack = sorted(self.angles_attack)

        #compare sorted angle list to the origial to sort the filenames
        for i in range(len(angles_attack_0)):
            for j in range(len(self.angles_attack)):
                if angles_attack_0[i] == self.angles_attack[j]:
                    self.filenames[j] = filenames_0[i]


    def process_data(self,filenames,angles_attack,xy_data,output):
        """Calls the L_chord() method and get_Cl_stagpt() method for each\n"""+\
                 """Cp file.  Appends results to output."""
        
        #get the length of the chord using the get_L_chord method 
        self.L_chord = self.get_L_chord(self.xy_data)

        #for each pressure coeff file, find the Cl and stagnation point
        for i in range(len(self.filenames)):
            Cp_data_file = open(self.filenames[i])
            self.Cp_data = []
            t=0
            for line in Cp_data_file:
                #ignore the first line in each Cp data file 
                if t>0:
                    line = line.strip().split()
                    self.Cp_data.append(float(line[0]))
                t += 1
            Cp_data_file.close()

            alpha = self.angles_attack[i]

            #compute the lift coeffient and stagnation point using the get_Cl_stagpt method     
            Cl,stag_x,stag_y,max_Cp = self.get_Cl_stagpt(self.xy_data,self.Cp_data,\
                                                            self.L_chord,alpha)
            #append to output string for data output 
            self.output += '  %5.2f  %7.4f  (%7.4f, %7.4f) %7.4f\n' % (alpha,Cl,stag_x,\
                                                               stag_y,max_Cp)
                    
    def get_L_chord(self,xy_data):
        """Returns the chord length of the airfoil."""
        
        #find max x and min x coordinates and compute the distance
        #between them
        max_x = self.xy_data[0][0]
        min_x = self.xy_data[0][0]
        max_index = 0
        min_index = 0
        for i in range(len(self.xy_data)):
            if xy_data[i][0] > max_x:
                max_x = self.xy_data[i][0]
                max_index = i
            if xy_data[i][0] < min_x:
                min_x = self.xy_data[i][0]
                min_index = i

        x1 = self.xy_data[min_index][0]
        y1 = self.xy_data[min_index][1]
        x2 = self.xy_data[max_index][0]
        y2 = self.xy_data[max_index][1]
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    
    def get_Cl_stagpt(self,xy_data,Cp_data,L_chord,alpha):
        """Returns the lift coefficient and stagnation point."""
        
        #length of Cp data is 1 less than length of xy_data so
        #use length of Cp data to deal with last index in xy_data (i+1)
        Fx_panel = []
        Fy_panel = []
        max_Cp = self.Cp_data[0]
        max_Cp_index = 0
        for i in range(len(self.Cp_data)):
            #find max Cp index to find stagnation point
            if Cp_data[i] > max_Cp:
                max_Cp = self.Cp_data[i]
                max_Cp_index = i

            #consistent order of difference fixes a consistent orientation
            dx =  self.xy_data[i+1][0] - self.xy_data[i][0]
            dy =  self.xy_data[i+1][1] - self.xy_data[i][1]

            #get x and y components of non-dimensional force 
            dCx = self.Cp_data[i]*dy / self.L_chord
            dCy = self.Cp_data[i]*dx / self.L_chord
            Fx_panel.append(dCx)
            Fy_panel.append(dCy)

        #stagnation point is the average of the points that comprise the panel
        stag_x = (self.xy_data[max_Cp_index][0] + self.xy_data[max_Cp_index+1][0])/2
        stag_y = (self.xy_data[max_Cp_index][1] + self.xy_data[max_Cp_index+1][1])/2

        #sum force components and calculate the lift coefficient 
        Cx = sum(Fx_panel)
        Cy = sum(Fy_panel)
        Cl = Cy*math.cos(-alpha*math.pi/180) - Cx*math.sin(-alpha*math.pi/180)
        return Cl,stag_x,stag_y,max_Cp

    
    def __repr__(self):
        """Prints the lift coefficients and stagnation points for each\n"""+\
                  """pressure coefficient data file."""
        
        string = 'Test case: %s\n\n' % self.inputdirname
        string += '  alpha     cl          stagnation pt\n'
        string += '  -----  -------  --------------------------\n'
        string += '%s' % self.output
        return string
