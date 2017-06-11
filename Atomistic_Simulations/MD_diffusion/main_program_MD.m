%Calculate LJ vibration frequencies
%Joe Burg 
%HW 3

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%use LJ units
%atom positions are LJ units (not scaled)

clear;
kb_T=4.0;
dt=0.0001;
nsteps=200000;

%set size of computational cell
L=3;
M=L;
N=L;

%potential minimum is 2^(1/6)
%set lattice constant (cubic primitive cell)
lattice=sqrt(2)*2^(1/6);
%lattice=lattice*0.95;  %can scale lattice constant

rcut=1.3;

%set lattice vectors
latvec=[L*lattice 0 0; 0 M*lattice 0; 0 0 N*lattice];

%set up computational cell for perfect xtal
atoms=setup_cell(L,M,N,latvec);
[natoms,temp]=size(atoms);
   
%initialize velocities
[velocities,atoms_old]=initialize_velocities(atoms,latvec,kb_T,dt);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %main program for verlet integration and equilibrium 
% 
% for time=1:nsteps
%     if (rcut*2<latvec(1,1) && rcut*2<latvec(2,2) && rcut*2<latvec(3,3))
%       [pot_e(time),forces]=calc_energy_faster(atoms,latvec,rcut,1);
%     else
%         [pot_e(time),forces]=calc_energy(atoms,latvec,rcut,1);
%     end
%     
%     %verlet integration
%     [atoms_new,velocities]=integrate(atoms,atoms_old,velocities,forces,latvec,dt);
%     
%     %calculate the kinetic energy
%     [instantaneous_kb_T(time),kin_e(time)]=calc_ke(velocities,natoms);
%     
%     %total energy calculation
%     total_energy(time)=kin_e(time)+pot_e(time);
%     
%     %access initial energy
%     total_energy_t0 = total_energy(1);
%     
%     %store velocity information
%     saved_velocities(time,:,:)=velocities;
%     
%     %calculate temperature deviation
%     deviation_kb_T(time)=1/(3*natoms)*(total_energy(time)-total_energy_t0);
%     
%     %redefine atoms 
%     atoms_old=atoms;
%     atoms=atoms_new;
%     time
% end
% 
% % figure;
% % plot(instantaneous_kb_T,'-')  
% % figure;
% % plot(deviation_kb_T,'-')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %obtaining the vibrational spectrum
% 
% %compute the fast fourier transform to transform the velocities to 
% % frequency space 
% for i=1:natoms
%     for j=1:3
%         vel_freq_space(:,i,j)=fft(saved_velocities(:,i,j));
%     end 
% end
% 
% %calculate the power spectrum P(w)
% for i=1:nsteps
%     v=abs(squeeze(vel_freq_space(i,:,:)));
%     P(i,:)=sum(diag(v'*v))/(3*natoms);
% end
% 
% freq = [1:nsteps-1]/(nsteps*dt);
% 
% plot(freq(1:round(end/2)),P(1:round(end/2)))

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%calculating the diffusion coefficient

%initialize atoms
atoms_initial = atoms;

for time=1:nsteps
    if (rcut*2<latvec(1,1) && rcut*2<latvec(2,2) && rcut*2<latvec(3,3))
      [pot_e(time),forces]=calc_energy_faster(atoms,latvec,rcut,1);
    else
        [pot_e(time),forces]=calc_energy(atoms,latvec,rcut,1);
    end
    
    %verlet integration
    [atoms_new,velocities]=integrate(atoms,atoms_old,velocities,forces,latvec,dt);
    
    %calculate the kinetic energy
    [instantaneous_kb_T(time),kin_e(time)]=calc_ke(velocities,natoms);
    
    %total energy calculation
    total_energy(time)=kin_e(time)+pot_e(time);
    
    %access initial energy
    total_energy_t0 = total_energy(1);
    
    %store velocity information
    saved_velocities(time,:,:)=velocities;
    
    %calculate temperature deviation
    deviation_kb_T(time)=1/(3*natoms)*(total_energy(time)-total_energy_t0);
    
    %redefine atoms 
    atoms_old=atoms;
    
    %calculate diffusion coeff
    mean_sqr_disp(time)=sum(sum(abs(atoms-atoms_initial).^2))/natoms;   
    atoms=atoms_new; 
    
    time
end

%plotting the mean square displcement and energy deviation
figure;
time=[0:dt:dt*(nsteps-1)];
plot(time,mean_sqr_disp)
xlabel('time')
ylabel('mean square displacement')
title('L = M = N = 3; dt = 0.0001; kbT = 4.0')

figure; 
plot(time,deviation_kb_T)
xlabel('time')
ylabel('k_{b}T_{deviation}')
title('L = M = N = 3; dt = 0.0001; kbT = 4.0')

%Compute P(w)
for i=1:natoms
    for j=1:3
        vel_freq_space(:,i,j)=fft(saved_velocities(:,i,j));
    end 
end

for i=1:nsteps
    v=abs(squeeze(vel_freq_space(i,:,:)));
    P(i,:)=sum(diag(v'*v))/(3*natoms);
end

figure;
freq = [1:nsteps-1]/(nsteps*dt);
plot(freq(1:round(end/2)),P(1:round(end/2)))
ylabel('P(\omega)')
xlabel('\omega')
title('L = M = N = 3; dt = 0.0001; kbT = 4.0')