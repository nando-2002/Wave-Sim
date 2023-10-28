import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import cm

nx = 1000
ny = 1000
nt = 9000

L = 1 #metres
c = 2 #metres per second

x = np.linspace(0, L, nx)
y = np.linspace(0, L, ny)

dx = L/nx
dy = L/ny

dt = (dx/c)*0.5 #seconds

u_old = np.zeros([nx, ny])
u_now = np.zeros([nx, ny])
u_future = np.zeros([nx, ny])

#input initial conditions
A = 4 #wave height - kinda not really
B = int(1*nx/8) #wave pos
C = 25 #wave width - again not really but kinda

for xx in range(nx):
    for yy in range(ny):
        u_old[xx, yy] = A*np.exp(-((xx - B)**2 + (yy - B)**2)/(2*C**2))
u_now = u_old

def display(output):
    plt.clf()
    plt.pcolormesh(x, y, output, shading='auto', cmap='viridis', vmax=4.2, vmin=-4.2)
    plt.colorbar()
    plt.ylim(0, L)
    plt.xlim(0, L)
    #plt.title(f"Time t = {t:.2f}")
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.pause(0.001)
    
def otherdisplay(output):
    fig, ax = plt.subplots(subplot_kw = {"projection":"3d"})
    a = x
    b = y
    a, b = np.meshgrid(a, b)
    surf = ax.plot_surface(a, b, output, cmap = cm.viridis, linewidth = 0, antialiased = False)

#otherdisplay(u_old)

for i in range(nt):
    u_future[1:nx-1, 1:ny-1] = (
            2*u_now[1:nx-1, 1:ny-1] - u_old[1:nx-1, 1:ny-1]
            + c*(dt**2)*(
                (u_now[2:nx, 1:ny-1] + u_now[0:nx-2, 1:ny-1] - 2*u_now[1:nx-1, 1:ny-1])/(dx**2) +
                (u_now[1:nx-1, 2:ny] + u_now[1:ny-1, 0:ny-2] - 2*u_now[1:nx-1, 1:ny-1])/(dy**2)
                )
            )
    u_old = u_now
    u_now = u_future
    u_future = u_old
    #if (i%1000 == 0):
       
otherdisplay(u_future)

