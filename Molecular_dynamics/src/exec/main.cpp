#include <iostream>
#include <string>
#include <unistd.h>

#include "container.hpp"
#include "macros.hpp"
#include "timer.h"

int main(int argc, char *argv[])
{
    std::string inputfile = "";
    std::string outputfile = "";
    
    if (argc < 2)
    {
        std::cout << "Usage:" << std::endl;
        std::cout << "  " << argv[0] << " <number of steps> [-o outputfile] [-i inputfile]" << std::endl;
        return 0;
    }
    
    int c;
    while ((c = getopt(argc,argv,":i:o:")) != -1)
    {
        switch (c)
        {
            case 'i': inputfile = optarg; break;
            case 'o': outputfile = optarg; break;
            default: break;
        }
    }
    unsigned int Nsteps = (unsigned int)std::stoi(argv[optind]);

    unsigned int Nparticles = 64;
    double mass = 48.0;
    double length = 4.2323167;
    double temp0 = 0.728;
    
    try
    {
        double t0 = timer();
        container<double> con(Nparticles,mass,length,temp0,Nsteps,inputfile);
        con.RunSimulation(-1,outputfile);
        double elapsedtime = timer() - t0;
        std::cout << "Time elapsed " << elapsedtime << " seconds." << std::endl;
    }
    catch (std::exception &e)
    {
        std::cerr << e.what() << std::endl;
    }
    
    return 0;
}
