function [E_total,sim_atoms] = minimize_energy(sim_atoms,r_cutoff,vectors,force_tol,alpha)
%The purpose of this fucntion is to minimize the energy of 
% the system with respect to atom positions.  

%choose initial position of atoms and calculate the forces 
[E_total,forces] = total_energy(sim_atoms,r_cutoff,vectors);

%move atoms in direction of forces and repeat if any force 
%component is larger than the force tolerance 
while max(max(forces)) > force_tol
    sim_atoms = sim_atoms + alpha*forces/vectors;
    
    [E_total,forces]=total_energy(sim_atoms,r_cutoff,vectors);
end
