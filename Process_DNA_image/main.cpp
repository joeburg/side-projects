#include <iostream>

#include "imageanalysis.hpp"

int main()
{
  /* Instantiate a float version using data from a file */

  std::cout << "Instantiating instance of Image class using float and data from a file..." << std::endl;
  ImageAnalysis::Image<float>image1("cy3.tif");

  unsigned long int saturated1 = image1.CountPixelsGreaterThanOrEqual(1.);
  std::cout << "Number of saturated pixels = " << saturated1 << std::endl;

  image1.Threshold(0.78125);
  image1.Save("cy3_float_threshold.tif");

  /* Instantiate an unsigned char version using data from memory */

  unsigned char *data;
  unsigned int width, height;
  ImageIO::Read8bitGrayscaleTIFF("cy3.tif", data, width, height);

  std::cout << "Instantiating instance of Image class using unsigned char and data from memory..." << std::endl;
  ImageAnalysis::Image<unsigned char> image2(data, width, height);

  unsigned long int saturated2 = image2.CountPixelsGreaterThanOrEqual(255);
  std::cout << "Number of saturated pixels = " << saturated2 << std::endl;

  image2.Threshold(200);
  image2.Save("cy3_uchar_threshold.tif");

  delete[] data;

  return 0;
}
