"""
Script associated to Section 4.5

It can produce the data associated to
 - Figure 8

The script produces .npy files, which 
can be plotted using the Matlab routines 
which can found in the 'figures' folder. 
"""

import numpy as np
import sys
import scipy.linalg as sc
import math
import matplotlib.pyplot as plt
import time

sys.path.append('../resources/')

import Stiefel_interp_funcs     as sifs


# Load dataset 
sigmas = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])

D = np.loadtxt('../dataset/CallPrice_Vol=0.9.txt')
m,n = D.shape

Data = np.zeros((9,n,m))

k = 0
for sigma in sigmas:
    Data[k,:,:] = np.loadtxt('../dataset/CallPrice_Vol=' +str(sigma)+'.txt').T
    k += 1

# Interpolate in sigma = 0.1, 0.5 and 0.9 ( k = 0, 4, 8)
ss = np.array([0.1, 0.5, 0.9])

# Obtain Stiefel data from a truncated SVD. 
# We truncate at p = 5
p = 5

US = np.zeros((3,n,p))
VS = np.zeros((3,m,p))
SS = np.zeros((3,p))

ks = [0,4,8]
i = 0
for k in ks:
    U, S, VT = sc.svd(Data[k,:,:],\
                        full_matrices=False,\
                        compute_uv=True,\
                        overwrite_a=True)
    # So (U * S) @ VT = Data[k,:,:]
    #print(sc.norm((U*S)@VT -Data[k,:,:]))
    
    # Truncate and save
    US[i,:,:] = U[:,0:p]
    V = VT.T
    VS[i,:,:] = V[:,0:p]
    SS[i,:] = S[0:p]
    print(sc.norm((US[i,:,:] *SS[i,:])@VS[i,:,:].T -Data[k,:,:]))
    i += 1

# We must align the signs 
U0 = US[0,:,:]

for i in range(1,3):
    Coord = US[i,:,:].T @ U0
    Csign = np.diag(np.sign(np.diag(Coord)))
    US[i,:,:] = US[i,:,:] @ Csign

    VS[i,:,:] = VS[i,:,:] @ Csign


# We can now interpolate. Try sigma = 0.2
sigmastar = 0.2
alpha  = -0.5

retra = 3
Deltas_u = sifs.Stiefel_geodesic_interp_pre(US,\
                                            ss,\
                                            alpha,\
                                            retra)

Deltas_v = sifs.Stiefel_geodesic_interp_pre(VS,\
                                            ss,\
                                            alpha,\
                                            retra)


U_star = sifs.Stiefel_geodesic_interp(US,\
                                            Deltas_u,\
                                            ss,\
                                            sigmastar,\
                                            alpha,
                                            retra)

V_star = sifs.Stiefel_geodesic_interp(VS,\
                                            Deltas_v,\
                                            ss,\
                                            sigmastar,\
                                            alpha,
                                            retra)

# For SS we do linear interpolation
def pre_linear_int(Locs, samples):
    dims = Locs.shape
    Deltas = np.zeros((dims[0],dims[1]))

    for k in range(len(samples)-1):
        Delta = Locs[k+1,:] - Locs[k,:]

        Deltas[k,:] = Delta

    return Deltas

def linear_int(Locs,Deltas,samples, mu_star):
    aux = abs(samples - mu_star)
    index = np.argmin(aux)
    if (mu_star < samples[index]) or abs(mu_star - samples[-1])<1.0e-15:
        pos = index-1
    else:
        pos = index

    Delta = Deltas[pos,:]
    lin_factor = (mu_star - samples[pos])/(samples[pos+1] - samples[pos])
    Y_star = lin_factor*Delta + Locs[pos,:]
    return Y_star

Deltas_S = pre_linear_int(SS,ss)
SS_star = linear_int(SS,Deltas_S,ss,sigmastar)
#SS_star = SS[0,:] + (SS[1,:] - SS[0,:]) /(0.5 - 0.1) *(sigmastar - 0.1)

# Compute SVD
Y_interp = (U_star*SS_star) @ V_star.T


retractions = [1,2,3,4,5,6]
rel_approx_err = np.zeros((6,len(sigmas)))
for retra in retractions:
    print("----------------------------------")
    print("Interpolate using retraction nr. "+str(retra))
    # Compute tangent vectors
    Deltas_u = sifs.Stiefel_geodesic_interp_pre(US,\
                                            ss,\
                                            alpha,\
                                            retra)

    Deltas_v = sifs.Stiefel_geodesic_interp_pre(VS,\
                                                ss,\
                                                alpha,\
                                                retra)
    k = 0
    for sigmastar in sigmas:
        print(sigmastar)
        U_star = sifs.Stiefel_geodesic_interp(US,\
                                            Deltas_u,\
                                            ss,\
                                            sigmastar,\
                                            alpha,
                                            retra)

        V_star = sifs.Stiefel_geodesic_interp(VS,\
                                                Deltas_v,\
                                                ss,\
                                                sigmastar,\
                                                alpha,
                                                retra)
        
        SS_star = linear_int(SS,Deltas_S,ss,sigmastar)

        Y_interp = (U_star*SS_star) @ V_star.T

        rel_approx_err[retra-1,k] = sc.norm(Y_interp - Data[k,:,:])/sc.norm(Data[k,:,:])
        
        k += 1
        
    print("----------------------------------")

print(rel_approx_err)
#print(sc.norm(Y_interp - Data[1,:,:])/sc.norm(Data[1,:,:]))