%Joe Burg 
%MatSci 331 HW #4-5
%simulated annealing

%use LJ units
%atom positions are LJ units (not scaled)

clear;
rejected_configs=0; %number of configurations rejected through Boltzmann criterion
kb_T=0.11;
beta=1.0/kb_T;
nsteps=250000;
mc_max_move=0.1; %maximum spatial move in x, y, and z directions for single atom random displacement (in LJ units)

delta_kb_T=-kb_T/nsteps   %do simulated annealing

%anneal schedule 1
delta_kb_T_1=(-kb_T/nsteps)*(5/2); 
delta_kb_T_2=(-kb_T/nsteps)*(5/8);

%anneal schedule 2
dT1 = (-kb_T/nsteps)*3;
dT2 = (-kb_T/nsteps)*(5/9);
dT3 = (-kb_T/nsteps)*3;

%anneal schedule 3
dT4 = (-kb_T/nsteps)*(5/9);
dT5 = (-kb_T/nsteps)*5;
%delta_kb_T=0;

%initialize random number generator to produce same sequence every time the
%code is run.  This enables reproduction of results.
s=RandStream('mt19937ar');
RandStream.setGlobalStream(s);
reset(s,1);

%set size of computational cell
L=2;
M=L;
N=L;


%potential minimum is 2^(1/6)
%set lattice constant (cubic primitive cell)
lattice=sqrt(2)*2^(1/6);
%lattice=sqrt(2)*2^(1/6)*2.0;
%lattice=lattice*1.1;  %can scale lattice constant



rcut=1.3;

%set lattice vectors
latvec=[L*lattice 0 0; 0 M*lattice 0; 0 0 N*lattice];

%set up computational cell for perfect xtal
atoms=setup_cell(L,M,N,latvec);

%make cube of fcc xtal
latvec=latvec*2;

[natoms,temp]=size(atoms);
atoms_start=atoms; %for use in calculating diffusion coefficient

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%write initial atoms positions to file
%atoms_initial = fopen('atoms_initial.txt', 'w')
atoms_label = ones(1,natoms);
atoms_label = atoms_label';
output_atoms_initial = [atoms_label,atoms];
file = 'atoms_initial_2000MC.xyz';
numatom = ['32'];
atomlabel = ['Atoms'];
dlmwrite(file,numatom,'delimiter','%d','-append')
dlmwrite(file,atomlabel,'delimiter','','-append')
dlmwrite(file,output_atoms_initial,'delimiter','\t','-append')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%calculate the energy of the perfect crystal
if (rcut*2<latvec(1,1) && rcut*2<latvec(2,2) && rcut*2<latvec(3,3))
     [etot_perfect_xtal,forces]=calc_energy_faster(atoms,latvec,rcut,1);
     etot_perfect_xtal=etot_perfect_xtal/natoms;
     etot=etot_perfect_xtal;
else
    disp('Cell too small for calc_energy_faster');
    quit;
end

for step=1:nsteps
    
    step
   
    %output for movie; write atoms every 100 steps 
    if mod(step,100) == 0  
        atoms_label = ones(1,natoms);
        atoms_label = atoms_label';
        output_atoms_final = [atoms_label,atoms];
        file2 = 'atoms_final.xyz';
        numatom = ['32'];
        atomlabel = ['Atoms'];
        dlmwrite(file2,numatom,'delimiter','%d','-append')
        dlmwrite(file2,atomlabel,'delimiter','','-append')
        dlmwrite(file2,output_atoms_final,'delimiter','\t','-append')
    end
    
    [etot_sequence(step),atoms,rejected_configs] = MC_move(atoms,latvec,natoms,mc_max_move,rcut,beta,etot,rejected_configs);
    etot=etot_sequence(step);
    
    rejected_configs/step;

    %Calculate <r>^2
    r=(atoms-atoms_start);
    r_squared(step)=sum(sum(r.*r))/natoms;
    
%     %annealing schedule 1
%     %fast anneal. long quench
%     if step <= (nsteps/5)
%         kb_T=kb_T+delta_kb_T_1;
%         beta=1/kb_T;
%     else
%         kb_T=kb_T+delta_kb_T_2;
%         beta=1/kb_T;
%     end

%     %anneal schedule 2
%     if step <= (nsteps/20)
%         kb_T = kb_T + dT1;
%         beta=1/kb_T;
%     elseif step <= (9*nsteps)/10
%         kb_T = kb_T + dT2;
%         beta=1/kb_T;
%     else
%         kb_T = kb_T + dT3;
%         beta=1/kb_T;
%     end

%     %anneal schedule 3
%     if step <= (9*nsteps)/10
%         kb_T = kb_T + dT4;
%         beta = 1/kb_T;
%     else
%         kb_T = kb_T + dT5;
%         beta = 1/kb_T;
%     end
    
    %linear ramp
    kb_T=kb_T+delta_kb_T;
    beta=1/kb_T;
end
    
rejected_configs/step

figure(1);
plot(etot_sequence,'k');
ylabel('Potential Energy');
xlabel('Step');


figure(2);
plot(r_squared,'k');
xlabel('Step');
ylabel('<\Delta r>^{2}');

% figure(3);
% plot(kb_T,'k');
% xlabel('Step');
% ylabel('k_{b}T');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %write final position of atoms to file
% output_atoms_final = [atoms_label,atoms];
% file2 = 'atoms_final_2000MC.xyz';
% dlmwrite(file2,numatom,'%d')
% dlmwrite(file2,atomlabel,'delimiter','','roffset',1)
% dlmwrite(file2,output_atoms_final,'delimiter','\t','roffset',1,'-append')


