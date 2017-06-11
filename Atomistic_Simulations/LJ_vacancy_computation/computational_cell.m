function sim_atoms = computational_cell( L,M,N )
%This function sets up a computational cell consisting of 
% LxMxN periodic copies of an fcc crystal with the 
% corresponding basis atoms.

%create a cubic fcc unit cell with 4 basis atoms 
N_basis=4;
basis_atom(1,:)=[0 0 0];
basis_atom(2,:)=[0.5 0.5 0];
basis_atom(3,:)=[0 0.5 0.5];
basis_atom(4,:)=[0.5 0 0.5];

%make copies of the unit cell with LxMxN dimension; 
%displace each atom by some vector [i j k] in each loop
%keep track of the number of atoms in the computational cell
N_atom=0;
for i=0:L-1;
    for j=0:M-1
        for k=0:N-1
            for l = 1:N_basis
            sim_atoms(N_atom+l,:) = basis_atom(l,:) + [i j k];
            end
        N_atom = N_atom + N_basis;
        end
    end
end

%scale the atom coordinates
sim_atoms(:,1) = sim_atoms(:,1)/L;
sim_atoms(:,2) = sim_atoms(:,2)/M;
sim_atoms(:,3) = sim_atoms(:,3)/N;