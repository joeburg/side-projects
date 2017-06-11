#include <iostream>
#include <string>

#include "include/container.hpp"

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        std::cout << "Usage:" << std::endl;
        std::cout << "  " << argv[0] << " <number of steps> " << std::endl;
        return 0;
    }

    std::string randFile = "data/random.txt";
    unsigned int Nparticles = 64;
    unsigned int Nsteps = 25;
    double mass = 48.0;
    double length = 4.2323167;
    double temp0 = 0.728;
    
    try
    {
        container<double> con(Nparticles,mass,length,temp0,Nsteps,randFile);
        con.RunSimulation();
    }
    catch (std::exception &e)
    {
        std::cerr << e.what() << std::endl;
    }
    
    return 0;
}
