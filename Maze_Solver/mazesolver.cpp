/* Purpose: code to implement the right hand wall following algorithm */

#include <iostream>
#include <fstream>
#include <string>
#define ni 201
#define nj 201

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        std::cout << "Usage:" << std::endl;
        std::cout << "  " << argv[0] << " <maze file> <solution file>" << std::endl;
        return 0;
    }
    
    std::string filename = argv[1];
    std::string ofilename = argv[2];
    
    // Initialize the array values to 1
    int maze[ni][nj];
    int n = 1;
    for (int i = 0; i < ni; i++)
    {
        for (int j = 0; j < nj; j++)
        {
            maze[i][j] = n;
        }
    }
    
    // Read the array values from maze file
    std::ifstream f(filename);
    int nif, njf;
    if (f.is_open())
    {
        // Read the size of the data and make sure storage is sufficient
        f >> nif >> njf;
        if (nif > ni or njf > nj)
        {
            std::cout << "Not enough storage available!" << std::endl;
            return 0;
        }
        
        // Read the data and populate the array
        int i, j;
        while (f >> i >> j)
        {
            maze[i][j] = 0; //wall present
        }
    }
    f.close();
    
    // Open output file to write maze solution
    int N_steps = 1; // already have starting position
    std::ofstream of;
    of.open(ofilename);
    if (of.is_open())
    {
        // Find the maze entrance in first row and store in solution file
        int pos_x;
        int pos_y = 0;
        for (int i = 0; i < njf; i++)
        {
            if (maze[pos_y][i])
            {
                pos_x = i;
                of << 0 << " " << pos_x << std::endl;
                break;
            }
        }
        
        // Right hand wall following algorithm
        // first enumerate the possible directions
        enum direction
        {
            north,
            south,
            east,
            west
        };
        
        /* since the first row only has one entry point, the first
         direction will always be south */
        direction d = south;
        
        /* for a given direction, always try to move right first;
         if you can move right make sure you change directions;
         then try forward and finally left (change direction)
         keep iterating until final row is reached */
        while (pos_y != nif-1)
        {
            // store positions to the right and forward
            int posr[2] = {pos_y,pos_x};
            int posf[2] = {pos_y,pos_x};
            switch (d)
            {
                case north:
                    posr[1]++;
                    posf[0]--;
                    break;
                    
                case south:
                    posr[1]--;
                    posf[0]++;
                    break;
                 
                case east:
                    posr[0]++;
                    posf[1]++;
                    break;
                    
                case west:
                    posr[0]--;
                    posf[1]--;
                    break;
            }
            
            // if you can turn right, turn right and switch direction
            if (maze[posr[0]][posr[1]])
            {
                pos_y = posr[0];
                pos_x = posr[1];
                N_steps++;
                of << pos_y << " " << pos_x << std::endl;
                switch (d)
                {
                    case north: d = east; break;
                    case south: d = west; break;
                    case east: d = south; break;
                    case west: d = north; break;
                }
                    
            }
            
            // if you can go forward, move
            else if (maze[posf[0]][posf[1]])
            {
                pos_y = posf[0];
                pos_x = posf[1];
                N_steps++;
                of << pos_y << " " << pos_x << std::endl;
            }
            
            // else just turn left (switch direction)
            else
            {
                switch (d)
                {
                    case north: d = west; break;
                    case south: d = east; break;
                    case east: d = north; break;
                    case west: d = south; break;
                }
            }
        }
    }
    of.close();
    
    std::cout << "Maze solved!" << std::endl;
    std::cout << "Number of steps taken: " << N_steps << std::endl;
    return 0;
}