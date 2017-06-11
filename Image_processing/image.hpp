#ifndef IMAGE_HPP
#define IMAGE_HPP

#include <string>

#include "assignment6.hpp"
#include <boost/multi_array.hpp>


class image
{
    // private data attributes of class
    std::string filename;
    std::string outfile;
    boost::multi_array<unsigned char,2> orig_img;
    unsigned int N;
    
    // private methods used in image class
    void Convolution(boost::multi_array<unsigned char,2> &input,
                     boost::multi_array<unsigned char,2> &output,
                     boost::multi_array<float,2> &kernel);
    
    // public methods
    public:
    image(std::string filename);
    void BoxBlur(unsigned int N);
    unsigned int Sharpness();
    void Save(std::string outfile);
};

#endif /* IMAGE_HPP */