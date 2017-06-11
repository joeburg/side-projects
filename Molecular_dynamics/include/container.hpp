#ifndef CONTAINER_HPP
#define CONTAINER_HPP

#include <algorithm>
#include <array>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <vector>

#include "macros.hpp"
#include "operators.hpp"
#include "particle.hpp"
#include "swap.hpp"

template <typename T>
class container
{
    private:
    std::vector<particle<T> > particles, particles_h;
    std::vector<std::array<T,3> > forces, forces_h;
    T mass, length, temp0;
    T h = (T)0.01; // time step
    unsigned int Nparticles;
    int Nsteps, StartStep=0;
    T totalU, totalKE, totalE;
    std::string inputfile,outputfile,datatype,fileformat;
    
    void InitPositionCubic(void);
    void InitVelocity(void);
    
    void SetRestartDatType(void);
    void RestartDatBinary(void);
    void RestartDatAscii(void);
    void RestartVtk(void);
    void WriteState(int step);
    void WriteToVtk(int step, std::ofstream& of);
    void WriteToDat(int step, std::ofstream& of);
    void SetDataType(void);
    std::string outfileName(int step);
    
    T Potential(T r);
    void InternalForce(unsigned int i, bool nextstep);
    std::array<T,3> Verlet(std::array<T,3> r, std::array<T,3> v, std::array<T,3> a);
    std::array<T,3> VelVerlet(std::array<T,3> v, std::array<T,3> a, std::array<T,3> a_h);
    void ComputeEnergy(void);
    
    public:
    container(unsigned int Nparticles,T mass, T length, T temp0,
              int Nsteps, std::string inputfile);
    void RunSimulation(int savefreq=-1, std::string outputfile="");
    #ifndef SWIG
    std::array<T,3> GetEnergy(void);
    #endif
};

template <typename T>
container<T>::container(unsigned int Nparticles,T mass, T length, T temp0,
                        int Nsteps, std::string inputfile)
{
    this->Nparticles = Nparticles;
    this->mass = mass;
    this->length = length;
    this->temp0 = temp0;
    this->Nsteps = Nsteps;
    this->inputfile = inputfile;
    
    SetDataType(); // double or float
    
    if (inputfile.empty())
    {
        InitPositionCubic();
        InitVelocity();
        
        // since no input file, check for output file to set file format
        std::size_t found = outputfile.find(".vtk");
        if (found != std::string::npos) fileformat = ".vtk";
        else fileformat = ".dat";
    }
    else
    {
        // restart as a .vtk file or as a .dat/.txt file
        std::size_t found = inputfile.find(".vtk");
        if (found != std::string::npos)
        {
            fileformat = ".vtk";
            RestartVtk();
        }
        else
        {
            fileformat = ".dat";
            SetRestartDatType();
        }
    }
}

template <typename T>
void container<T>::RunSimulation(int savefreq, std::string outputfile)
{
    this->outputfile = outputfile;
    particles_h = std::vector<particle<T>>(Nparticles);
    forces = std::vector<std::array<T,3>>(Nparticles);
    forces_h = std::vector<std::array<T,3>>(Nparticles);
    std::array<T,3> r,v,a,a_h;
    
    std::cout << "Timestep      TotalU           TotalKE          TotalE " << std::endl;
    std::cout << "--------  ---------------  ---------------  ---------------" << std::endl;
    int iter = 0;
    for (int t=StartStep; t < StartStep+Nsteps+1; t++)
    {
        ComputeEnergy();
        std::cout << std::setw(5) << t << "     " << std::setw(15) << std::fixed << std::setprecision(10) << \
        totalU << "   "  << totalKE << "   " << totalE << "   " << std::endl;
        
        /* initilize all forces to 0; this is done here since we will
        compute Fij and Fji simultaneously */
        for (unsigned int i=0; i < Nparticles; i++)
        {
            forces[i] = {(T)0,(T)0,(T)0};
            forces_h[i] = {(T)0,(T)0,(T)0};
        }
        
        for (unsigned int i=0; i < Nparticles; i++)
        {
            r = particles[i].GetPos();
            v = particles[i].GetVel();
            InternalForce(i,false);
            a = (1/mass)*forces[i];
            
            particles_h[i].SetPos(Verlet(r,v,a));
            particles[i].SetAccl(a);
        }
        
        for (unsigned int i=0; i < Nparticles; i++)
        {
            v = particles[i].GetVel();
            a = particles[i].GetAccl();
            InternalForce(i,true);
            a_h = (1/mass)*forces_h[i];
            
            particles_h[i].SetVel(VelVerlet(v,a,a_h));
        }

        /* write positions and velocities of the last step
         as well as every savefreq steps */
        if (t == StartStep+Nsteps) WriteState(t);
        else if (iter == savefreq)
        {
            WriteState(t);
            iter = 1;
        }
        else iter++;
        
        for (unsigned int i=0; i < Nparticles; i++)
        {
            // update particles positions and velocities
            particles[i].SetPos(particles_h[i].GetPos());
            particles[i].SetVel(particles_h[i].GetVel());
        }
    }
}

