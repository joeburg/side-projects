//
//  main.cpp
//  
//
//  Created by Joe Burg  on 11/17/14.
//
//

#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdio.h>
#include <string>

#include <boost/multi_array.hpp>
#include "image.hpp"

int main()
{
    std::string filename = "stanford.jpg";
    
    // load original image and compute sharpness
    image img(filename);
    unsigned int sharp0 = img.Sharpness();
    
    std::cout << "Original image:" << std::setw(4) << sharp0 << std::endl;
    
    // blur image and compute sharpness
    for (unsigned int i=3; i < 28; i += 4)
    {
        //std::cout << i << std::endl;
        image img2(filename);
        
        // blur image
        img2.BoxBlur(i);
        
        // save image to .jpg file
        std::ostringstream stream;
        std::string outfile;
        stream << "BoxBlur" << std::setw(2) << std::setfill('0') << i << ".jpg";
        outfile = stream.str();
        img2.Save(outfile);
        
        // compute sharpness
        unsigned int sharp = img2.Sharpness();
        
        // display status on screen
        std::cout << "BoxBlur(" << std::setw(2)<< i << "):" << std::setw(7) << sharp << std::endl;
    }
    return 0;
}