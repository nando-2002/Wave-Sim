import numpy as np 
import matplotlib.pyplot as plt



def visualize(xtitle, ytitle, var, ylimup, colour, n):
    plt.style.use("dark_background")
    plt.plot(np.linspace(0,xmax,nx), var, colour)   
    plt.ylim(-ylimup,ylimup) 
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.grid('steps')  
    plt.savefig(f'images/1Dimages/{n:3}.jpg', dpi = 200)
    plt.show()
    

nx =1000
nt =2840
c = 2

pold = np.zeros(nx)
p = np.zeros(nx) 
pnew = np.zeros(nx) 

xmax = 1
x = np.linspace(0, xmax, nx)
dx = xmax/(nx - 1)

dt = (dx/c)*1 #mutliply this by desired CFL number which is 1 by default
#dt = 0.025

#initial condition (gaussian function)

A = 4 #wave height - kinda not really
B = int(nx/2) #wave pos
C = 25 #wave width - again not really but kinda

pold[:] = A*np.exp(-(((((x[:])/dx) - B)**2)/(2*C**2)))
#pold[int(3*nx/8):int(5*nx/8)] = 1
p = pold

#visualize("pos", "mag", pold, 5, "r-")
#visualize("pos", "mag", p, 5, "r-")


for i in range(nt):
    '''
    for j in range(1, nx - 1):
        pnew[j] = (c*(dt**2)/(dx**2))*(p[j + 1] - 2*p[j] + p[j - 1]) + 2*p[j] - pold[j]
    '''
    pnew[1:nx - 1] = (c*(dt**2)/(dx**2))*(
        p[2:nx] - 2*p[1:nx - 1] + p[0:nx - 2]
        ) + 2*p[1:nx - 1] - pold[1:nx - 1] 
    
    pold = p
    p = pnew
    pnew = pold
    if(i%10 == 0):
        visualize("position", "magnitude", p, 4.1, "c-", (i/100))