template <typename T>
std::string container<T>::outfileName(int step)
{
    /* finds the first and last ? in output file string, sets
    the length of ?'s to width and generates output file with 
     step number, 0 padding, and the file format */
    std::size_t baseidx = outputfile.find("?");
    std::size_t lastidx = outputfile.find_last_of("?");
    std::string base = outputfile.substr(0,baseidx);
    std::stringstream s;
    s << base << std::setw(lastidx-baseidx+1) << std::setfill('0') << step << fileformat;
    return s.str();
}

template <typename T>
void container<T>::WriteState(int step)
{
    /* write system state to file if output file given and last step reached;
     both writes are in binary */
    if (!outputfile.empty())
    {
        std::string outfile = outfileName(step);
        
        std::ofstream of;
        of.open(outfile, std::ios::binary);
        if (of.is_open())
        {
            if (fileformat == ".vtk") WriteToVtk(step, of);
            else WriteToDat(step, of);
            of.close();
            std::cout << "Solution saved to: " << outfile << std::endl;
        }
        else
        {
            std::stringstream s;
            s << "ERROR: Writing to file " << outfile << " failed!";
            ThrowException(s.str());
        }
    }
}

template <typename T>
void container<T>::WriteToDat(int step, std::ofstream& of)
{
    // write file in .dat binary format
    of << "BINARY" << std::endl;
    of.write((char *)&step, sizeof(int));
    for (unsigned int i=0; i < Nparticles; i++)
    {
        std::array<T,3> r = particles[i].GetPos();
        for (unsigned int i=0; i < 3; i++) of.write((char *)&r[i], sizeof(T));
        
        std::array<T,3> v = particles[i].GetVel();
        for (unsigned int i=0; i < 3; i++) of.write((char *)&v[i], sizeof(T));
    }
}

template <typename T>
void container<T>::WriteToVtk(int step, std::ofstream& of)
{
    // write file in .vtk binary format
    // vlk header
    of << "# vtk DataFile Version 3.0" << std::endl;
    of << "vtk output" << std::endl;
    of << "BINARY" << std::endl;
    of << "DATASET POLYDATA" << std::endl;
    
    // time information
    T time = step*h;
    
    of << "FIELD FieldData 2" << std::endl;
    of << "TIME 1 1 " << datatype << std::endl;
    char bufT[sizeof(T)];
    swap(time, bufT);
    of.write(bufT, sizeof(T));
    
    of << "CYCLE 1 1 int" << std::endl;
    char bufint[sizeof(int)];
    swap(step, bufint);
    of.write(bufint,sizeof(int));
    
    // positions
    of << "POINTS " << Nparticles << " " << datatype << std::endl;
    for (unsigned int i=0; i < Nparticles; i++)
    {
        std::array<T,3> r = particles[i].GetPos();
        for (unsigned int j=0; j < 3; j++)
        {
            char buf[sizeof(T)];
            swap(r[j], buf);
            of.write(buf, sizeof(T));
        }
    }

    // point data
    of << "POINT_DATA " << Nparticles << std::endl;
    of << "SCALARS particle " << datatype << std::endl;
    of << "LOOKUP_TABLE default" << std::endl;
    for (unsigned int n = 0; n < Nparticles; n++)
    {
        char buf[sizeof(T)];
        swap((T)1, buf);
        of.write(buf, sizeof(T));
    }
    
    // velocities
    of << "VECTORS velocity " << datatype << std::endl;
    for (unsigned int i=0; i < Nparticles; i++)
    {
        std::array<T,3> v = particles[i].GetVel();
        for (unsigned int j=0; j < 3; j++)
        {
            char buf[sizeof(T)];
            swap(v[j], buf);
            of.write(buf, sizeof(T));
        }
    }
}

