%Joe Burg 
% Compute and plot atomic radial wavefunctions 
% This program calls atomic_eigenproblem_solver
%HW 6-1

clear;
npoints=1000;
deltar=0.08;
rcut=0;
Z=3;
ell=1;

% [eigenvecs,eigenvals]=atomic_eigenproblem_solver(Z,rcut,ell,npoints,deltar);
% r=[1:npoints]*deltar;
% 
% figure(1);
% plot(r,eigenvecs(:,1),'k');
% hold on
% plot(r,eigenvecs(:,2),'b');
% plot(r,eigenvecs(:,3),'r');
% xlabel('r (atomic units)')
% ylabel('\phi_{n,l}(r)')

% eigenvals(1,1)
% eigenvals(2,2)
% eigenvals(3,3)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% step=1;
% for rcut_index=1:16
%     rcut=(rcut_index-1)/5
%     rcutvec(:,step)=rcut;
%     [eigenvecs,eigenvals]=atomic_eigenproblem_solver(Z,rcut,ell,npoints,deltar);
%     eigenvals_rcut(1:5,rcut_index)=[eigenvals(1,1), eigenvals(2,2),eigenvals(3,3),eigenvals(4,4),eigenvals(5,5)];
%     step=step+1;
%     eigenvals(1,1)
% end
% figure(3);
% plot(rcutvec,eigenvals_rcut')
% ylabel('E(n) (Hartree)')
% xlabel('r_{c} (atomic units)')
% 
% figure(4);
% plot(r,eigenvecs(:,1),'k');
% hold on
% plot(r,eigenvecs(:,2),'b');
% plot(r,eigenvecs(:,3),'r');
% xlabel('r (atomic units)');
% ylabel('\phi_{n,l}(r)');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% %compare wave functions of full potential and pseuopotential
% %full potential
% rcut=0;
% [eigenvecsfull,eigenvalsfull]=atomic_eigenproblem_solver(Z,rcut,ell,npoints,deltar);
% r=[1:npoints]*deltar;
% 
% %pseuopotential
% rcut=2.0;
% [eigenvecsPS,eigenvalsPS]=atomic_eigenproblem_solver(Z,rcut,ell,npoints,deltar);
% 
% figure(5);
% plot(r,eigenvecsfull(:,2),'r');
% hold on
% plot(r,eigenvecsPS(:,1),'b');
% xlabel('r (atomic units)');
% ylabel('\phi_{n,l}(r)');
% xlim([0,10])
% title('r_{cutoff} = 2.6'); 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %compare 2p energy state of full potential and pseuopotential
% %full potential
% rcut=0;
% [eigenvecsfull,eigenvalsfull]=atomic_eigenproblem_solver(Z,rcut,ell,npoints,deltar);
% r=[1:npoints]*deltar;
% 
% %pseuopotential
% rcut=0.26;
% [eigenvecsPS,eigenvalsPS]=atomic_eigenproblem_solver(Z,rcut,ell,npoints,deltar);
% 
% (eigenvalsfull(1,1)-eigenvalsPS(1,1))*27.2
%  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %plot reciprocal-space form of the pseudopotential and the bare Coulomb
% %potential
% 
% rcut=2.0;
% index=1;
% for i=0:0.01:20
%     Vrs(:,index)=-4*pi*Z*sin(i*rcut)/(rcut*i^3);
%     Vcol(:,index)=-Z/i;
%     index=index+1;
% end
% steps=[0:size(Vrs,2)-1];
% 
% figure(6);
% plot(steps,Vrs,'b');
% hold on
% plot(steps,Vcol,'r');
% ylim([-6,3]);
% xlabel('r (a.u.)  &  |G|');
% ylabel('V(r)  &  V(G)');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%band structure of bare Coulomb potential and pseudopotential

ecut=40.0;
bcc_lat_const=6.60;
num_kvecs=10;
%Define lattice vectors 
a1=[-0.5,0.5,0.5]*bcc_lat_const;
a2=[0.5,-0.5,0.5]*bcc_lat_const;
a3=[0.5,0.5,-0.5]*bcc_lat_const;

%Define reciprocal lattcie vectors
vol=dot(a1,cross(a2,a3));
b1=2*pi*cross(a2,a3)/vol;
b2=2*pi*cross(a3,a1)/vol;
b3=2*pi*cross(a1,a2)/vol;

[plane_waves,num_plane_waves]=get_plane_waves(b1,b2,b3,ecut);
num_plane_waves

%define k-points where bands will be computed
%from gamma to L for bcc crystal
for i=0:(num_kvecs-1)
    k_vecs(:,i+1)=i/(num_kvecs-1)/2*b1+i/(num_kvecs-1)/2*b2+i/(num_kvecs-1)/2*b3;
end

%form the potential part of the Hamiltonian
% %bare coulomb potential
% cell_vol = bcc_lat_const^3;
% H_pot=coulomb_pot(plane_waves,num_plane_waves,cell_vol);

% %pseudopotential
% rcut=2;
% H_pot=pseudo_pot(plane_waves,num_plane_waves,Z,rcut);

%no PE
H_pot=zeros(num_plane_waves,num_plane_waves); %free electron case


H_kinetic = zeros(num_plane_waves,num_plane_waves);
%loop over k vecs along gamma to L
for k=1:num_kvecs
    for i=1:num_plane_waves
        %form the kinetic part of the Hamiltonian here
        H_kinetic(i,i)=0.5*norm(k_vecs(:,k)-plane_waves(:,i))^2;
    end
    H = H_kinetic + H_pot;
    %compute eigenvalues
    eigenvalues(k,:)=sort(eig(H));
    %eigenvalues(k,:)=sort(eigs(H-eye(size(H))*10000))+10000; %this may run faster for large matricies
    k
end
figure(1);
plot(eigenvalues);
ylim([0,2])
xlabel('k');
ylabel('Band Energy');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%pseuopotential
% rcutoff=2;
% for i=0:r(npoints)-1
%     if i<rcutoff
%         Vps(:,i+1)=-Z/rcutoff;
%     else
%         Vps(:,i+1)=-Z/i;
%     end
% end
% steps=[0:size(Vps,2)-1];
% 
% figure(5);
% plot(r,eigenvecs(:,2),'b');
% hold on
% plot(steps,Vps,'g');
% xlim([0,10]);
% xlabel('r (atomic units)');
% ylabel('\phi_{n,l}(r) ; V^{ps}(r)');
% title('r_{cutoff} = 2'; 



