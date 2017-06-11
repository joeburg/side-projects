#ifndef glob_hpp
#define glob_hpp

#include <string>
#include <vector>

/*
   C++ style glob function for getting a vector of filenames
   matching a pattern.  For example, to get the names of all
   the wav files in the data/ directory:

   auto files = glob("data/*.wav");
*/

std::vector<std::string> glob(std::string path);

#endif /* glob_hpp */