template <typename T>
void container<T>::SetRestartDatType(void)
{
    particles = std::vector<particle<T>>(Nparticles);
    
    std::ifstream f;
    f.open(inputfile, std::ios::in);
    if (f.is_open())
    {
        std::string filetype;
        std::getline(f,filetype);
        if (filetype == "ASCII") RestartDatAscii();
        else RestartDatBinary();
    }
    else
    {
        std::stringstream s;
        s << "ERROR: Reading file " << inputfile << " failed!";
        ThrowException(s.str());
    }
}

template <typename T>
void container<T>::RestartDatBinary(void)
{
    // restart from a binary file in .dat format
    std::ifstream f;
    f.open(inputfile, std::ios::binary);
    
    // read past binary indicator
    std::string garbage;
    std::getline(f,garbage);
    f.read((char *)&StartStep, sizeof(int));
    std::cout << "Restarting at time step " << StartStep << " from file: " << inputfile << std::endl;
    
    for (unsigned int i=0; i < Nparticles; i++)
    {
        std::array<T,3> r = {(T)0,(T)0,(T)0};
        for (unsigned int i=0; i < 3; i++) f.read((char *)&r[i], sizeof(T));
        
        std::array<T,3> v = {(T)0,(T)0,(T)0};
        for (unsigned int i=0; i < 3; i++) f.read((char *)&v[i], sizeof(T));
        
        particle<T> p;
        p.SetPos(r);
        p.SetVel(v);
        particles[i] = p;
    }
    f.close();
}

template <typename T>
void container<T>::RestartDatAscii(void)
{
    std::cout << "restarting from ascii .dat.." << std::endl;
    
    // restart from a ASCII file in .dat format
    std::ifstream f;
    f.open(inputfile, std::ios::in);
    
    std::string garbage;
    std::getline(f,garbage); // read past ascii indicator
    f >> StartStep;
    std::cout << "Restarting at time step " << StartStep << " from file: " << inputfile << std::endl;
    
    for (unsigned int i=0; i < Nparticles; i++)
    {
        std::array<T,3> v = {(T)0,(T)0,(T)0};
        std::array<T,3> r = {(T)0,(T)0,(T)0};
        f >> r[0] >> r[1] >> r[2] >> v[0] >> v[1] >> v[2];
        particle<T> p;
        p.SetPos(r);
        p.SetVel(v);
        particles[i] = p;
    }
    f.close();
}

template <typename T>
void container<T>::RestartVtk(void)
{
    particles = std::vector<particle<T>>(Nparticles);
    
    std::ifstream f;
    f.open(inputfile, std::ios::binary);
    if (f.is_open())
    {
        std::string garbage;
        T time;
        char buf[sizeof(T)];
        char bufint[sizeof(int)];
        
        // get starting timestep
        for (unsigned int i=0; i < 6; i++) std::getline(f,garbage);
        f.read(buf, sizeof(T));
        unswap(buf, &time);
        
        std::getline(f,garbage);
        f.read(bufint, sizeof(int));
        unswap(bufint, &StartStep);
        
        // read in positions
        std::getline(f,garbage);
        for (unsigned int i=0; i < Nparticles; i++)
        {
            std::array<T,3> r = {(T)0,(T)0,(T)0};
            for (unsigned int j=0; j < 3; j++)
            {
                f.read(buf, sizeof(T));
                unswap(buf, &r[j]);
            }
            particle<T> p;
            p.SetPos(r);
            particles[i] = p;
        }
         
        for (unsigned int i=0; i < 3; i++) std::getline(f,garbage);
        for (unsigned int i=0; i < Nparticles; i++)
        {
            f.read(buf, sizeof(T));
        }
        
        // read in velocities
        std::getline(f,garbage);
        for (unsigned int i=0; i < Nparticles; i++)
        {
            std::array<T,3> v = {(T)0,(T)0,(T)0};
            for (unsigned int j=0; j < 3; j++)
            {
                f.read(buf, sizeof(T));
                unswap(buf, &v[j]);
            }
            particles[i].SetVel(v);
        }
        f.close();
    }
    else
    {
        std::stringstream s;
        s << "ERROR: Reading file " << inputfile << " failed!";
        ThrowException(s.str());
    }
}


