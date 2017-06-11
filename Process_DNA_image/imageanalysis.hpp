#ifndef IMAGEANALYSIS_HPP
#define IMAGEANALYSIS_HPP

#include <algorithm>
#include <limits>
#include <string>

#include "imageio.hpp"

namespace ImageAnalysis
{
    template <typename T>
    class Image
    {
    private:
        T *data;
        T max;
        T min;
        unsigned int width;
        unsigned int height;
        unsigned int capacity;
        void SetMaxMin();
        
    public:
        Image(std::string filename);
        Image(T *data, unsigned int width, unsigned int height);
        void Save(std::string filename);
        void Threshold(T threshold);
        unsigned long int CountPixelsGreaterThanOrEqual(T value = (T)0);
        ~Image();
    };
    
    
    template<>
    void Image<unsigned char>::SetMaxMin()
    {
        /*Private method to set the min/max values for unsigned char data */
        min = 0;
        max = 255;
    }
    
    template<>
    void Image<float>::SetMaxMin()
    {
        /*Private method to set the min/max values for float data */
        min = 0.f;
        max = 1.f;
    }
    
    template <typename T>
    Image<T>::Image(std::string filename)
    {
        /*Constructor that loads the data and writes it to memory */
        ImageIO::Read8bitGrayscaleTIFF(filename,data,width,height);
        capacity = width*height;
        SetMaxMin(); // set maximum based on data type
    }
    
    template <>
    Image<float>::Image(std::string filename)
    {
        /*Constructor that loads the data and writes it to memory
         specifically for float data */
        // create pointer that will point to location in memory where the
        // unsigned char data that will be read in is located
        unsigned char *dataUC;
        ImageIO::Read8bitGrayscaleTIFF(filename,dataUC,width,height);
        capacity = width*height;
        
        // set max for float
        SetMaxMin();
        
        // convert 8 bit grayscale to float
        data = new float[capacity];
        for (unsigned int n=0; n < capacity; n++)
            data[n] = (float)dataUC[n]/255.f;
        
        delete[] dataUC;
    }
    
    template <typename T>
    Image<T>::Image(T *data, unsigned int width, unsigned int height)
    {
        /* allocate memory and copy existing memory to location */
        capacity = width*height;
        this->width = width;
        this->height = height;
        this->data = new T[capacity];
        std::copy(data,data+capacity,this->data);
        
        SetMaxMin();
    }
    
    template <typename T>
    void Image<T>::Save(std::string filename)
    {
        /* method to save the current state of an image */
        ImageIO::Write8bitGrayscaleTIFF(filename,data,width,height);
    }
    
    template <>
    void Image<float>::Save(std::string filename)
    {
        /*convert float values to unsigned char; create pointer to
         local data that will be converted to unsigned char */
        unsigned char *dataUC = new unsigned char[capacity];
        for (unsigned int n=0; n < capacity; n++)
            dataUC[n] = (unsigned char)(data[n]*255);
        
        ImageIO::Write8bitGrayscaleTIFF(filename,dataUC,width,height);
        
        delete[] dataUC;
    }
    
    template <typename T>
    void Image<T>::Threshold(T threshold)
    {
        /* method that sets pixel values to a maximum or minimum
         based on a threshold */
        for (unsigned int n=0; n < capacity; n++)
        {
            if (data[n] < threshold)
                data[n] = min;
            else
                data[n] = max;
        }
    }
    
    template <typename T>
    unsigned long int Image<T>::CountPixelsGreaterThanOrEqual(T value)
    {
        /* method that returns the number of pixels that have value greater than
         or equal to a given value */
        unsigned long int N = 0;
        for (unsigned int n=0; n < capacity; n++)
        {
            if (data[n] >= value) N++;
        }
        
        return N;
    }
    
    template <typename T>
    Image<T>::~Image()
    {
        if (data)
        {
            delete[] data;
            data = NULL;
        }
    }
}
#endif /* IMAGEANALYSIS_HPP */
