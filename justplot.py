import sys
sys.path.insert(0, 'C:/GitHub/Raman/Raman')
# sys.path.insert(0, r'C:\Users\sjbrooke\github\Raman')
from Modular_Raman_Analyser import *
from Header_Finder import *
import matplotlib.pyplot as plt
import numpy as np

fileDir = r'C:\Users\sjbro\OneDrive - Massey University\Sam\PhD\Data\Raman\2021\3-13-21 Lines and maps\linescans\f14line4/'

peakDict = {'LA':(673,683), 'E2g':(745, 755)}
dataDict, headerDict = load_files(dir = fileDir, viewGraph = False)

dataLA = []
dataE2g = []

for file, data in dataDict.items():
    dataLA.append(data[678, 1])
    dataE2g.append(data[750, 1])

Xline = list(range(len(dataLA)))
plt.plot(Xline, dataLA, label = 'LA')
plt.plot(Xline, dataE2g, label = 'LA')
plt.show()
