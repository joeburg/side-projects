function [H_pot] = hydrogen_atom_pot(plane_waves,num_plane_waves,cell_vol)
%compute the potential energy for a hydrogen atom
%V(G)=-(4*Pi*e^2)/(omega|G|^2)

H_pot=zeros(num_plane_waves,num_plane_waves);
for i=1:num_plane_waves
    for j=1:num_plane_waves
        if i ~= j
            G1=plane_waves(:,i);
            G2=plane_waves(:,j);
            H_pot(i,j)=-(4*pi)/(cell_vol*norm(G1-G2)^2);
        end
    end
end
end

