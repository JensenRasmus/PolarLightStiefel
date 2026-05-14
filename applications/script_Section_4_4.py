"""
Script associated to Section 4.4

It can produce the data associated to
 - Figure 5

The script produces .npy files, which 
can be plotted using the Matlab routines 
which can found in the 'figures' folder. 
"""

import scipy.linalg as sc
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import sys

from matplotlib import cm
from matplotlib.colors import LightSource


sys.path.append('../resources/')
import snapshot_analytic_mat    as snam
import Stiefel_interp_funcs     as sifs
import Stiefel_Exp_Log          as EL
import Hermite_interp as HI
import simulate_fisher as simfish

r = 0.3
L = 30
T = 10 # end time
Nx = 100
Nt = 10000

rank = 6

print("Compute rank " + str(rank) + " POD bases of the Fisher KKP equation for varying r")

#rs = np.array([0.5,0.9])
rs = np.array([0.1,0.5,0.9])
#rs = np.array([0.1,0.3,0.5,0.7,0.9])

Us = np.zeros([len(rs),Nx,rank])
print("----------------------------------------------")
#rs = np.array([0.1,0.5,0.9])

for i in range(len(rs)):
    y = simfish.fisher_KKP(L,T,Nx,Nt,rs[i])

    U, S, VT = sc.svd(y,\
                        full_matrices=False,\
                        compute_uv=True,\
                        overwrite_a=True)
    
    # Truncate
    Us[i,:,:] = U[:,0:rank]

# Align the coordinates wrt. U0 = Us[0,:,:]
sign = False
if sign:
    ref_for_sign = 1
    U0 = np.copy(Us[ref_for_sign,:,:])
    for i in range(len(rs)):
        Coord = Us[i,:,:].T @ U0
        Csign = np.diag(np.sign(np.diag(Coord)))
        Us[i,:,:] = Us[i,:,:] @ Csign
        
# ref_for_sign = 1
# U0 = np.copy(Us[ref_for_sign,:,:])

# for i in range(len(rs)):
#     Coord = Us[i,:,:].T @ U0
#     Csign = np.diag(np.sign(np.diag(Coord)))
#     print(Csign)

# input("Press Enter to continue...")
    

Us_c = np.copy(Us)
for i in range(len(rs)):
    Us_c[i,:,:] = Us[i,:,:]#HST.apply_WYT(Us[i,:,:] ,W,Y)
    

Nd = 81
ran = np.linspace(rs[0],rs[-1],Nd)


di = np.zeros([Nd,1])
sigmap_s = np.zeros([3,Nd])
# Create reference data
create_ref_data = 1
if create_ref_data:
    Uref = np.zeros([Nd,Nx,rank])
    Uref_c = np.zeros([Nd,Nx,rank])

    for i in range(0,Nd):
        y = simfish.fisher_KKP(L,T,Nx,Nt,ran[i])

        U, S, VT = sc.svd(y,\
                            full_matrices=False,\
                            compute_uv=True,\
                            overwrite_a=True)
        
        # align signs 
        sigmap_s[:,i] = S[rank-2:rank+1]
        
        if sign:
            Coord = U[:,0:rank].T @ U0
            Csign = np.diag(np.sign(np.diag(Coord)))

            Uref[i,:,:] = U[:,0:rank] @ Csign;
            Uref_c[i,:,:] = Uref[i,:,:]#HST.apply_WYT(Uref[i,:,:] ,W,Y);
            print(np.diag(Csign))

        else:
            Uref[i,:,:] = U[:,0:rank] 
            Uref_c[i,:,:] = Uref[i,:,:]#HST.apply_WYT(Uref[i,:,:] ,W,Y);

        
        # Track Riemannian distance from U0
        # di[i] = EL.distStiefel(U0,Uref[i,:,:])
    np.save("Uref",Uref)
    np.save("Uref_c",Uref_c)
    # Simulate system and obtain the basis
else:
    Uref = np.load("Uref.npy")
    Uref_c = np.load("Uref_c.npy")

np.save("sigma_ps",sigmap_s)

