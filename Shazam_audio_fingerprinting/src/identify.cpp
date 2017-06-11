#include <algorithm>
#include <cassert>
#include <map>
#include <math.h>
#include <set>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

#include "audioio.h"
#include "identify.hpp"
#include "mkl.h"

AudioIdentify::AudioIdentify(unsigned int windowsize, unsigned int overlap,
                             unsigned int neighborhood_size, unsigned int fan_value,
                             float threshold)
{
    this->windowsize = windowsize;
    this->overlap = overlap;
    this->neighborhood_size = neighborhood_size;
    this->fan_value = fan_value;
    this->threshold = threshold;
}

void AudioIdentify::AddToDatabase(std::string filename)
{
    infile = filename.c_str();
    ComputeFingerprints();
    database[filename] = fingerprints;
}

std::pair<std::string,double> AudioIdentify::FindMatches(std::string filename)
{
    infile = filename.c_str();
    ComputeFingerprints();
    
    // initialize best match pair
    double max_perct = 0;
    std::pair<std::string,double> bestmatch("",max_perct);
    
    // compare the fingerprints in the sample file to the fingerprints in the database
    for (auto &file : database)
    {
        std::set<std::size_t> intersect;
        std::set_intersection(file.second.begin(),file.second.end(),fingerprints.begin(),
                              fingerprints.end(),std::inserter(intersect,intersect.begin()));
        
        double frac_match = (double) intersect.size() / fingerprints.size();
        
        if ((frac_match > threshold) and (frac_match > max_perct))
        {
            max_perct = frac_match;
            bestmatch.first = file.first;
            bestmatch.second = max_perct;
        }
    }
    bestmatch.second *= 100; // change to %
    return bestmatch;
}


void AudioIdentify::ComputeFingerprints(void)
{
    // read the data from the input file
    int status = ReadWavFile(infile,&data,&nframes,&nchannels);
    if (status != 0) throw std::runtime_error("Could not read wav file.");
    
    // get the data from the first channel
    dataCH1 = std::vector<float>(nframes);
    for (unsigned int i=0; i < nframes; i++) dataCH1[i] = (float)data[i*nchannels];
    free(data); data = NULL;
    
    // compute the 2D spectrogram
    ComputeSpectrogram();
    
    // find the max peaks in the spectrogram
    FindLocalMaxima();
    
    // generating fingerprints using a hash funciton of pairs of peaks
    HashFingerprints();
}

void AudioIdentify::HashFingerprints(void)
{
    // refresh the fingerprint
    fingerprints.clear();
    
    std::hash<std::string> hash_fingerprint;
    long freq1, freq2, time1, time2;
    for (unsigned int i=0; i < localmaxima.size(); i++)
    {
        time1 = localmaxima[i][0];
        freq1 = localmaxima[i][1];
        for (unsigned int j=1; j < fan_value+1; j++)
        {
            if (i+j < localmaxima.size())
            {
                time2 = localmaxima[i+j][0];
                freq2 = localmaxima[i+j][1];
                
                std::stringstream s;
                s << freq1 << "|" << freq2 << "|" << time2-time1;
                std::string peaks = s.str();
                
                std::size_t fingerprint = hash_fingerprint(peaks);
                fingerprints.insert(fingerprint);
            }
        }
    }
}

void AudioIdentify::FindLocalMaxima(void)
{
    // refresh localmaxima data structure
    localmaxima.clear();
    
    for (long i=0; i < Ntime ; i++)
    {
        for (long j=0; j < Nfreq; j++)
        {
            bool isMax = true;
            long cntr_idx = i*Nfreq + j;
            for (long k = i - (neighborhood_size-1)/2; k <= i + (neighborhood_size-1)/2; k++)
            {
                // if neighborhood index goes outside the spectrogram, just continue
                if (k < 0 or k > Ntime-1) continue;
                
                for (long l = j - (neighborhood_size-1)/2; l <= j + (neighborhood_size-1)/2; l++)
                {
                    if (l < 0 or l > Nfreq-1) continue;
                    
                    if (spectrogram[k*Nfreq + l] > spectrogram[cntr_idx])
                    {
                        isMax = false;
                        break;
                    }
                }
                if (!isMax) break;
            }
            // powerspectrum value must be greater than 10 decibels
            std::array<long,2> max_idx = {i,j};
            if (isMax and (spectrogram[cntr_idx] > 10)) localmaxima.push_back(max_idx);
        }
    }
}

void AudioIdentify::ComputeSpectrogram(void)
{
    // refresh the spectrogram
    spectrogram.clear();
    
    Nfreq = (long)(windowsize/2)+1;
    Ntime = (long)(nframes - overlap)/(windowsize - overlap);
    k = (float)2/(windowsize*44100);
    kBD = (float)1/(windowsize*44100);
    
    std::vector<float> output(2*Nfreq);
    spectrogram.resize(Ntime*Nfreq);
    
    // congiure FFT handle
    MKL_LONG status;
    DFTI_DESCRIPTOR_HANDLE handle;
    status = DftiCreateDescriptor(&handle, DFTI_SINGLE, DFTI_REAL, 1, windowsize);
    assert(status == 0);
    
    status = DftiSetValue(handle, DFTI_NUMBER_OF_TRANSFORMS, 1);
    assert(status == 0);
    
    status = DftiSetValue(handle, DFTI_PLACEMENT, DFTI_NOT_INPLACE);
    assert(status == 0);
    
    status = DftiCommitDescriptor(handle);
    assert(status == 0);
    
    // compute spectrogram
    for (long i=0; i < Ntime; i++)
    {
        status = DftiComputeForward(handle, &dataCH1[i*(windowsize-overlap)], output.data());
        assert(status == 0);
        
        // compute row in spectrogram
        for (long j=0; j < Nfreq; j++)
        {
            float P;
            if (j == 0 or j == (Nfreq-1))
                P = 10*std::log10(kBD*(output[2*j]*output[2*j] + output[2*j+1]*output[2*j+1]));
            else
                P = 10*std::log10(k*(output[2*j]*output[2*j] + output[2*j+1]*output[2*j+1]));
            spectrogram[i*Nfreq + j] = P;
        }
    }
    
    // cleanup
    status = DftiFreeDescriptor(&handle);
    assert(status == 0);
}





