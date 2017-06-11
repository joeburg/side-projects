//
//  maintest.cpp
//  
//
//  Created by Joe Burg on 1/12/15.
//
//

#include <iostream>
#include <string>

#include "imageio.hpp"
#include "tiffio.h"


int main()
{
    std::string infilename = "cy3.tif";
    std::string outfilename = "out.tif";
    unsigned char *data;
    unsigned int width;
    unsigned int height;
    
    ImageIO::Read8bitGrayscaleTIFF(infilename,data,width,height);
    
    ImageIO::Write8bitGrayscaleTIFF(outfilename,data,width,height);
    
    delete[] data;
    data = NULL;
    
    return 0;
}