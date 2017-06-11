//
//  imageio.h
//  
//
//  Created by Joe Burg on 1/12/15.
//
//

#ifndef IMAGEIO_HPP
#define IMAGEIO_HPP

#include <string>

namespace ImageIO
{
    void Read8bitGrayscaleTIFF(std::string filename,
                               unsigned char * &data,
                               unsigned int &width,
                               unsigned int &height);
    
    void Write8bitGrayscaleTIFF(std::string filename,
                                unsigned char * data,
                                unsigned int width,
                                unsigned int height);
}

#endif /* IMAGEIO_HPP */
