%Joe Burg
%monte carlo, MC_move

%use LJ units
%atom positions are LJ units (not scaled)

function [etot_sequence,atoms,rejected_configs] = MC_move(atoms,latvec,natoms,mc_max_move,rcut,beta,etot,rejected_configs)
%rejected_config=scalar

atoms_Old=atoms; 

%choose random atom
atomNumber = randi(natoms,1); %number of atom picked up
rand_atom = atoms_Old(atomNumber,:); %atoms picked up

rand_move=rand(1,3); %random number for moving the picked atom

atoms_new=atoms;
atoms_new(atomNumber,1)=rand_atom(1,1)+(rand_move(1,1)-0.5)*mc_max_move;
atoms_new(atomNumber,2)=rand_atom(1,2)+(rand_move(1,2)-0.5)*mc_max_move;
atoms_new(atomNumber,3)=rand_atom(1,3)+(rand_move(1,3)-0.5)*mc_max_move;

etot_Old=etot;

[etot_New,forces]=calc_energy_faster(atoms_new,latvec,rcut,0);


if (etot_New < etot_Old)
    atoms=atoms_new;
    etot_sequence=etot_New;
elseif (rand(1) < exp(-beta*(etot_New-etot_Old)))
    atoms=atoms_new;
    etot_sequence=etot_New;
else
    atoms=atoms_Old;
    rejected_configs=rejected_configs+1; %add number of rejected configs
    etot_sequence=etot;
end

end

