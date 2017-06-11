#include <iomanip>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

#include "glob.hpp"
#include "identify.hpp"


int main(int argc, char *argv[])
{
  if (argc != 3)
  {
    std::cout << "Usage:" << std::endl;
    std::cout << "  " << argv[0] << " <reference dir> <sample dir>" << std::endl;
    return 1;
  }

  std::string refdir = argv[1];
  std::string sampledir = argv[2];

  try
  {
    AudioIdentify a(4096, 2048, 37, 15, 0.05);

    std::cout << "Adding reference files to database..." << std::endl;
    auto reflist = glob(refdir + "/*.wav");
    for (auto &reffile : reflist)
    {
      a.AddToDatabase(reffile);
      std::cout << reffile << " added." << std::endl;
    }

    std::cout << "\nAttempting to identify samples..." << std::endl;
    auto samplelist = glob(sampledir + "/*.wav");
    for (auto &samplefile : samplelist)
    {
      std::cout << "Analyzing sample: " << samplefile << std::endl;
      auto match_info = a.FindMatches(samplefile);

      if (match_info.first == "")
      {
        std::cout << "No match found! :( \n" << std::endl;
      }
      else
      {
        std::cout << "Match found: " << match_info.first << std::endl;
        std::cout << "Percentage matched: " << std::setprecision(4) << match_info.second;
        std::cout << "%\n" << std::endl;
      }
    }
  }
  catch(std::exception &e)
  {
    std::cerr << "ERROR: " << e.what() << std::endl;
  }

  return 0;
}