template <typename T>
void container<T>::InitPositionCubic(void)
{
    particles = std::vector<particle<T>>(Nparticles);
    unsigned int Ncube = 1;
    while (Nparticles > (Ncube*Ncube*Ncube)) Ncube++;
    
    if ((Ncube*Ncube*Ncube) != Nparticles)
        ThrowException("CubicInit Warning: Particle number is not a perfect cube.");
    
    T rs = length/Ncube;
    T roffset = length/2 - rs/2;
    unsigned int Nadd = 0;
    std::array<T,3> r;
    for (unsigned int x = 0; x < Ncube; x++)
    {
        for (unsigned int y = 0; y < Ncube; y++)
        {
            for (unsigned int z = 0; z < Ncube; z++)
            {
                if (Nadd < Nparticles)
                {
                    particle<T> p;
                    r = {rs*x - roffset,rs*y - roffset, rs*z - roffset};
                    p.SetPos(r);
                    particles[Nadd] = p;
                    Nadd++;
                }
            }
        }
    }
}

template <typename T>
void container<T>::InitVelocity(void)
{    
    std::default_random_engine generator;
    std::uniform_real_distribution<T> distribution(-0.5,0.5);
    
    unsigned int initNDIM = 3;
    std::array<T,3> netP = {(T)0,(T)0,(T)0};
    T netE = (T)0;
    
    T newP;
    std::array<T,3> v;
    for (unsigned int n=0; n < Nparticles; n++)
    {
        v = {(T)0,(T)0,(T)0};
        for (unsigned int x=0; x < initNDIM; x++)
        {
            newP = distribution(generator);
            netP[x] += newP;
            netE += newP*newP;
            v[x] = newP;
        }
        particles[n].SetVel(v);
    }
    
    netP = ((T)1/Nparticles)*netP;
    T vscale = std::sqrt(3*Nparticles*temp0/(mass*netE));
    
    for (unsigned int n=0; n < Nparticles; n++)
    {
        v = particles[n].GetVel();
        v = vscale*(v - netP);
        particles[n].SetVel(v);
    }
}

template <typename T>
T container<T>::Potential(T r)
{
    T r6 = (T)std::pow(r,6);
    T r12 = r6*r6;
    return (4*(1/r12 - 1/r6));
}

template <typename T>
std::array<T,3> container<T>::Verlet(std::array<T,3> r, std::array<T,3> v, std::array<T,3> a)
{
    std::array<T,3> r_h = r + h*v + ((T)0.5*h*h)*a;
    return r_h;
}

template <typename T>
std::array<T,3> container<T>::VelVerlet(std::array<T,3> v, std::array<T,3> a, std::array<T,3> a_h)
{
    std::array<T,3> v_h = v + ((T)0.5*h)*(a + a_h);
    return v_h;
}

template <typename T>
void container<T>::InternalForce(unsigned int i, bool nextstep)
{
    /* computes all the forces on atom i as well as updates the equal but 
     opposite forces as a optimization; takes a bool which indicates if the 
     forces are being computed on the next step or the current step */
    std::array<T,3> dF;
    for (unsigned int j=i+1; j < Nparticles; j++)
    {
        // either computes forces for current step or next step
        if (nextstep)
        {
            dF = particles_h[i].ComputeForce(particles_h[j],length);
            
            for (unsigned int k=0; k < 3; k++)
            {
                forces_h[i][k] += dF[k];
                forces_h[j][k] -= dF[k];
            }
        }
        else
        {
            dF = particles[i].ComputeForce(particles[j],length);
            
            for (unsigned int k=0; k < 3; k++)
            {
                forces[i][k] += dF[k];
                forces[j][k] -= dF[k];
            }
        }
    }
}

template <typename T>
void container<T>::ComputeEnergy(void)
{
    totalU=(T)0; totalKE=(T)0; totalE=(T)0;
    std::array<T,3> vi;
    for (unsigned int i=0; i < Nparticles; i++)
    {
        vi = particles[i].GetVel();
        totalKE += (T)0.5*mass*(vi[0]*vi[0] + vi[1]*vi[1] + vi[2]*vi[2]);
        for (unsigned int j=0; j < i; j++)
            totalU += Potential(particles[i].Distance(particles[j],length));
    }
    totalE = totalKE + totalU;
}

template <typename T>
std::array<T,3> container<T>::GetEnergy(void)
{
    std::array<T,3> energy = {totalE,totalKE,totalU};
    return energy;
}

template <>
void container<double>::SetDataType(void)
{
    datatype = "double";
}

template <>
void container<float>::SetDataType(void)
{
    datatype = "float";
}


#endif /* CONTAINER_HPP */
