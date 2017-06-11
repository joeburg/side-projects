// Demonstrates reading and writing a TIFF file using libtiff

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "tiffio.h"

int main(int argc, char *argv[])
{
  TIFF *tif = NULL;
  unsigned int n;
  unsigned int width, height;
  unsigned char *rgba, *grayscale;
  char *inputfile = NULL, *outputfile = NULL;

  /* Confirm program was called correctly. */

  if (argc != 3)
  {
    printf("Usage:\n");
    printf("  %s <input file> <output file>\n", argv[0]);
    return 0;
  }
  inputfile = argv[1];
  outputfile = argv[2];

  /* Open the input file for read. */

  tif = TIFFOpen(inputfile, "r");
  if (!tif)
  {
    printf("ERROR: Failed to open %s for input!\n", inputfile);
    return 1;
  }

  /* Read fields from the input file. */

  TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &width);
  TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &height);

  /* Read the image in RGBA format (8 bits per channel).  Use an unsigned char
     pointer so the individual channels are easily accessible. */

  rgba = (unsigned char *) _TIFFmalloc(4*width*height*sizeof(unsigned char));
  TIFFReadRGBAImage(tif, width, height, (unsigned int *)rgba, 0);

  /* Convert RGBA data to grayscale using average method. */

  grayscale = (unsigned char *) malloc(width*height*sizeof(unsigned char));
  for(n = 0; n < width*height; n++)
  {
    /* Average the sum of the R, G, and B channels. */
    grayscale[n] = (unsigned char)(((unsigned int)rgba[4*n+0] +
                                    (unsigned int)rgba[4*n+1] +
                                    (unsigned int)rgba[4*n+2])/3);
  }

  /* Free RGBA memory and close the file. */

  _TIFFfree(rgba);
  rgba = NULL;

  TIFFClose(tif);
  tif = NULL;

  /* Open output file for write. */

  tif = TIFFOpen(outputfile, "w");
  if (!tif)
  {
    printf("ERROR: Failed to open %s for output!\n", outputfile);
    return 1;
  }

  /* Write fields to the output file. */

  TIFFSetField(tif, TIFFTAG_IMAGEWIDTH, width);
  TIFFSetField(tif, TIFFTAG_IMAGELENGTH, height);
  TIFFSetField(tif, TIFFTAG_BITSPERSAMPLE, 8);
  TIFFSetField(tif, TIFFTAG_SAMPLESPERPIXEL, 1);
  TIFFSetField(tif, TIFFTAG_ORIENTATION, 4);

  /* Write the grayscale data to the output file. */

  TIFFWriteEncodedStrip(tif, 0, grayscale, width*height);

  /* Close the output file and free remaining memory. */

  TIFFClose(tif);
  tif = NULL;

  free(grayscale);
  grayscale = NULL;

  return 0;
}
