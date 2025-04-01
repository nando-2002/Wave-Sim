import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import cm
#from numba import jit, njit, prange
from mpl_toolkits.mplot3d import Axes3D
import time

start = time.time()

nx = 350
ny = 350
nt = 250

L = 1 #metres
c = 2 #metres per second

x = np.linspace(0, L, nx)
y = np.linspace(0, L, ny)

dx = L/nx
dy = L/ny

dt = (dx/c)*0.6 #seconds

u_old = np.zeros([nx, ny])
u_now = np.zeros([nx, ny])
u_future = np.zeros([nx, ny])
d2ux = np.zeros([nx, ny])
d2uy = np.zeros([nx, ny])

solver = int(2) #select 2 for finite difference

#input initial conditions

A = 4 #wave height - kinda not really
B = int(4*nx/8) #wave pos
C = int(0.1*L/dx) #wave width - again not really but kinda

for xx in range(nx):
    for yy in range(ny):
        u_old[xx, yy] = A*np.exp(-((xx - B)**2 + (yy - B)**2)/(2*C**2))
u_now = u_old

seismo = np.zeros(nt)

#calculate spectral derivative
def der2(f):
    fhat = np.fft.fft(f)
    k = (2*np.pi/L)*np.arange(-nx/2, nx/2)
    k = np.fft.fftshift(k)
    dfhat = -fhat*k**2
    df = np.real(np.fft.ifft(dfhat))
    return df

#display seismogram
def display1d(xtitle, ytitle, var, ylimup, colour, n):
    plt.style.use("default")
    plt.plot(np.linspace(0,L,nt), var, colour)   
    plt.ylim(-ylimup,ylimup) 
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.grid('steps')  
    #plt.savefig(f'images/1Dimages/{n:3}.jpg', dpi = 200)
    plt.show()    

#display 2d visualization
def display(output):
    plt.style.use("default")
    plt.clf()
    plt.pcolormesh(x, y, output, shading='auto', cmap='coolwarm', vmax=0.6, vmin=-0.6)
    plt.colorbar()
    plt.ylim(0, L)
    plt.xlim(0, L)
    #plt.title(f"Time t = {t:.2f}")
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.pause(0.001)

#display 3d surface    
def otherdisplay(output, n):
    fig, ax = plt.subplots(subplot_kw = {"projection":"3d"})
    a = x
    b = y
    a, b = np.meshgrid(a, b)
    ax.axes.set_zlim3d(bottom=-6, top=6)
    surf = ax.plot_surface(a, b, output, cmap = cm.gnuplot, linewidth = 0, antialiased = False)
    #plt.savefig(f'images/2Dimages/{n:3}.jpg', dpi = 200)
    #plt.close()

#otherdisplay(u_old)

#spectral solution
if (solver == 1):
    for i in range(nt):
        for j in range(nx):
            d2ux[:,j] = der2(u_now[:,j])
        for jj in range(ny):
            d2uy[jj,:] = der2(u_now[jj,:])
            
        u_future = (2*u_now - u_old
                + c*(dt**2)*((d2ux + d2uy)))
        seismo[i] = u_now[int(0.8*nx),int(0.8*ny)]
        u_old = u_now
        u_now = u_future
        u_future = u_old
        #if (i%50 == 0):
            #otherdisplay(u_future, i)
        
#finite difference solution
if (solver == 2):
    for i in range(nt):
        u_future[1:nx-1, 1:ny-1] = (
                2*u_now[1:nx-1, 1:ny-1] - u_old[1:nx-1, 1:ny-1]
                + c*(dt**2)*(
                    (u_now[2:nx, 1:ny-1] + u_now[0:nx-2, 1:ny-1] - 2*u_now[1:nx-1, 1:ny-1])/(dx**2) +
                    (u_now[1:nx-1, 2:ny] + u_now[1:ny-1, 0:ny-2] - 2*u_now[1:nx-1, 1:ny-1])/(dy**2)
                    )
                )
        seismo[i] = u_now[int(0.8*nx),int(0.8*ny)]
        u_old = u_now
        u_now = u_future
        u_future = u_old
        #if (i%50 == 0):
            #otherdisplay(u_future, i)

       
end = time.time()
print("Time taken to execute: ", (end - start), "seconds")
otherdisplay(u_future,0)
#display1d('x distance', 'magnitude', seismo, 6, 'b-', 0)