//
//  identify.cpp
//  
//
//  Created by Joe Burg  on 2/23/15.
//
//

#include <algorithm>
#include <cassert>
#include <map>
#include <math.h>
#include <set>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

#include <iostream>

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
    // add exception about overlap and windowsize!!!
    
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
        std::set_intersection(file.second.begin(),file.second.end(),filename.begin(),
                              filename.end(),std::inserter(intersect,intersect.begin()));
        
        double frac_match = (double) intersect.size() / file.second.size();
        
        if ((frac_match > threshold) and (frac_match > max_perct))
        {
            max_perct = frac_match;
            bestmatch.first = file.first;
            bestmatch.second = max_perct;
        }
    }
    return bestmatch;
}


void AudioIdentify::ComputeFingerprints(void)
{
    // read the data from the input file
    int status = ReadWavFile(infile,&data,&nframes,&nchannels);
    if (status != 0) throw std::runtime_error("Could not read wav file.");
    
    //std::cout << "read file successfully" << std::endl;
    
    // get the data from the first channel
    dataCH1 = std::vector<float>(nframes);
    for (unsigned int i=0; i < nframes; i++) dataCH1[i] = (float)data[i*nchannels];
    free(data); data = NULL;
    
    //std::cout << "got Ch1 data succesfully" << std::endl;
    
    // compute the 2D spectrogram
    ComputeSpectrogram();
    
    //std::cout << "computed the spectrogram successfully" << std::endl;
    
    // find the max peaks in the spectrogram
    FindLocalMaxima();
    
    // generating fingerprints using a hash funciton of pairs of peaks
    HashFingerprints();
}

void AudioIdentify::HashFingerprints(void)
{
    std::hash<std::string> hash_fingerprint;
    unsigned int freq1, freq2, time1, time2;
    for (unsigned int i=0; i < localmaxima.size(); i++)
    {
        time1 = localmaxima[i][0];
        freq1 = localmaxima[i][1];
        for (unsigned int j=0; j < fan_value; j++)
        {
            time2 = localmaxima[i+j][0];
            freq2 = localmaxima[i+j][1];
            
            std::stringstream s;
            s << freq1 << "|" << freq2 << "|" << time2-time1;
            std::string peaks = s.str();
            
            std::size_t fingerprint = hash_fingerprint(peaks);
            fingerprints.insert(fingerprint);
            
            /*
            if (i==0 and j==0)
            {
                std::cout << peaks << std::endl;
                std::cout << fingerprint << std::endl;
            }
             */
        }
    }
    
}

void AudioIdentify::FindLocalMaxima(void)
{
    unsigned int i_trans, j_trans;
    float localmax;
    
    /*
    for (unsigned int i=0; i < Ntime; i++)
    {
        for (unsigned int j=0; j < Nfreq; j++)
        {
            // find the local max in the neighborhood centered at j+i*Nfreq
            localmax = spectrogram[i*Nfreq + j];
            for (unsigned int k=0; k < neighborhood_size; k++)
            {
                // transformed i coord between neighborhood  and image
                i_trans = i - neighborhood_size/2 + k;
                if ((i_trans < 0) or (i_trans > Ntime-1)) i_trans = 0;
                
                for (unsigned int l=0; l < neighborhood_size; l++)
                {
                    // transformed j coord between kernel and image
                    j_trans = j - neighborhood_size/2 + l;
                    if ((j_trans < 0) or (j_trans > Nfreq-1)) j_trans = 0;
                    
                    if (spectrogram[i_trans*Nfreq + j_trans] > localmax)
                    {
                        localmax = spectrogram[i_trans*Nfreq + j_trans];
                        //std::cout << spectrogram[i_trans*Nfreq + j_trans] << std::endl;
                    }
                }
            }
            // powerspectrum value must be greater than 10 decibels
            std::array<unsigned int,2> max_idx = {i,j};
            if (localmax >= 10) localmaxima.push_back(max_idx);
        }
    }
    */
    
    for (unsigned int i=0; i < Ntime; i++)
    {
        for (unsigned int j=0; j < Nfreq; j++)
        {
            bool isMax = true;
            // loop over neighborhood and check if any value is larger
        }
    }
    
    std::cout << "number of maixma = " << localmaxima.size() << std::endl;
}

void AudioIdentify::ComputeSpectrogram(void)
{
    Nfreq = (windowsize/2)+1;
    Ntime = (unsigned int)((nframes - overlap)/(windowsize - overlap) + 1);
    k = (float)2/(windowsize*44100);
    kBD = (float)1/(windowsize*44100);
    
    //std::cout << "initialized values" << std::endl;
    
    std::vector<float> output(2*Nfreq);
    spectrogram.resize(Ntime*Nfreq);
    
    //std::cout << "initialized data structures" << std::endl;
    
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
    
    //std::cout << "initialized handle " << std::endl;
    
    // compute spectrogram
    for (unsigned int i=0; i < Ntime; i++)
    {
        status = DftiComputeForward(handle, &dataCH1[i], output.data());
        assert(status == 0);
        
        //if (i==0) std::cout << output[0] << " " << output[2] << " " << output[4] << std::endl;
        
        //std::cout << "computed fft" << std::endl;
        
        // compute row in spectrogram
        for (unsigned int j=0; j < Nfreq; j++)
        {
            float P;
            if (j == 0 or j == (Nfreq-1))
            {
                P = 10*std::log10(kBD*(output[2*j]*output[2*j] + output[2*j+1]*output[2*j+1]));
                //std::cout << P << std::endl;
            }
            else
                P = 10*std::log10(k*(output[2*j]*output[2*j] + output[2*j+1]*output[2*j+1]));
            spectrogram[i*Nfreq + j] = P;
        }
    }
    
    //std::cout << spectrogram[0] << " " << spectrogram[1] << " " << spectrogram[2] << " " << spectrogram[3] << std::endl;
    //std::cout << "computed spectrogram" << std::endl;
    
    // cleanup
    status = DftiFreeDescriptor(&handle);
    assert(status == 0);
}





