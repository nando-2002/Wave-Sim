import numpy as np 
import numexpr as ne
import matplotlib.pyplot as plt
#from matplotlib import cm

nx = 1000
ny = 1000
nt = 10000

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

#input initial conditionsz
u_old[int(3*nx/8):int(5*nx/8),int(3*ny/8):int(5*ny/8)] = 0.5
u_now = u_old

def display(output):
    plt.clf()
    plt.pcolormesh(x, y, output, shading='auto', cmap='viridis')
    plt.colorbar()
    plt.ylim(0, L)
    plt.xlim(0, L)
    #plt.title(f"Time t = {t:.2f}")
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.pause(0.001)

display(u_old)

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
    if (i%1000 == 0):
        #display(u_future)
        print(i)
