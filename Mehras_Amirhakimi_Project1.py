# initialization
import numpy as np
import scipy.sparse as sp
nx = eval(input('x,y grid number: '))
ny = nx
dx = 1/nx
dy = 1/ny
N = (nx+1)*(ny+1)
x = np.linspace(0, 1, nx+1)
y = np.linspace(0, 1, ny+1)

# constructing A and b (coefficient matrix and right hand side vector)
A = np.zeros([N,N])
b = np.zeros(N)
for i in range(N):
    if i==0:
        A[i,i]=-4
        A[i,i+1]=1
        A[i,i+nx+1]=1
        b[i]=-1
    elif i==nx:
        A[i,i]=-3
        A[i,i-1]=1
        A[i,2*i+1]=1
        b[i]=-1
    elif i==N-nx-1:
        A[i,i]=-4
        A[i,i-nx-1]=1
        A[i,i+1]=1
        b[i]=-1
    elif i==N-1:
        A[i,i]=-3
        A[i,i-1]=1
        A[i,i-nx-1]=1
        b[i]=-1
    elif i<nx+1:
        A[i,i]=-4
        A[i,i-1]=1
        A[i,i+1]=1
        A[i,i+nx+1]=1
        b[i]=-1
    elif i>N-nx-1:
        A[i,i]=-4
        A[i,i-1]=1
        A[i,i+1]=1
        A[i,i-nx-1]=1
        b[i]=-1
    elif i%(nx+1)==0:
        A[i,i]=-4
        A[i,i-nx-1]=1
        A[i,i+nx+1]=1
        A[i,i+1]=1
    elif (i+1)%(nx+1)==0:
        A[i,i]=-3
        A[i,i-1]=1
        A[i,i-nx-1]=1
        A[i,i+nx+1]=1
    else:
        A[i,i]=-4
        A[i,i-1]=1
        A[i,i+1]=1
        A[i,i-nx-1]=1
        A[i,i+nx+1]=1

Asp=sp.coo_matrix(A)

# Sparsity pattern for nx = 6
import matplotlib.pyplot as plt
print(plt.spy(Asp))

# GMRES (without preconditioning)
import scipy.sparse.linalg as spla
def counter(rk=None):
    counter.niter+=1
    print("# iter {:3d}, residual = {}".format(counter.niter,str(rk)))
x0=np.zeros(N)
counter.niter=0
T = spla.gmres(A,b,x0=x0,callback=counter)
print(T[0])

# Plotting 2D temperature field
T2 = T[0].reshape(ny+1,nx+1)
x,y = np.meshgrid(x,y)
plt.figure(figsize=(8,8))
plt.contourf(x,y,T2,10)
plt.set_cmap('jet')
plt.colorbar()
plt.ylabel('y')
plt.xlabel('x')
plt.show()