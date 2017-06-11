function [kb_T,KE] = calc_ke(velocities,natoms)
%calculate the kinetic energy and temperatue

%KE = 1/2 mv^2
%kbT = (2/3N)*KE
%set mass = 1 
m = 1.0;

%calcuate the kinetic energy
KE = 0.5*m*sum(sum(velocities.^2));

%calculate the temperatue 
kb_T = (2/(3*natoms))*KE;

end

