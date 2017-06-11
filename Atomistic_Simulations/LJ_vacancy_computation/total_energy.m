function [E_total,forces] = total_energy(sim_atoms,r_cutoff,vectors)
%This function calculates the total energy of the computational
% cell with periodic boundary conditions in addition to the forces 
% between the atoms. All atoms are looped over (1 to N) for i and j
% and x, y, and z periodic copies of the cell l, m, and n. 

%find length of column in sim_atom matrix to obtain the number of atoms
N_atoms = length(sim_atoms(:,1));

%find number of periodic copies of computational cell (l_max,m_max,n_max)
% and set min = -max. We must ensure that l_max*L*a > r_c (same for m & n).
%Use a celing function to obtain the integer above r_c/(L*a), etc. 
l_max = ceil(r_cutoff/vectors(1,1));
m_max = ceil(r_cutoff/vectors(2,2));
n_max = ceil(r_cutoff/vectors(3,3));

l_min = -l_max;
m_min = -m_max;
n_min = -n_max;


%calculate the total energy and forces 
E_total = 0;
forces = zeros(N_atoms,3);
for i=1:N_atoms
    for j=1:N_atoms
        for l=l_min:l_max
        for m=m_min:m_max
        for n=n_min:n_max
            d = (sim_atoms(i,:)-sim_atoms(j,:)+[l m n])*vectors;
            d_n = norm(d);
            
            %calcuate energy for distances larger than 0
            if d_n < r_cutoff && d_n > 0
                V = 4*((1/d_n)^12 - (1/d_n)^6);
                E_total = E_total + 0.5*V;
            
                %calculate forces 
                F = -24*((1/d_n)^7-2*(1/d_n)^13)*(d/d_n);
                forces(i,:) = forces(i,:) + F;
            end
        end
        end
        end
    end
end
end


