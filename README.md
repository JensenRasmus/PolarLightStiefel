# newStiefelPolar

**Rasmus Jensen and Ralf Zimemrmann**

Source code for reproducing the experiments in Section 4 of "An new polar factor retraction on the Stiefel manifold with closed-form inverse".

For practical reasons, one might need to edit the files slightly to either generate data (True/False flags), as well as edit the dimensions, in order for the scripts to run. 

Several scripts in this repository is taken from a [repositotry](https://github.com/RalfZimmermannSDU/RiemannStiefelLog) belonging to the author RZ. There, a slightly different convention for the Riemannian metric is used ($\alpha$-metrics). Letting $\alpha=0$ yields the canonical metric, and $\alpha = -0.5$ yields the Euclidean metric. 

To use the Matlab scripts in the 'figures' folder, one has to use the package 'readNPY'. 
Place the [folder containing the git repository npy-matlab]{https://github.com/kwikteam/npy-matlab/tree/master} in the 'figures' folder, in order for the Matlab scripts to work. 