//
//  imageio.cpp
//  
//
//  Created by Joe Burg on 1/12/15.
//
//

#include <cstring>
#include <iostream>
#include <string>


#include "imageio.hpp"
#include "tiffio.h"

namespace ImageIO
{
    void Read8bitGrayscaleTIFF(std::string filename,
                               unsigned char * &data,
                               unsigned int &width,
                               unsigned int &height)
    {
        TIFF *tif = NULL;
        unsigned int n;
        unsigned char *rgba;
        
        /* Open the input file for read */
        tif = TIFFOpen(filename.c_str(), "r");
        if (!tif)
        {
            std::cerr << "ERROR: Failed to open " << filename << " for input!" << std::endl;
            exit(1);
        }
        
        /* Read fields from the input file. */
        TIFFGetField(tif,TIFFTAG_IMAGEWIDTH, &width);
        TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);
        
        /* Read the image in RGBA format. Use unsigned char pointer 
         so the individual channels are easily accessible. */
        rgba = (unsigned char *) _TIFFmalloc(4*width*height*sizeof(unsigned char));
        TIFFReadRGBAImage(tif, width, height, (unsigned int *)rgba, 0);
        
        /* Convert RGBA data to grayscale using average method. */
        data = new unsigned char[width*height];
        for(n = 0; n < width*height; n++)
        {
            /* Average the sum of the R, G, and B channels. */
            data[n] = (unsigned char)(((unsigned int)rgba[4*n+0] +
                                            (unsigned int)rgba[4*n+1] +
                                            (unsigned int)rgba[4*n+2])/3);
        }
        
          /* Free RGBA memory and close the file. */
        _TIFFfree(rgba);
        rgba = NULL;
        
        TIFFClose(tif);
        tif = NULL;
    }
    
    void Write8bitGrayscaleTIFF(std::string filename,
                                unsigned char *data,
                                unsigned int width,
                                unsigned int height)
    {
        TIFF *tif = NULL;

        /* Open the output file for write */
        tif = TIFFOpen(filename.c_str(), "w");
        if (!tif)
        {
            std::cerr << "ERROR: Failed to open " << filename << " for output!" << std::endl;
            exit(1);
        }
        
        /* Write fields to the output file. */
        TIFFSetField(tif, TIFFTAG_IMAGEWIDTH, width);
        TIFFSetField(tif, TIFFTAG_IMAGELENGTH, height);
        TIFFSetField(tif, TIFFTAG_BITSPERSAMPLE, 8);
        TIFFSetField(tif, TIFFTAG_SAMPLESPERPIXEL, 1);
        TIFFSetField(tif, TIFFTAG_ORIENTATION, 4);
        
        /* Write the grayscale data to the output file. */
        TIFFWriteEncodedStrip(tif, 0, data, width*height);
        
        /* Close the output file and free remaining memory. */
        TIFFClose(tif);
        tif = NULL;
    }
}


