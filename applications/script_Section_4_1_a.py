"""
Script associated to Section 4.1 

It can produce the data associated to
 - Table 1

"""
#------------------------------------------------------------------------------
# Compare the costs of a foward + backward step.
# 
# We consider
# Polar factor retraction 
# Polar light retraction w. and wout. Cayley 
# Quasi geodesic Grassmann-like
# QR 
# 
# 
#------------------------------------------------------------------------------

import numpy as np
import scipy 
import sys
from   scipy import linalg
import time 
from numpy import random
import matplotlib.pylab as plt

sys.path.append('../resources/')

import Stiefel_retractions as STR
import Stiefel_Aux as StAux

# Tining of going back -> forward. 
def timings(U0,Xis):
    #N = Xis.shape[0]
    N = 10
    Ts = np.zeros((8,1))
    Qual = np.zeros((8,1))


    # PF
    
    for i in range(N):
        U1 = STR.Stiefel_PF_ret(U0,Xis[i,:,:])
        #print(np.linalg.norm(U1.T@U1 - np.eye(p)))
    
        t0 = time.time()
        Xiret = STR.Stiefel_PF_inv_ret(U0,U1)
        t1 = time.time()
        #print(np.linalg.norm(Xis[i,:,:] -STR.Stiefel_PF_inv_ret(U0,U1) ))
        Ts[0] = Ts[0] + (t1-t0)
        Qual[0] = Qual[0] + np.linalg.norm(Xiret -  Xis[i,:,:],'fro')

    print("*******************************")
    print("** Polar fractor retraction ***")
    print("*******************************")
    print("Avg. time:    ", str(Ts[0,0]/N))
    print("Avg. quality: ", str(Qual[0,0]/N))
    print("*******************************")

    # PL
    for i in range(N):
        U1 = STR.Stiefel_PL_ret(U0,Xis[i,:,:])
        #print(np.linalg.norm(U1.T@U1 - np.eye(p)))
    
        t0 = time.time()
        Xiret = STR.Stiefel_PL_inv_ret(U0,U1,1) # 1 = uses logm
        t1 = time.time()
        #print(np.linalg.norm(Xis[i,:,:] -STR.Stiefel_PF_inv_ret(U0,U1) ))
        Ts[1] = Ts[1] + (t1-t0)
        Qual[1] = Qual[1] + np.linalg.norm(Xiret -  Xis[i,:,:],'fro')

    print("*******************************")
    print("** Polar Light retraction ***")
    print("*******************************")
    print("Avg. time:    ", str(Ts[1,0]/N))
    print("Avg. quality: ", str(Qual[1,0]/N))
    print("*******************************")

    # PL-Cayley
    for i in range(N):
        U1 = STR.Stiefel_PL_ret(U0,Xis[i,:,:],mode = 2) # Cayley
        #print(np.linalg.norm(U1.T@U1 - np.eye(p)))
    
        t0 = time.time()
        Xiret = STR.Stiefel_PL_inv_ret(U0,U1,2) # Cayley
        t1 = time.time()
        #print(np.linalg.norm(Xis[i,:,:] -STR.Stiefel_PF_inv_ret(U0,U1) ))
        Ts[2] = Ts[2] + (t1-t0)
        Qual[2] = Qual[2] + np.linalg.norm(Xiret -  Xis[i,:,:],'fro')

    print("**************************************")
    print("** Polar Light w.Cayley retraction ***")
    print("**************************************")
    print("Avg. time:    ", str(Ts[2,0]/N))
    print("Avg. quality: ", str(Qual[2,0]/N))
    print("**************************************")


    # QD. Grassmann--like
    for i in range(N):
        U1 = STR.Stiefel_Quasi_geod(U0,Xis[i,:,:]) # Grassmann-like
        #print(np.linalg.norm(U1.T@U1 - np.eye(p)))
    
        t0 = time.time()
        Xiret = STR.Stiefel_inv_Quasi_geod(U0,U1,1) # Grassmann-like
        t1 = time.time()
        #print(np.linalg.norm(Xis[i,:,:] -STR.Stiefel_PF_inv_ret(U0,U1) ))
        Ts[3] = Ts[3] + (t1-t0)
        Qual[3] = Qual[3] + np.linalg.norm(Xiret -  Xis[i,:,:],'fro')

    print("**************************************")
    print("** Quasi-Geodesics: Grassmann-like ***")
    print("**************************************")
    print("Avg. time:    ", str(Ts[3,0]/N))
    print("Avg. quality: ", str(Qual[3,0]/N))
    print("**************************************")

    # QR
    for i in range(N):
        U1,R = STR.Stiefel_QR_ret(U0,Xis[i,:,:]) 
        #print(np.linalg.norm(U1.T@U1 - np.eye(p)))
    
        t0 = time.time()
        Xiret = STR.Stiefel_QR_inv_ref(U0,U1) 
        t1 = time.time()
        #print(np.linalg.norm(Xis[i,:,:] -STR.Stiefel_PF_inv_ret(U0,U1) ))
        Ts[4] = Ts[4] + (t1-t0)
        Qual[4] = Qual[4] + np.linalg.norm(Xiret -  Xis[i,:,:],'fro')

    print("**************************************")
    print("** QR retraction ***")
    print("**************************************")
    print("Avg. time:    ", str(Ts[4,0]/N))
    print("Avg. quality: ", str(Qual[4,0]/N))
    print("**************************************")

    # Cayley retraction
    for i in range(N):
        U1 = STR.Stiefel_Cayley(U0,Xis[i,:,:]) 
        #print(np.linalg.norm(U1.T@U1 - np.eye(p)))
    
        t0 = time.time()
        Xiret = STR.Stiefel_inv_Cayley(U0,U1) 
        t1 = time.time()
        #print(np.linalg.norm(Xis[i,:,:] -STR.Stiefel_PF_inv_ret(U0,U1) ))
        Ts[5] = Ts[5] + (t1-t0)
        Qual[5] = Qual[5] + np.linalg.norm(Xiret -  Xis[i,:,:],'fro')

    print("**************************************")
    print("** Cayley retraction ***")
    print("**************************************")
    print("Avg. time:    ", str(Ts[5,0]/N))
    print("Avg. quality: ", str(Qual[5,0]/N))
    print("**************************************")

    

    Ts = Ts / N
    Qual = Qual / N

    return Ts, Qual


