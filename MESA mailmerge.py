import sys
sys.path.insert(0, 'C:/GitHub/Raman/Raman')
from Modular_Raman_Analyser import *
from Header_Finder import *
import numpy as np

dataDir = r"C:\Users\sjbro\OneDrive - Massey University\Sam\PhD\MacDiarmid\MESA\Mailing Lists\For merge"

files = [file for file in os.listdir(dataDir) if file.endswith('.csv')]
# print(files)


data1 = open_csv(files[0], dataDir)
data1 = np.array(data1)
data2 = np.array(open_csv(files[1], dataDir))







mergeFields = ['PhD or MSc', 'Email Address', 'First Name', 'Last Name', 'Home Institution']




# print(data2[:, 1])

for idx, nameL in enumerate(data1[:, 1]):
    if not nameL in data2[:, 1:]:
        try:
            mergeData = np.vstack((data1[idx, :]))
        except:
            mergeData = np.array(data1[idx, :])



print(mergeData)
