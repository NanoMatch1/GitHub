%matplotlib
import matplotlib.pyplot as plt

fig, ax = plt.subpolots()
ln, = ax.plot(range(5))
ln.set_color('orange')

plt.ion()