# Dimensions 
n = 1000
p = 400
np.random.seed(345345)

A = np.random.rand(n,p)
U0,R0 = np.linalg.qr(A,mode='reduced')

N = 100 # Number of experiments
Create_Us = True
if Create_Us:
    Xis = np.zeros((N,n,p))
    for k in range(N):
        # Generate a tangent vector at U0
        A = np.random.rand(p,p) 
        A = 0.5 * (A.T - A) # Now A is p x p skew
        A = A / np.linalg.norm(A,'fro')

        B = np.random.rand(n,p) 
        B = B / np.linalg.norm(B,'fro')
        #B = np.zeros([n,p])

        Xi = U0 @ A + (B - U0 @ (U0.T @ B))

        # Q,R = np.linalg.qr(Xi - U0 @ (U0.T @ Xi),mode = 'reduced')
        # ART = np.concatenate((A,-R.T),axis =1)
        # RZ  = np.concatenate((R, np.zeros([p,p])),axis=1)
        # S = np.concatenate((ART, RZ),axis=0)
        # UQ = np.concatenate([U0, Q],axis=1)

        # U1 = UQ @ scipy.linalg.expm(S)
        Xis[k,:,:] = Xi
        print(k)
    np.save("Xis_n_p_"+str(n)+"_"+str(p),Xis)

else:
    Xis = np.load("Xis_n_p_"+str(n)+"_"+str(p)+".npy")

#Xi = Xis[0,:,:]
#print(U0.T @ Xi + Xi.T @ U0)
Ts, Qs = timings(U0,Xis)

print("************")
print(Ts)
print("************")
print(Qs)