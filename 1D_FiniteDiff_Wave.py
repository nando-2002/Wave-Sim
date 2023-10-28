import numpy as np 
import matplotlib.pyplot as plt

def visualize(xtitle, ytitle, var, ylimup, colour):
    plt.style.use("classic")
    plt.plot(np.linspace(0,xmax,nx), var, colour)   
    plt.ylim(-ylimup,ylimup) 
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.grid()
    plt.show()
    

nx = 1000
nt =1000
c = 3

pold = np.zeros(nx)
p = np.zeros(nx) 
pnew = np.zeros(nx) 

xmax = 10000
x = np.linspace(0, xmax, nx)
dx = xmax/(nx - 1)

dt = (dx/c)*0.5 #mutliply this by desired CFL number which is 1 by default
#dt = 0.025

#initial condition (gaussian function)

A = 1 #wave height
B = int(nx/2) #wave pos
C = 50 #wave width

pold[:] = A*np.exp(-(((((x[:])/dx) - B)**2)/(2*C**2)))
p[:] = pold[:]
#pnew[:] = pold[:]
#p[:] = A*np.exp(-(((((x[:])/dx) - B)**2)/(2*C**2)))
#p[1:nx-1] = pold[1:nx-1] - (0.5*c*(dt**2)/(dx**2))*(pold[2:nx] - 2*pold[1:nx-1] + pold[0:nx-2])

visualize("pos", "mag", pold, 5, "r-")
visualize("pos", "mag", p, 5, "r-")

m = (c*dt)/dx

for i in range(nt):
    '''
    for j in range(1, nx - 1):
        pnew[j] = (c*(dt**2)/(dx**2))*(p[j + 1] - 2*p[j] + p[j - 1]) + 2*p[j] - pold[j]
    '''
    pnew[1:nx - 1] = (c*(dt**2)/(dx**2))*(p[2:nx] - 2*p[1:nx - 1] + p[0:nx - 2]) + 2*p[1:nx - 1] - pold[1:nx - 1] 
    
    pold, p, pnew = p, pnew, pold
visualize("pos", "mag", pnew, 5, "b-")

    
    