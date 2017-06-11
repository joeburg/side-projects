function [eigenvecs,eigenvals]=atomic_eigenproblem_solver(Z,rcut,ell,npoints,deltar)
% computes the atomic eigenvalues and eigenvectors in the radial coordinate
% eigenvectors are the values of r*phi(r), where phi(r) is the radial
% wavefunction.  No electron-electron interactions.
% Evan Reed
% March 3, 2013


for m=1:npoints
    r=m*deltar;
    if (r>=rcut)
        H(m,m)=1/deltar^2-Z/r+ell*(ell+1)/2/r^2;
    else
        H(m,m)=1/deltar^2-Z/rcut+ell*(ell+1)/2/r^2;
    end
    if (m<npoints)
        H(m,m+1)=-0.5/deltar^2;
    end
    if (m>1)
        H(m,m-1)=-0.5/deltar^2;
    end
    
end

[eigenvecs,eigenvals]=eig(H);

        