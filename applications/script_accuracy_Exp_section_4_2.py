#------------------------------------------------------------------------------
# Conduct the experiment in Section 4.2
#------------------------------------------------------------------------------
import numpy as np
import scipy
import sys
from   scipy import linalg
import time
from numpy import random
import matplotlib.pylab as plt

sys.path.append('../../../Stiefel_log_general_metric/SciPy/')

import Stiefel_retractions as STR
import Stiefel_Aux as StAux
import Stiefel_Exp_Log as StEL

np.random.seed(6013294)
# Set dimensions
n = 1000
p = 400

Nt = 51
alpha  = -0.5

U0, U1, Xi = StEL.create_random_Stiefel_data(n, p, 0.5*np.pi, alpha)

mode = 1

Xi_pfi  = STR.Stiefel_PF_inv_ret(U0, U1)

# tangent for polar light retraction
Xi_pli  = STR.Stiefel_PL_inv_ret(U0, U1, mode)

I_unit = np.linspace(0.0, 1.0, Nt)
errors_geo_approx = np.zeros((Nt,2))

geo_t = np.zeros((Nt, n,p))

for k in range(Nt):
    tk      = I_unit[k]
    # geodesic at tk
    geo_t[k,:,:]  = StEL.Stiefel_Exp(U0, tk*Xi, alpha)
    # PF retraction at tk
    PF_tk   = STR.Stiefel_PF_ret(U0, tk*Xi_pfi)
    # PL retraction at tk
    PL_tk   = STR.Stiefel_PL_ret(U0, tk*Xi_pli, mode)

    error_PF= np.linalg.norm((geo_t[k,:,:]-PF_tk), 'fro')
    error_PL= np.linalg.norm((geo_t[k,:,:]-PL_tk), 'fro')
    errors_geo_approx[k,0] = error_PF
    errors_geo_approx[k,1] = error_PL

print('Max errors mode ', mode, ' are:')
print(np.max(errors_geo_approx[:,0]), ' (polar factor)')
print(np.max(errors_geo_approx[:,1]), ' (polar light)')

do_plot = True
if do_plot:
    plt.rcParams.update({'font.size': 40})

    line_err_PF, = plt.plot(I_unit, errors_geo_approx[:,0], 'r-', linewidth=3, label = 'errors PF')
    line_err_PL, = plt.plot(I_unit, errors_geo_approx[:,1], 'b-.', linewidth=3, label = 'errors PL')

    plt.legend()
    plt.xlabel('t')
    plt.ylabel('Errors')
    plt.show()


U0,U1,Xi = StEL.create_random_Stiefel_data(n,p,0.5*np.pi,alpha)

XiPF = STR.Stiefel_PF_inv_ret(U0,U1)
XiPL = STR.Stiefel_PL_inv_ret(U0,U1)


ts = np.linspace(0,1,Nt)

err = np.zeros((2,Nt))


for k in range(Nt):
    t = ts[k]
    Expt = StEL.Stiefel_Exp(U0,Xi*t,alpha)
    err[0,k] = np.linalg.norm(Expt - STR.Stiefel_PF_ret(U0,XiPF*t),'fro')
    err[1,k] = np.linalg.norm(Expt - STR.Stiefel_PL_ret(U0,XiPL*t),'fro')

print("Max error PF",np.max(err[0,:]))
print("Max error PL",np.max(err[1,:]))

# np.save('errs_n_'+str(n)+'_p_'+str(p),err)