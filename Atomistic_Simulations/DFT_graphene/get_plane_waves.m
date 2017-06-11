function [plane_waves,num_plane_waves]=get_plane_waves(b1,b2,b3,ecut);
%find the integral linear combinations of recip. lattice vecs with
%electron free particle energy less than ecut


max=ceil(sqrt(ecut)/(norm(b1)/sqrt(2)));
num_plane_waves=0;

for i=-max:max
for j=-max:max
for k=-max:max
    if (norm(i*b1+j*b2+k*b3)^2/2<ecut)
        num_plane_waves=num_plane_waves+1;
        %plane_waves(:,num_plane_waves)=[i,j,k];
        plane_waves(:,num_plane_waves)=i*b1+j*b2+k*b3;
    end
    end
end
end
end


       
        
    