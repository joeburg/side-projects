#ifndef CONTAINER_HPP
#define CONTAINER_HPP

#include <algorithm>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <typeinfo>
#include <vector>

#include "macros.hpp"
#include "operators.hpp"
#include "particle.hpp"
#include "swap.hpp"

template <typename T>
class container
{
    private:
    std::vector<particle<T>> particles, NextParticles;
    T mass, length, temp0;
    T h = (T)0.01; // time step
    unsigned int Nparticles;
    int Nsteps, StartStep=0;
    T totalU, totalKE, totalE;
    std::string inputfile, outputfile;
    
    void InitPositionCubic(void);
    void InitVelocity(void);
    void Restart(void);
    void WriteState(void);
    std::string GetDataType(void);
    
    T Potential(T r);
    std::vector<T> InternalForce(unsigned int i, bool next);
    std::vector<T> Verlet(std::vector<T> r, std::vector<T> v, std::vector<T> a);
    std::vector<T> VelVerlet(std::vector<T> v, std::vector<T> a, std::vector<T> a_h);
    void ComputeEnergy(void);
    
    public:
    container(unsigned int Nparticles,T mass, T length, T temp0,
              int Nsteps, std::string inputfile);
    void RunSimulation(std::string outputfile="");
    #ifndef SWIG
    std::vector<T> GetEnergy(void);
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
    
    if (inputfile.empty())
    {
        InitPositionCubic();
        InitVelocity();
    }
    else
    {
        Restart();
    }
}

template <typename T>
void container<T>::RunSimulation(std::string outputfile)
{
    this->outputfile = outputfile;
    NextParticles = std::vector<particle<T>>(Nparticles);
    std::vector<T> r,v,a,na,F;
    
    std::cout << "Timestep      TotalU           TotalKE          TotalE " << std::endl;
    std::cout << "--------  ---------------  ---------------  ---------------" << std::endl;
    for (int t=StartStep; t < StartStep+Nsteps+1; t++)
    {
        ComputeEnergy();
        std::cout << std::setw(5) << t << "     " << std::setw(15) << std::fixed << std::setprecision(10) << \
        totalU << "   "  << totalKE << "   " << totalE << "   " << std::endl;
        
        for (unsigned int i=0; i < Nparticles; i++)
        {
            r = particles[i].GetPos();
            v = particles[i].GetVel();
            a = (1/mass)*InternalForce(i,false);
            
            NextParticles[i].SetPos(Verlet(r,v,a));
            particles[i].SetAccl(a);
        }
        
        for (unsigned int i=0; i < Nparticles; i++)
        {
            v = particles[i].GetVel();
            a = particles[i].GetAccl();
            na = (1/mass)*InternalForce(i,true);
            
            NextParticles[i].SetVel(VelVerlet(v,a,na));
        }

        // write positions and velocities of the last step
        if (t == StartStep+Nsteps) WriteState();
        
        for (unsigned int i=0; i < Nparticles; i++)
        {
            // update particles positions and velocities
            particles[i].SetPos(NextParticles[i].GetPos());
            particles[i].SetVel(NextParticles[i].GetVel());
        }
    }
}

