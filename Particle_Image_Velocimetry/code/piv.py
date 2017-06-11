from distutils.core import setup, Extension
import numpy
import scipy.interpolate

import image


def InterpolatePeak(maxj, maxi, R, Rim1, Rip1, Rjm1, Rjp1, windowSize):
    """
    Function to interpolate peak to subpixel accuracy using parabolic fit.
    """
    hi = (Rim1-Rip1)/((2*Rim1)-(4*R)+(2*Rip1))
    hj = (Rjm1-Rjp1)/((2*Rjm1)-(4*R)+(2*Rjp1))
    disp2 = hi + (maxi-windowSize)
    disp1 = hj + (maxj-windowSize)
    return disp1, disp2


def XCorr(a, b):
    """
    Function to compute cross correlations.
    """
    if a.shape != b.shape:
        raise RuntimeError("Cannot cross correlate windows of different sizes.")

    n1, n2 = a.shape

##    sources = ['example.i', 'sum.c']
##    include_dirs = [numpy.get_include()]
##
##    _example = Extension('_example',
##                         sources=sources,
##                         include_dirs=include_dirs)
##
##    setup(name='example',
##          ext_modules=[_example])
    
    R = numpy.zeros((n1*2-1, n2*2-1))

    A = numpy.zeros((n1*3-2, n2*3-2))
    A[n1-1:2*n1-1, n2-1:2*n2-1] = a
    B = numpy.zeros((n1*3-2, n2*3-2))

    for i in range(-n1, n1-1):
        for j in range(-n2, n2-1):
            B[n1+i:2*n1+i, n2+j:2*n2+j] = b
            R[n1+i, n2+j] = numpy.sum(A*B)
            B[n1+i:2*n1+i, n2+j:2*n2+j] = 0

    return R


