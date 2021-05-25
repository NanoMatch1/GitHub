import numpy as np

dataX = list(range(-1000, 2000))

# wavenumber = [((-0.0006*float(pixel)**2)+(2.7848*pixel)-1098.4) for pixel in dataX]
wavenumber = [((3135.5*np.log(float(pixel+990)))-10022)-(10000000/785) for pixel in dataX]

print(wavenumber)
