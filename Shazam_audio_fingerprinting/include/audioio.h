#ifndef audioio_h
#define audioio_h

#ifdef __cplusplus
extern "C" {
#endif

int ReadWavFile(const char *filename, short **data, long *nframes, int *nchannels);

#ifdef __cplusplus
}
#endif

#endif /* audioio_h */