class VectorField:
    """
    VectorField class to load two images & perform cross correlations to yield a vector field
    """

    def __init__(self, imageAfile, imageBfile, maskfile):
        """
        Initializes the object, loads and prepares the two images
            
        Keyword arguments:
        imageAfile -- filename of the first image file
        imageBfile -- filename of the second image file
        maskfile -- filename of the mask 
        scaling -- pixel/mm conversion factor
        dt -- time elapsed between images
        """
        self.imageA = None
        self.imageB = None
        self.mask = None
        self.u1 = None
        self.u2 = None
        self.x1 = None
        self.x2 = None
        self.m = None
    
        self.LoadImages(imageAfile, imageBfile)
        self.LoadMask(maskfile)
        self.PrepareImages()
    
    def LoadImages(self, imageAfile, imageBfile):
        """
        Loads the two images
        """
        self.imageA = image.Image(imageAfile)
        self.imageB = image.Image(imageBfile)
    
        if self.imageA.sx1 != self.imageB.sx1 or self.imageA.sx2 != self.imageB.sx2:
            raise RuntimeError("Image files are not the same size.")
    
    def LoadMask(self, maskfile):
        """
        Loads the mask
        """
        # If no mask file was defined, specify an empty array
        # In general, the mask will have 1s where the mask is and 0s elsewhere.
        if not maskfile:
            self.mask = numpy.zeros((self.imageA.sx1, self.imageA.sx2))
        else:
            m = image.Image(maskfile)
            self.mask = m.img/numpy.amax(m.img)

        if (self.imageA.sx1, self.imageA.sx2) != self.mask.shape:
            print self.imageA.sx1
            print self.imageA.sx2
            print self.mask.shape
            raise RuntimeError("Mask file is not the same size as the image files.")

    def PrepareImages(self):
        """
        Prepares the images for processing (background image removeal and intensity normalization)
        
        As these are more advanced features, they are not included here.
        """
        pass

    def MultiPass(self, windowSize, overlap, threshold_g, threshold_l, window_l):
        """
        Controls the multi-pass routine.
        
        For simplicity the following restrictions are made:
            - Only square interrogation windows will be used
            - The size of the image must be an exact multiple of the size(s) of the windows (with overlap)
            - Only even-size windows are supported
            
        Note that an additional final pass will be performed at the smallest window size. 
        
        Algorithms follow closely the MatPIV code by J.K. Sveen:
        http://www.mn.uio.no/math/english/people/aca/jks/matpiv/
        """
        if windowSize.size == 0:
            raise RuntimeError("No window sizes specified.")
        if overlap < 0 or overlap > 1:
            raise RuntimeError("Overlap of windows is outside allowable range")
        for i in range(0, windowSize.size):
            if not (self.imageA.sx1/(windowSize[i]*(1-overlap))-1).is_integer() \
            or not (self.imageA.sx2/(windowSize[i]*(1-overlap))-1).is_integer():
                raise RuntimeError("Image size is not evenly divisible by window size for given overlap")
            
        passes = windowSize.shape[0]
        
        # Allocate starting velocity arrays of zeros for first pass
        # Size corresponds to number of windows that will be taken across the image on the first pass
        self.u1 = numpy.zeros((numpy.int_(self.imageA.sx1/(windowSize[0]*(1-overlap))-1),
                               numpy.int_(self.imageA.sx2/(windowSize[0]*(1-overlap))-1)))
        self.u2 = numpy.zeros((numpy.int_(self.imageA.sx1/(windowSize[0]*(1-overlap))-1),
                               numpy.int_(self.imageA.sx2/(windowSize[0]*(1-overlap))-1)))
        
        # At each window size, call the Pass method to perform the desired cross correlation and displacement analysis
        for i in range(0, passes):
            print 'Beginning pass #%d with window size %d' % (i+1, windowSize[i])
            # If this is not the final window size do not use interpolation in Pass method
            self.Pass(windowSize[i], overlap, 0)
            self.PostProcess(threshold_g, threshold_l, window_l)
            if i != passes-1:
                # Expand velocity and coordinate arrays to allow finer resolution on next pass
                self.Expand(windowSize[i], windowSize[i+1], overlap)
        print 'Beginning final pass #%d with window size %d' % (passes+1, windowSize[passes-1])
        self.Pass(windowSize[passes-1], overlap, 1)
        self.PostProcess(threshold_g, threshold_l, window_l)
    
    def Pass(self, windowSize, overlap, interp):
        """
        Conducts cross-correlation beween images using windows of desired size.
        """
        # Create temporary references for current velocity vectors
        v1 = self.u1
        v2 = self.u2
        
        # Initialize the coordinate vectors to the proper size
        self.x1 = numpy.zeros((numpy.int_(self.imageA.sx1/(windowSize*(1-overlap))-1),
                               numpy.int_(self.imageA.sx2/(windowSize*(1-overlap))-1)))
        self.x2 = numpy.zeros((numpy.int_(self.imageA.sx1/(windowSize*(1-overlap))-1),
                               numpy.int_(self.imageA.sx2/(windowSize*(1-overlap))-1)))
        
        # Initialize windowed mask to proper size
        self.m = numpy.zeros((numpy.int_(self.imageA.sx1/(windowSize*(1-overlap))-1),
                              numpy.int_(self.imageA.sx2/(windowSize*(1-overlap))-1)))
 
        sequence = numpy.arange(0, numpy.int_(self.imageA.sx1-windowSize+1), numpy.int_((1-overlap)*windowSize))
        jjIter = sequence.__iter__()
        
        sequence = numpy.arange(0, numpy.int_(self.imageA.sx2-windowSize+1), numpy.int_((1-overlap)*windowSize))
        iiIter = sequence.__iter__()
    
        cj = 0
        for jj in jjIter:
            ci = 0
            iiIter = sequence.__iter__()
            for ii in iiIter:
                # Check that the center of the window is not within a masked region.
                if self.mask[numpy.int_(jj+windowSize/2), numpy.int_(ii+windowSize/2)] != 1:
                    # Check if the velocity value from the last iteration was indeterminate
                    if numpy.isnan(v1[cj, ci]):
                        v1[cj, ci] = 0
                    
                    if numpy.isnan(v2[cj, ci]):
                        v2[cj, ci] = 0
                    
                    # Check that last determined velocity does not shift window outside of range of image
                    if jj+v1[cj, ci] < 0:
                        v1[cj, ci] = -jj
                    
                    if jj+v1[cj, ci] > self.imageA.sx1-windowSize:
                        v1[cj, ci] = self.imageA.sx1-windowSize - jj
                    
                    if ii+v2[cj, ci] < 0:
                        v2[cj, ci] = -ii
                    
                    if ii+v2[cj, ci] > self.imageA.sx2-windowSize:
                        v2[cj, ci] = self.imageA.sx2-windowSize - ii
                    
                    # Take the appropriate window from each image
                    a = self.imageA.img[numpy.int_(jj):numpy.int_(jj+windowSize), numpy.int_(ii):numpy.int(ii+windowSize)]
                    b = self.imageB.img[numpy.int_(jj+v1[cj,ci]):numpy.int_(jj+windowSize+v1[cj,ci]),
                                        numpy.int_(ii+v2[cj,ci]):numpy.int_(ii+windowSize+v2[cj,ci])]

                    # Subtract mean intensity over each window
                    a = a - numpy.mean(a)
                    b = b - numpy.mean(b)

                    # Compute cross correlation
                    R = XCorr(a, b)

                    # Find indices of maximum value
                    ind = numpy.argmax(R)
                    r1, r2 = R.shape
                    maxj, maxi = numpy.unravel_index(ind, [r1, r2])
                    
                    # If this is the final pass, use interpolation to yeild subpixel accuracies
                    if interp:
                        Rji = R[maxj, maxi]

                        # Handle edge cases
                        nj, ni = R.shape
                        if maxi-1 >= 0:
                            Rjim1 = R[maxj, maxi-1]
                        else:
                            Rjim1 = numpy.nan
                        if maxi+1 < ni:
                            Rjip1 = R[maxj, maxi+1]
                        else:
                            Rjip1 = numpy.nan
                        if maxj-1 >= 0:
                            Rjm1i = R[maxj-1, maxi]
                        else:
                            Rjm1i = numpy.nan
                        if maxj+1 < nj:
                            Rjp1i = R[maxj+1, maxi]
                        else:
                            Rjp1i = numpy.nan
                        
                        disp1, disp2 = InterpolatePeak(maxj, maxi, Rji, Rjim1, Rjip1,Rjm1i, Rjp1i, windowSize)
                        
                        # Update velocity arrays
                        self.u1[cj,ci] = -disp1 + v1[cj,ci]
                        self.u2[cj,ci] = -disp2 + v2[cj,ci]
                    else:
                        self.u1[cj,ci] = -(maxj - windowSize)+v1[cj,ci]
                        self.u2[cj,ci] = -(maxi - windowSize)+v2[cj,ci]
                    
                    # Update coordinate arrays
                    self.x1[cj,ci] = jj+windowSize/2
                    self.x2[cj,ci] = ii+windowSize/2
                    self.m[cj,ci] = 0

                else:
                    # Window is within a mask region, update velocity arrays and coordinate arrays
                    self.u1[cj,ci] = numpy.nan
                    self.u2[cj,ci] = numpy.nan
                    self.x1[cj,ci] = jj+windowSize/2
                    self.x2[cj,ci] = ii+windowSize/2
                    self.m[cj,ci] = 1
                ci += 1
            cj += 1
    
    def Expand(self, win1, win2, overlap):
        """
        Expands the velocity vector array and coordinate array to allow higher resolution of next pass
        """
        y1 = numpy.arange(win1/2, self.imageA.sx1 - win1/2+1, (1-overlap)*win1)
        y1i = numpy.arange(win2/2, self.imageA.sx1 - win2/2+1,(1-overlap)*win2)
        
        y2 = numpy.arange(win1/2, self.imageA.sx2 - win1/2+1, (1-overlap)*win1)
        y2i = numpy.arange(win2/2, self.imageA.sx2 - win2/2+1,(1-overlap)*win2)
        
        f = scipy.interpolate.interp2d(y1, y2, self.u1, kind='linear')
        self.u1 = numpy.around(f(y2i,y1i))
        
        f = scipy.interpolate.interp2d(y1, y2, self.u2, kind='linear')
        self.u2 = numpy.around(f(y2i,y1i))

    def PostProcess(self, threshold_g, threshold_l, window_l):
        """
        Perform filteration and interpolation functions here
        """
        self.GlobalFilter(threshold_g)
        self.LocalFilter(window_l, threshold_l)
        self.InterpNans()

    def GlobalFilter(self, threshold):
        """
        Global filtration based on standard deviations over entire 2D velocity field.
        Vectors with component values outside the range [-threshold * std(vel component)
        + mean(vel component), threshold * std(vel component) + mean(vel component)]
        for both components will be set to nan
        """
        # Determine velocity field statistics
        u1std = numpy.nanstd(self.u1)
        u2std = numpy.nanstd(self.u2)
        u1mean = numpy.nanmean(self.u1)
        u2mean = numpy.nanmean(self.u2)
        
        # Define upper and lower bounds for each component
        u1_lb = -threshold*u1std + u1mean
        u1_ub = threshold*u1std + u1mean
        
        u2_lb = -threshold*u2std + u2mean
        u2_ub = threshold*u2std + u2mean
        
        # Check that each vector in field (not including the masked regions) fulfills required condition
        jj, ii = self.u1.shape
        for j in range(0, jj):
            for i in range(0, ii):
                if self.m[j,i] != 1:
                    if ((self.u1[j,i] < u1_lb) or (self.u1[j,i] > u1_ub)) \
                    or ((self.u2[j,i] < u2_lb) or (self.u2[j,i] > u2_ub)):
                        self.u1[j,i] = numpy.nan
                        self.u2[j,i] = numpy.nan

    def LocalFilter(self, window, threshold):
        """
        Local filtration based on mean neighborhoods of 2D velocity fields. Vectors
        with a component value outside the range [-threshold * std(neighbor vel components)
        + mean(neighbor vel component), rangeFactor * std(neighbor vel component)
        + mean(neighbor vel component)] will have both components set to nan
        """
        # First create temporary arrays to hold vector components with necessary padding at edges
        jj, ii = self.u1.shape
        pad = numpy.int_(numpy.floor(window/2))
        tmp1 = numpy.zeros((jj + 2*pad, ii + 2*pad))*numpy.nan
        tmp2 = numpy.zeros((jj + 2*pad, ii + 2*pad))*numpy.nan
    
        tmp1[pad:jj+pad, pad:ii+pad] = self.u1
        tmp2[pad:jj+pad, pad:ii+pad] = self.u2
    
        # For each point in the fields not within the masked region
        for j in range(pad, jj+pad):
            for i in range(pad, ii+pad):
                if self.m[j-pad,i-pad] != 1:
                    if not numpy.all(numpy.isnan(tmp1[j-pad:j+pad+1, i-pad:i+pad+1])) \
                    and not numpy.all(numpy.isnan(tmp2[j-pad:j+pad+1, i-pad:i+pad+1])):
                        nmean1 = numpy.nanmean(tmp1[j-pad:j+pad+1, i-pad:i+pad+1])
                        nstd1 = numpy.nanstd(tmp1[j-pad:j+pad+1, i-pad:i+pad+1])
                        nmean2 = numpy.nanmean(tmp2[j-pad:j+pad+1, i-pad:i+pad+1])
                        nstd2 = numpy.nanstd(tmp2[j-pad:j+pad+1, i-pad:i+pad+1])
                        if tmp1[j+pad, i+pad] > (nmean1+nstd1*threshold) \
                        or tmp1[j+pad, i+pad] < (nmean1-nstd1*threshold) \
                        or tmp2[j+pad, i+pad] > (nmean2+nstd2*threshold) \
                        or tmp2[j+pad, i+pad] < (nmean2-nstd2*threshold):
                            self.u1[j-pad,i-pad] = numpy.nan
                            self.u2[j-pad,i-pad] = numpy.nan
                    else:
                        self.u1[j-pad,i-pad] = numpy.nan
                        self.u2[j-pad,i-pad] = numpy.nan

    def InterpNans(self):
        """ 
        Quasi-bilinear interpolation: average 1D interpolation along each row and
        1D interpolation along each column to removed nan values from velocity field
        """
    
        # Store shape of vector field for future use
        n1, n2 = self.u1.shape
        
        v1 = self.u1.copy()
        v2 = self.u2.copy()
        
        w1 = self.u1.copy()
        w2 = self.u2.copy()

        # 1D interpolation along rows
        for j in range(0, n1):
            # References to this row
            tu1 = self.u1[j, 0:n2]
            tx2 = self.x2[j, 0:n2]
            ty2 = tx2
        
            # Find the locations of the nans in u1 data
            nans = numpy.isnan(tu1)
        
            # Remove those data points from the arrays
            tu1 = tu1[~nans]
            tx2 = tx2[~nans]
            
            # Interpolate if array not empty, otherwise, allow slice to remain nans
            if tu1.size > 0:
                v1[j, 0:n2] = numpy.interp(ty2, tx2, tu1)
            else:
                v1[j, 0:n2] = numpy.zeros((1, n2))*numpy.nan

            # References to this row
            tu2 = self.u2[j, 0:n2]
            tx2 = self.x2[j, 0:n2]
            ty2 = tx2
            
            # Find the locations of the nans in u2 data
            nans = numpy.isnan(tu2)
            
            # Remove those data points from the arrays
            tu2 = tu2[~nans]
            tx2 = tx2[~nans]

            # Interpolate
            if tu2.size > 0:
                v2[j, 0:n2] = numpy.interp(ty2, tx2, tu2)
            else:
                v2[j, 0:n2] = numpy.zeros((1, n2))*numpy.nan
                
        for i in range(0, n2):
            # References to this row
            tu1 = self.u1[0:n1, i]
            tx1 = self.x1[0:n1, i]
            ty1 = tx1
                                    
            # Find the locations of the nans in u1 data
            nans = numpy.isnan(tu1)
                                        
            # Remove those data points from the arrays
            tu1 = tu1[~nans]
            tx1 = tx1[~nans]
            
            # Interpolate
            if tu1.size > 0:
                w1[0:n1, i] = numpy.interp(ty1, tx1, tu1)
            else:
                w1[0:n1, i] = numpy.zeros((n1, 1))
           
            # References to this row
            tu2 = self.u2[0:n1, i]
            tx1 = self.x1[0:n1, i] 
            ty1 = tx1
            
            # Find the locations of the nans in u2 data
            nans = numpy.isnan(tu2)
            
            # Remove those data points from the arrays
            tu2 = tu2[~nans]
            tx1 = tx1[~nans]
            
            # Interpolate
            if tu1.size > 0:
                w2[0:n1, i]= numpy.interp(ty1, tx1, tu2)
            else:
                w2[0:n1, i] = numpy.zeros((n1, 1))

        self.u1 = (v1 + w1)/2
        self.u2 = (v2 + w2)/2
    
        # Reinsert nans associated with mask
        c = numpy.where(self.m > 0)
        self.u1[c] = numpy.nan
        self.u2[c] = numpy.nan

    def Scaling(self, scaling, dt):
        """
        If desired, convert velocities and coordinates from pixel/dt, pixels to mm/sec, mm
        """
        self.u1 = self.u1/dt/scaling
        self.u2 = self.u2/dt/scaling
        self.x1 = self.x1/scaling
        self.x2 = self.x2/scaling

    def Save(self, outputFileBase):
        """
        Save velocity field and coordinate field to file. 
        """
        filename = outputFileBase + '_u1.txt'
        numpy.savetxt(filename, self.u1, delimiter=' ')

        filename = outputFileBase + '_u2.txt'
        numpy.savetxt(filename, self.u2, delimiter=' ')

        filename = outputFileBase + '_x1.txt'
        numpy.savetxt(filename, self.x1, delimiter=' ')

        filename = outputFileBase + '_x2.txt'
        numpy.savetxt(filename, self.x2, delimiter=' ')
