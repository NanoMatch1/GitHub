import math
import numpy as np
import matplotlib.pyplot as plt

def pause(text = 'Paused...'):
    input(text)

x1 = np.array(list(np.arange(0,100, 0.01))).astype(float)


sinx1 = [math.sin(val) for val in x1]


start = math.asin(1)
finish = math.asin(0)

# sinFat = [2*x for x in sinx1]
# sinFat.append(sinFat[-1])
plt.plot(x1, sinx1)
# plt.plot(x1, sinFat)
plt.xlim(start, start+4*math.pi)
plt.ylim(-2, 2)
plt.title('So potential. Much tiddies.')
plt.ylabel('Most Energies!')
plt.xlabel('Such space-time-continuum')
# plt.show()
plt.cla()



import numpy as np
from mpl_toolkits.mplot3d import Axes3D
# Axes3D import has side effects, it enables using projection='3d' in add_subplot
import matplotlib.pyplot as plt
import random

def fun(x):
    return x**2

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# x = y = np.arange(-3.0, 3.0, 0.05)
X, Y = np.meshgrid(x1[:10], x1[:10])
zs = np.array(sinx1[:100])
Z = zs.reshape(X.shape)
# Z = np.array(sinx1).astype(float)

ax.plot_surface(X, Y, Z)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
