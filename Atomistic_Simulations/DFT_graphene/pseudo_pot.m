function [H_pseudo] = pseudo_pot(plane_waves,num_plane_waves,Z,rcut)
%compute pseudopotential 

H_pseudo=zeros(num_plane_waves,num_plane_waves);
for i=1:num_plane_waves
    for j=1:num_plane_waves
        if i ~= j
            G1=plane_waves(:,i);
            G2=plane_waves(:,j);
            H_pseudo(i,j)=-(4*pi*Z*sin(norm(G1-G2)*rcut))/(norm(G1-G2)^2*norm(G1-G2)*rcut);
        end
    end
end
end