plotSigma_p = False
if plotSigma_p:
    plt.rcParams.update({'font.size': 20})
    # for i in range(4):
    #     line_sigma  = plt.plot(ran, sigmap_s[i,:], linewidth=3, label = '$\sigma$' + str(i))
    line_sigma  = plt.plot(ran, sigmap_s[0,:], 'k--',linestyle =':', linewidth=3, label = '$\sigma_{p-1}$  ')
    line_sigma  = plt.plot(ran, sigmap_s[1,:], 'b-', linewidth=3, label = '$\sigma_{p}$')
    line_sigma  = plt.plot(ran, sigmap_s[2,:], 'r--.', linewidth=3, label = '$\sigma_{p+1}$')

    plt.legend()
    plt.xlabel('r')
    plt.ylabel('$\sigma$')
    plt.show()


Err = np.zeros([6,len(ran)])
alpha  = -0.5
retra = 3

comp_time = np.zeros([6,2])
for d in range(100):
    for r in range(1,7):
        retra = r
        t_start = time.time()
        Deltas = sifs.Stiefel_geodesic_interp_pre(Us,\
                                                    rs,\
                                                    alpha,\
                                                    retra)
        
        
        #     print("A norm" + str(np.linalg.norm(A)))
        #     print("B norm" + str(np.linalg.norm(Delta - U @ A)))
        # input("Press any key")
        comp_time[r-1,0] = comp_time[r-1,0] + (time.time()-t_start)

        t_start = time.time()
        for k in range(len(ran)):    
            rs_star = ran[k]
            U_star = sifs.Stiefel_geodesic_interp(Us,\
                                                    Deltas,\
                                                    rs,\
                                                    rs_star,\
                                                    alpha,
                                                    retra)
            
            Err[r-1,k] = np.linalg.norm( U_star - Uref[k,:,:],'fro') / np.linalg.norm(Uref[k,:,:],'fro')
        comp_time[r-1,1] = comp_time[r-1,1] + (time.time()-t_start)

        # print("For Deltas[1,:,:] obtained from retraction ",r)
        # Delta = Deltas[0,:,:]
        # U = Us[0,:,:]
        # A = U.T@Delta
        # B = Delta - U@A
        # print("Norm of A",str(np.linalg.norm(A)))
        # print("Norm of B",str(np.linalg.norm(B)))
        # input("PR")
tim = time.time()
U_star = sifs.Stiefel_geodesic_interp(Us,\
                                                    Deltas,\
                                                    rs,\
                                                    rs_star,\
                                                    alpha,
                                                    retra)

print("max errors:")

print("PW linear, retra1 (Riemann     ):", Err[0,:].max())
print("PW linear, retra2 (polar factor):", Err[1,:].max())
print("PW linear, retra3 (polar light ):", Err[2,:].max())  
print("PW linear, retra4 (QD )         :", Err[3,:].max())  
print("PW linear, retra4 (QR )         :", Err[4,:].max())  
print("PW linear, retra5 (Cayley )         :", Err[5,:].max())  


np.save('Errors',Err)

do_plot = True
if do_plot:
    plt.rcParams.update({'font.size': 30})
  
    line_RBF1,  = plt.plot(ran, Err[0,:], 'b',linestyle =':', linewidth=3, label = 'Errors Riemann')
    line_RBF2,  = plt.plot(ran, Err[1,:], 'r-', linewidth=3, label = 'Errors PF')
    line_RBF3,  = plt.plot(ran, Err[2,:], 'k--.', linewidth=3, label = 'Errors PL')
    line_RBF3,  = plt.plot(ran, Err[3,:], 'b--.', linewidth=3, label = 'Errors QG')
    line_RBF2,  = plt.plot(ran, Err[4,:], 'r--', linewidth=3, label = 'Errors QR')
    line_RBF2,  = plt.plot(ran, Err[4,:], 'b-', linewidth=3, label = 'Errors Cayley')

    #line_pts, = plt.plot(mu_samples, np.zeros((len(mu_samples),)),  'bo', linewidth=3, label = 'fk')
    plt.legend(loc = 2)
    plt.xlabel('r')
    plt.ylabel('Errors')
    plt.show()

