//
//  identify.h
//  
//
//  Created by Joe Burg  on 2/23/15.
//
//

#ifndef identify_hpp
#define identify_hpp

#include <map>
#include <set>
#include <string>
#include <utility>
#include <vector>

class AudioIdentify
{
    private:
    unsigned int windowsize, overlap, neighborhood_size, fan_value;
    long Nfreq, Ntime;
    float threshold, k, kBD;
    
    const char *infile;
    short *data = NULL;
    long nframes = 0;
    int nchannels = 0;
    
    std::vector<float> dataCH1, spectrogram;
    std::vector<std::array<long,2>> localmaxima;
    std::set<std::size_t> fingerprints;
    std::map<std::string,std::set<std::size_t>> database;
    
    void ComputeFingerprints(void);
    void ComputeSpectrogram(void);
    void FindLocalMaxima(void);
    void HashFingerprints(void);
    
    public:
    AudioIdentify(unsigned int windowsize, unsigned int overlap,
                  unsigned int neighborhood_size, unsigned int fan_value,
                  float threshold);
    void AddToDatabase(std::string filename);
    std::pair<std::string,double> FindMatches(std::string filename);
};

#endif /* identify_hpp */
