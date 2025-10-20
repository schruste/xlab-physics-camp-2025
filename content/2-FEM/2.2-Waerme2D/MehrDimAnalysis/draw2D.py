import matplotlib.pyplot as plt
from random import random
from math import *



from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
#from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from math import pi

def draw2D(px=0,py=0):
    #fig = plt.figure()
    #ax = fig.gca(projection='3d')

    #ax = fig.add_subplot(1, 2, 1, projection='3d')
    #ax = plt.subplot2grid((2, 2), (0, 0), rowspan=2, projection='3d')
    #ax2 = plt.subplot2grid((2, 2), (0, 1))
    #ax3 = plt.subplot2grid((2, 2), (1, 1))

    plt.figure(figsize=(10, 5))
    ax = plt.subplot2grid((4, 4), (0, 0), rowspan=4, colspan=2, projection='3d')
    ax2 = plt.subplot2grid((4, 4), (0, 2), rowspan=2, colspan=2)
    ax3 = plt.subplot2grid((4, 4), (2, 2), rowspan=2, colspan=2)
    
    # plt.figure(figsize=(8, 6))
    #plt.plot(x1, y1, 'o-')
    #plt.title('A tale of 2 subplots')
    #plt.ylabel('Damped oscillation')

    #plt.subplot(2, 1, 2)
    #plt.plot(x2, y2, '.-')
    #plt.xlabel('time (s)')
    #plt.ylabel('Undamped')

    #plt.show()    
    
    #ax = plt.gca(projection='3d')

    # Make data.
    X1D = np.arange(-1, 1.01, 0.02)
    Y1D = np.arange(-1, 1.01, 0.02)
    X, Y = np.meshgrid(X1D, Y1D)

    def f(x,y):
        return np.cos(pi*(x+y)) - y**2 +  0.8 * x

    def dfdx(x,y):
        return -pi*np.sin(pi*(x+y)) + 0.8
    def dfdy(x,y):
        return -pi*np.sin(pi*(x+y)) - 2*y
    def df(x,y):
        return [dfdx(x,y,z),dfdy(x,y,z)]


    #def f(x,y):
    #    return x

    #def dfdx(x,y):
    #    return 1
    #def dfdy(x,y):
    #    return 0
    def df(x,y):
        return [dfdx(x,y),dfdy(x,y)]


    Z = f(X,Y)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.jet,linewidth=0, antialiased=False)

    h=0.1
    XI = np.arange(-h, 1.01*h, h)
    #print(XI)
    #px = 0.2
    #py = 0.3

    ax.plot([px],[py],[f(px,py)], "X")

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('f(x,y)')    
    
    norm = sqrt(dfdx(px,py)**2 + dfdy(px,py)**2)

    Xs = px + dfdx(px,py)/norm * XI
    Ys = py + dfdy(px,py)/norm * XI
    print("f(x,y) = ", f(px,py), "gradient: ", df(px,py))

    Zs = [f(px,py) + dfdx(px,py) * (x-px) + dfdy(px,py) * (y-py) for x,y in zip(Xs,Ys)]

    ax.plot(Xs,Ys,Zs)

    #X1 = 

    # Customize the z axis.
    #ax.set_zlim(-1.01, 1.01)
    #ax.zaxis.set_major_locator(LinearLocator(10))
    #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    #fig.colorbar(surf, shrink=0.5, aspect=5)
    
    #ax = fig.add_subplot(1, 2, 2)
    #ax = plt.subplot2grid((2, 2), (0, 1), rowspan=1)
    # plt.figure(figsize=(8, 3))

    ZX = [f(x,py) for x in X1D]
    ax2.plot(X1D,ZX)
    ax2.plot([px],[f(px,py)],"x")
    ax2.set_title(r'$g(x)=f(x,y^*)$')    
    
    ZY = [f(px,y) for y in Y1D]
    ax3.plot(Y1D,ZY)
    ax3.plot([py],[f(px,py)],"x")
    ax3.set_title(r'$h(y)=f(x^*,y)$')
    
    # plt.figure(figsize=(15, 6))
    plt.tight_layout()
    plt.show()
