%Joe Burg, HW2
%Lennard Jones Model: fcc crystal energies, forces, vacancies,
%energy minimization, interstitials, relaxed and unrelaxed lattice 

clear;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%initialize size of computational cell
L = 1;
M = L;
N = L; 

%define unit vectors 
vectors = eye(3);

%use minimum energy lattice constant and create a scale parameter
a = 2^(2/3);
a_scale = 1.0;
a = a_scale*a;

%create vectors scaled by the lattice constant and the cell size
vectors = a*[L 0 0;0 M 0;0 0 N].*vectors;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%perfect fcc crystal
%compute the total energy of the system and forces on the atoms
sim_atoms = computational_cell(L,M,N);
N_atoms = length(sim_atoms(:,1));
r_cutoff = 3.0;

[E_total,forces] = total_energy(sim_atoms,r_cutoff,vectors);

%print energy per atom and the forces 
E_atom = E_total/N_atoms
forces;

% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%creating a vacany in the lattice 
%remove the last atom from the crystal to create a vacancy 
sim_atoms_vac = sim_atoms(1:N_atoms-1,:);

%compute the total energy and forces 
[E_tot_vac, forces_vac] = total_energy(sim_atoms_vac,r_cutoff,vectors)

%calculate the vacancy energy
E_vac = E_tot_vac - ((N_atoms-1)/N_atoms)*E_total


%convergence of vacancy energy
max_L = 2;
energies = zeros(1,max_L);
index = 1:max_L
for L = 1:max_L
    M = L;
    N = L;
    
    vectors_loop = eye(3);
    vectors_loop = a*[L 0 0;0 M 0;0 0 N].*vectors_loop;
    clear sim_atoms;
    sim_atoms = computational_cell(L,M,N);
    N_atoms = length(sim_atoms(:,1));
    
    %calculate total energy of perfect lattice 
    [E_total_loop,forces]=total_energy(sim_atoms,r_cutoff,vectors_loop);
    %calculate total energy of lattice with vacancy
    [E_tot_vac_loop,forces]=total_energy(sim_atoms(1:N_atoms-1,:),...
        r_cutoff,vectors_loop)
    %determine vacancy energy
    E_vac_loop = E_tot_vac_loop - ((N_atoms-1)/N_atoms)*E_total_loop;
    energies(:,L) = energies(:,L) + E_vac_loop
end

plot(index,energies,'-o')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %minimize the energy with respect to atom positions 
% 
% %set alpha and force tolerance 
% alpha = 1e-3;
% force_tol = 1e-2;
% 
% %calculate the vacancy energy then minimize the energy
% for L = 1:2
%     M = L;
%     N = L;
%     
%     %setup cell and vectors 
%     vectors = [L*a 0 0;0 M*a 0;0 0 N*a];
%     clear sim_atoms N_atoms;
%     sim_atoms = computational_cell(L,M,N);
%     
%     %create a vacancy
%     N_atoms = length(sim_atoms(:,1));
%     sim_atoms = sim_atoms(1:N_atoms-1,:);
%  
%     %minimize the energy with respect to atoms positions with a vacancy
%     [energy_min,atoms_min]=minimize_energy(sim_atoms,r_cutoff,...
%         vectors,force_tol,alpha);
%     
%     E_vac_min(L) = energy_min - (N_atoms-1)*E_atom;
%     max_disp(L)=max(max((sim_atoms-atoms_min)*vectors));
% end    
% 
% max_disp
% E_vac_min
% plot(E_vac_min,'-o')


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %place an interstitial in cell and determine choice of alpha
% 
% %set alpha and force tolerance 
% alpha = 5e-2;
% force_tol = 1e-2;
% 
% %calculate the vacancy energy then minimize the energy
% for L = 1:3
%     M = L;
%     N = L;
%     
%     %setup cell and vectors 
%     vectors = [L*a 0 0;0 M*a 0;0 0 N*a];
%     clear sim_atoms N_atoms;
%     sim_atoms = computational_cell(L,M,N);
%     
%     %create a vacancy
%     N_atoms = length(sim_atoms(:,1));
%     sim_atoms(N_atoms+1,:) = [0.5/L 0.5/M 0.5/N];
%  
%     %minimize the energy with respect to atoms positions with a vacancy
%     [energy_min,atoms_min]=minimize_energy(sim_atoms,r_cutoff,...
%         vectors,force_tol,alpha);
%     
%     E_interstitial(L) = energy_min - (N_atoms+1)*E_atom;
%     max_disp(L)=max(max((sim_atoms-atoms_min)*vectors));
% end    
% 
% max_disp
% E_interstitial
% plot(E_interstitial,'-o')
