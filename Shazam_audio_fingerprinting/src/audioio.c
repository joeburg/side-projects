#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sndfile.h>

int ReadWavFile(const char *filename, short **data, long *nframes, int *nchannels)
{
  /* Open sound file */

  SF_INFO sndInfo;
  memset(&sndInfo, 0, sizeof(SF_INFO));
  SNDFILE *sndFile = sf_open(filename, SFM_READ, &sndInfo);
  if (sndFile == NULL)
  {
    return 1;
  }

  /* Check format, should be 16 bit PCM */

  if (sndInfo.format != (SF_FORMAT_WAV | SF_FORMAT_PCM_16))
  {
    return 2;
  }

  /* Allocate memory */

  *nframes = sndInfo.frames;
  *nchannels = sndInfo.channels;

  *data = NULL;
  *data = (short *) malloc((unsigned long)(sndInfo.channels*sndInfo.frames)*sizeof(short));
  if (*data == NULL)
  {
    return 3;
  }

  /* Read the file */

  long nframesread = sf_readf_short(sndFile, *data, sndInfo.frames);
  if (nframesread != sndInfo.frames)
  {
    free(*data);
    return 4;
  }

  sf_close(sndFile);

  return 0;
}

#ifdef USE_MAIN
int main()
{
  /* Test code for a two channel sample file */

  char *filename = "Chopin_EtudeOp25No1.wav";
  short *data = NULL;
  long nframes = 0;
  int nchannels = 0;
 
  int status = ReadWavFile(filename, &data, &nframes, &nchannels);
  if (status != 0)
  {
    printf("Could not read wav file, status = %u\n", status);
    return 1;
  }

  printf("nframes = %ld\n", nframes);
  printf("nchannels = %d\n", nchannels);

  for (long n = 0; n < 16; n++)
  {
    printf("%8ld %6d %6d\n", n, data[2*n], data[2*n+1]);
  }
  printf("     ...\n");
  for (long n = nframes-3; n < nframes; n++)
  {
    printf("%8ld %6d %6d\n", n, data[2*n], data[2*n+1]);
  }

  free(data); data = NULL;
  nframes = 0;

  return 0;
}
#endif /* USE_MAIN */
