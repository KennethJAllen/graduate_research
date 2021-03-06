import numpy as np
from numpy import linalg as LA
from matplotlib import pyplot as plt

def Alternating_Projection(M, Omega, r):
    #Alternating projection matrix completion algorithm based on work by Lai, Varghese
    #M is initial completion guess
    #Omega is mask
    #r is rank of completion

    N = 500 #number of itterations
    X = M.copy()

    for k in range(N):
        U, S, Vh = LA.svd(X) #singular value decompostion of X
        Sigma = np.zeros((m,n))
        np.fill_diagonal(Sigma,S) #diagonal matrix of singular values
        X = U[:,0:r] @ Sigma[0:r,0:r] @ Vh[0:r,:] #rank r projection
        X[Omega] = M[Omega] #known_entries #projection onto plane of completions
    return X #completion

def random_mask(m,n,k):
    #creates a random mxn mask with exactly k true entries
    perm = np.random.choice(m*n, k, replace=False)
    Omega_linear = np.zeros(m*n)
    Omega_linear[perm] = 1
    Omega = np.reshape(Omega_linear,(m,n))
    Omega = Omega==1 #turns Omega into a logical matrix
    return Omega

#example
m = 40
n = 30 #matrix size m x n
r = 5 #rank of completion
A = np.random.rand(m,r)
B = np.random.rand(r,n) #random factor matrices
M = A @ B #random rank r matrix

known_ratio = 0.75 #ratio of known to unknown entries
num_known = round(known_ratio*m*n) #number of known entries
Omega = random_mask(m,n,num_known) #random mask of unknown entries

M0 = M.copy()
M0[~Omega] = 0 #sets unknown entries equal to zero

X = Alternating_Projection(M0,Omega,r)
err = LA.norm(X-M,2)
print("The spectral norm error between the original and completion is",err)