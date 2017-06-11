import matplotlib.pyplot
import scipy.misc

class Image:

    """
    Image class to hold and preprocess raw data images.
    """
    
    def __init__(self, imagefile):
        """
        Initializes the object and loads the data 
        
        Keyword arguments:
        imagefile -- filename of the image file
        """
        self.img = None
        self.sx1 = 0
        self.sx2 = 0
    
        self.LoadImageFile(imagefile)
    
    def LoadImageFile(self, imagefile):
        """
        Reads the image file always converting to grayscale
        """
        # Assumes that images will already be in grayscale
        try:
            self.img = scipy.misc.imread(imagefile)
            self.sx1, self.sx2 = self.img.shape
        except IOError:
            raise IOError("File " + imagefile + " does not exist")
    
    def DisplayImage(self):
        """
        Displays the image
        """
        matplotlib.pyplot.imshow(img)
        matplotlib.pyplot.show(block=False)
