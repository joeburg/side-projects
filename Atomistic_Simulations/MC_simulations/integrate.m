function [atoms_new,velocities] = integrate(atoms,atoms_old,velocities,forces,latvec,dt)
%Function that implements the Verlet algorithm.  This is an integration
% scheme that obtains the atoms new positions and velocities. 

%r(t+dt) = atoms new
%r(t-dt) = atoms old
%r(t+dt) = -r(t-dt)+2r(t)+F(t)/m *dt^2
%v(t) = [r(t+dt)-r(t-dt)]/(2dt)

atoms_new = -atoms_old + 2*atoms + forces*dt^2;
velocities = (atoms_new - atoms_old)/(2*dt);
end

