/* Purpose: image class that can read and write JPEG files
computes the sharpness of the image and blur the image */



#define BOOST_DISABLE_ASSERTS
#include <iostream>
#include <boost/multi_array.hpp>
#include <limits>

#include "image.hpp"


// private methods used in image class
void image::Convolution(boost::multi_array<unsigned char,2> &input,
                 boost::multi_array<unsigned char,2> &output,
                 boost::multi_array<float,2> &kernel)
{
    // get dimensions of kernel
    auto shape = kernel.shape();
    auto nrows = shape[0];
    auto ncols = shape[1];
    
    // get dimensions of orig image
    auto shape_img = orig_img.shape();
    auto Nr_img = shape_img[0];
    auto Nc_img = shape_img[1];
    
    // check if kernel has appropriate properties
    if (nrows != ncols)
    {
        std::cerr << "ERROR: Kernel is not square." << std::endl;
        exit(1);
    }
    else if (nrows % 2 == 0)
    {
        std::cerr << "ERROR: Kernel must have odd size." << std::endl;
        exit(1);
    }
    else if (nrows < 3)
    {
        std::cerr << "ERROR: Kernel must be at least of size 3." << std::endl;
        exit(1);
    }
    
    // obtain each pixel in image (center of kernel)
    for (int i=0; i < (int)Nr_img ; i++)
    {
        for (int j=0; j < (int)Nc_img; j++)
        {
            // compute convolution with kernel
            float sum = 0;
            int i_trans, j_trans;
            for (int k=0; k < (int)nrows; k++)
            {
                i_trans = i - ((int)nrows-1)/2 + k;  // transformed i coord between kernel and image
                if (i_trans < 0)
                    i_trans = 0;
                else if (i_trans > (int)Nr_img-1)
                    i_trans = (int)Nr_img - 1;
                
                for (int l=0; l < (int)nrows; l++)
                {
                    j_trans = j - ((int)nrows-1)/2 + l;  // transformed j coord between kernel and image
                    if (j_trans < 0)
                        j_trans = 0;
                    else if (j_trans > (int)Nc_img-1)
                        j_trans = (int)Nc_img - 1;
                    
                    sum += input[i_trans][j_trans]*kernel[k][l];
                }
            }
            
            // update each pixel in output with sum
            float char_max = std::numeric_limits<unsigned char>::max();
            float char_min = std::numeric_limits<unsigned char>::min();
            sum = std::min(sum,char_max);
            sum = std::max(sum,char_min);
            output[i][j] = (unsigned char)sum;
        }
    }
}


// constructor for image class
image::image(std::string filename)
{
    this->filename = filename;
    
    // load data from jpeg file
    ReadGrayscaleJPEG(this->filename, orig_img);
}

// method to blur an image
void image::BoxBlur(unsigned int N)
{
    // build the kernel based on given size
    boost::multi_array<float,2> kernel(boost::extents[N][N]);
    for (unsigned int i=0; i < N; i++)
    {
        for (unsigned int j=0; j < N; j++)
            kernel[i][j] = 1/((float)N*(float)N);
    }
    
    // smooth image using kernel
    auto copy = orig_img;
    Convolution(copy,orig_img,kernel);
}

// method to compute the sharpness of an image
unsigned int image::Sharpness(void)
{
    // initialize laplacian operator
    boost::multi_array<float,2> laplacian(boost::extents[3][3]);
    for (unsigned int i=0; i<3; i++)
    {
        for (unsigned int j=0; j<3; j++)
        {
            if (i==1 and j==1)
                laplacian[i][j] = -4.;
            else if ((i==0 and j==1) or (i==1 and j==0) or (i==1 and j==2) or (i==2 and j==1))
                laplacian[i][j] = 1.;
            else
                laplacian[i][j] = 0.;
        }
    }
    
    // convolute image with laplacian
    auto shape_img = orig_img.shape();
    auto Nr_img = shape_img[0];
    auto Nc_img = shape_img[1];
    boost::multi_array<unsigned char,2> sharp_img(boost::extents[Nr_img][Nc_img]);
    
    Convolution(orig_img,sharp_img,laplacian);
    
    // find maximum of sharp image to return sharpness
    unsigned char sharpness = 0;
    for (unsigned int i=0; i < Nr_img; i++)
    {
        for (unsigned int j=0; j < Nc_img; j++)
        {
            if (sharp_img[i][j] > sharpness)
                sharpness = sharp_img[i][j];
        }
    }
    return (unsigned int)sharpness;
}

// method to save an image
void image::Save(std::string outfile)
{
    // if outfile string is empty use filename
    if (outfile == "")
        outfile = this->filename;
    
    // write blurred image to file
    WriteGrayscaleJPEG(outfile,orig_img);
}