template <typename T>
void container<T>::Restart(void)
{
    particles = std::vector<particle<T>>(Nparticles);
    
    std::ifstream f;
    //f.open(inputfile, std::ios::in);
    f.open(inputfile, std::ios::binary);
    if (f.is_open())
    {
        /*
        //f >> StartStep;
        f.read((char *)&StartStep, sizeof(unsigned int));
        std::cout << "Restarting at time step " << StartStep << " from file: " << inputfile << std::endl;

        for (unsigned int i=0; i < Nparticles; i++)
        {
            std::vector<T> v(3,(T)0);
            std::vector<T> r(3,(T)0);
            //f >> r[0] >> r[1] >> r[2] >> v[0] >> v[1] >> v[2];
            f.read((char *)&r[0], sizeof(T));
            f.read((char *)&r[1], sizeof(T));
            f.read((char *)&r[2], sizeof(T));
            f.read((char *)&v[0], sizeof(T));
            f.read((char *)&v[1], sizeof(T));
            f.read((char *)&v[2], sizeof(T));
            
            particle<T> p;
            p.SetPos(r);
            p.SetVel(v);
            particles[i] = p;
        }
        */
        
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
        
        std::cout << "Startstep = " << StartStep << std::endl;
        
        // read in positions
        std::getline(f,garbage);
        for (unsigned int i=0; i < Nparticles; i++)
        {
            std::vector<T> r(3,(T)0);
            for (unsigned int j=0; j < 3; j++)
            {
                f.read(buf, sizeof(T));
                unswap(buf, &r[j]);
            }
            particle<T> p;
            p.SetPos(r);
            particles[i] = p;
        }
        
        // read in velocities
        std::getline(f,garbage);
        for (unsigned int i=0; i < Nparticles; i++)
        {
            std::vector<T> v(3,(T)0);
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
void container<T>::WriteState(void)
{
    // write system state to file if output file given and last step reached
    if (!outputfile.empty())
    {
        std::ofstream of;
        //of.precision(30);
        of.open(outputfile, std::ios::binary);
        if (of.is_open())
        {
            /*
            //of << StartStep+Nsteps << std::endl;
            unsigned int step = StartStep+Nsteps;
            of.write((char *)&step, sizeof(unsigned int));
            //std::cout << step << std::endl;
            
            for (unsigned int i=0; i < Nparticles; i++)
            {
                std::vector<T> r = particles[i].GetPos();
                std::vector<T> v = particles[i].GetVel();
                //of << r[0] << " " << r[1] << " " << r[2] << " " << v[0] << " " << v[1] << " " << v[2] << std::endl;
                of.write((char *)&r[0], sizeof(T));
                of.write((char *)&r[1], sizeof(T));
                of.write((char *)&r[2], sizeof(T));
                of.write((char *)&v[0], sizeof(T));
                of.write((char *)&v[1], sizeof(T));
                of.write((char *)&v[2], sizeof(T));
            }
             */
            
            char buf[sizeof(T)];
            char bufint[sizeof(int)];
            
            // vlk header
            of << "# vtk DataFile Version 3.0" << std::endl;
            of << "vtk output" << std::endl;
            of << "BINARY" << std::endl;
            of << "DATASET POLYDATA" << std::endl;
            
            // time information
            int step = StartStep+Nsteps;
            T time = step*h;
            
            of << "FIELD FieldData 2" << std::endl;
            of << "TIME 1 1 " << typeid(time).name() << std::endl;
            //char bufT[sizeof(T)];
            swap(time, buf);
            of.write(buf, sizeof(T));
            
            of << "CYCLE 1 1 int" << std::endl;
            //char bufui[sizeof(int)];
            swap(step, bufint);
            of.write(bufint,sizeof(int));
            
            // positions
            of << "POINTS " << Nparticles << " " << typeid(time).name() << std::endl;
            for (unsigned int i=0; i < Nparticles; i++)
            {
                std::vector<T> r = particles[i].GetPos();
                for (unsigned int j=0; j < 3; j++)
                {
                    //char buf[sizeof(T)];
                    swap(r[j], buf);
                    of.write(buf, sizeof(T));
                }
            }
            
            // velocities
            of << "VECTORS velocity " << typeid(time).name() << std::endl;
            for (unsigned int i=0; i < Nparticles; i++)
            {
                std::vector<T> v = particles[i].GetVel();
                for (unsigned int j=0; j < 3; j++)
                {
                    //char buf[sizeof(T)];
                    swap(v[j], buf);
                    of.write(buf, sizeof(T));
                }
            }
            
            // vertices
            char one[sizeof(int)];
            swap(1, one);
            of << "VERTICES " << Nparticles << " " << 2*Nparticles << std::endl;
            for (int i=0; i< Nparticles; i++)
            {
                of.write(one, sizeof(int));
                //char buf[sizeof(int)];
                swap(i,bufint);
                of.write(bufint,sizeof(int));
            }
            
            // point data
            of << "POINT_DATA " << Nparticles << std::endl;
            of << "SCALARS element " << typeid(time).name() << std::endl;
            of << "LOOKUP_TABLE default" << std::endl;
            for (unsigned int n = 0; n < Nparticles; n++)
            {
                of.write(one, sizeof(int));
            }
            
            of.close();
            std::cout << "Solution saved to: " << outputfile << std::endl;
        }
        else
        {
            std::stringstream s;
            s << "ERROR: Writing to file " << outputfile << " failed!";
            ThrowException(s.str());
        }
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
    std::vector<T> r;
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
    std::vector<T> netP(3,(T)0);
    T netE = (T)0;
    
    T newP;
    std::vector<T> v;
    for (unsigned int n=0; n < Nparticles; n++)
    {
        v.resize(3,(T)0);
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
std::vector<T> container<T>::Verlet(std::vector<T> r, std::vector<T> v, std::vector<T> a)
{
    std::vector<T> r_h = r + h*v + ((T)0.5*h*h)*a;
    return r_h;
}

template <typename T>
std::vector<T> container<T>::VelVerlet(std::vector<T> v, std::vector<T> a, std::vector<T> a_h)
{
    std::vector<T> v_h = v + ((T)0.5*h)*(a + a_h);
    return v_h;
}

template <typename T>
std::vector<T> container<T>::InternalForce(unsigned int i, bool next)
{
    std::vector<T> F(3,(T)0);
    std::vector<T> dF;
    for (unsigned int j=0; j < Nparticles; j++)
    {
        if (j != i)
        {
            if (next) dF = NextParticles[i].ComputeForce(NextParticles[j],length);
            else dF = particles[i].ComputeForce(particles[j],length);
            
            for (unsigned int k=0; k < 3; k++) F[k] += dF[k];
        }
    }
    return F;
}

template <typename T>
void container<T>::ComputeEnergy(void)
{
    totalU=(T)0; totalKE=(T)0; totalE=(T)0;
    std::vector<T> vi;
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
std::vector<T> container<T>::GetEnergy(void)
{
    std::vector<T> energy = {totalE,totalKE,totalU};
    return energy;
}

template <>
std::string container<double>::GetDataType(void)
{
    
}


#endif /* CONTAINER_HPP */
