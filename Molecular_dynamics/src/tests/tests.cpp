#include <array>
#include <cppunit/ui/text/TestRunner.h>
#include <cppunit/TestCase.h>
#include <cppunit/TestCaller.h>
#include <cppunit/extensions/HelperMacros.h>
#include <string>

#include "container.hpp"

class SimulationTest: public CppUnit::TestCase
{
    /* setup a suite of tests */
    CPPUNIT_TEST_SUITE( SimulationTest );
    CPPUNIT_TEST( TestInitSimulation );
    CPPUNIT_TEST( TestRestartSimulation );
    CPPUNIT_TEST_SUITE_END();
    
    public:
    SimulationTest() : CppUnit::TestCase("Simulation Test") {}
    
    /* implementation of the tests */
    void TestInitSimulation()
    {
        unsigned int Nsteps = 10;
        unsigned int Nparticles = 64;
        double mass = 48.0;
        double length = 4.2323167;
        double temp0 = 0.728;
        
        std::string inputfile = "solution0.dat";
        
        container<double> con(Nparticles,mass,length,temp0,Nsteps,inputfile);
        con.RunSimulation();
        
        std::array<double,3> energy = con.GetEnergy();
        double totalE = energy[0];
        double totalKE = energy[1];
        double totalU = energy[2];
        
        // chech if the energy level are within the tolerance of the solution
        double tol = 1.e-10;
        CPPUNIT_ASSERT(std::abs(totalU - (-323.5277900792)) < tol);
        CPPUNIT_ASSERT(std::abs(totalKE - 65.4308062926) < tol);
        CPPUNIT_ASSERT(std::abs(totalE - (-258.0969837866)) < tol);
    }
    
    void TestRestartSimulation()
    {
        unsigned int Nsteps = 10;
        unsigned int Nparticles = 64;
        double mass = 48.0;
        double length = 4.2323167;
        double temp0 = 0.728;
        
        std::string inputfile = "solution10_ref.dat";
        
        container<double> con(Nparticles,mass,length,temp0,Nsteps,inputfile);
        con.RunSimulation();
        
        std::array<double,3> energy = con.GetEnergy();
        double totalE = energy[0];
        double totalKE = energy[1];
        double totalU = energy[2];
        
        // chech if the energy level are within the tolerance of the solution
        double tol = 1.e-10;
        CPPUNIT_ASSERT(std::abs(totalU - (-311.5666041769)) < tol);
        CPPUNIT_ASSERT(std::abs(totalKE - 53.4727891310) < tol);
        CPPUNIT_ASSERT(std::abs(totalE - (-258.0938150458)) < tol);
    }
};


int main(void)
{
    CppUnit::TextUi::TestRunner runner;
    runner.addTest(SimulationTest::suite());
    bool successful = runner.run();
    return !successful;
}
