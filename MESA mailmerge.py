import sys
sys.path.insert(0, 'C:/GitHub/Raman/Raman')
from Modular_Raman_Analyser import *
from Header_Finder import *
import numpy as np

dataDir = r"C:\Users\sjbro\OneDrive - Massey University\Sam\PhD\MacDiarmid\MESA\Mailing Lists\For merge"

files = [file for file in os.listdir(dataDir) if file.endswith('.csv')]
# print(files)


dataAnewList = np.array(open_csv(files[0], dataDir))
dataMCexportFeb = np.array(open_csv(files[1], dataDir))
dataMI = np.array(open_csv(files[2], dataDir))
dataVUW = np.array(open_csv(files[3], dataDir))

for idx, file in enumerate(files):
    print("File"+str(idx)+': '+str(file))



mergeFields = ['PhD or MSc', 'Email Address', 'First Name', 'Last Name', 'Home Institution']

# print(p)


# print(data2[:, 1])

def case_normalise(toList, fromList, column = 3):
    toList = [str(x) for x in toList[:, column]]
    fromList = [str(x) for x in fromList[:, column]]



    toColLower = []
    fromColLower = []
    # for x in toList:
    #     toColLower.append(x.strip().lower())
    toColLower = [x.strip().lower() for x in toList]
    # for y in fromList:
    #     fromColLower.append(y.strip().lower())
    fromColLower = [x.strip().lower() for x in fromList]

    # toColLower = [x.lower() for x in toList]
    # fromColLower = [x.lower() for x in fromList]


    return toColLower, fromColLower


def merge_data(toList, fromList, column = 3):


    toColLower, fromColLower = case_normalise(toList, fromList, column)

    for idx, name in enumerate(fromColLower):
        print([name], ';', str(fromList[idx, column]))
        if str(fromList[idx, column]).strip().lower() != name:
            print('sorting error')
            print(p)
        if not name in toColLower:
            try:
                mergeData = np.vstack((mergeData, fromList[idx, :]))
            except:
                mergeData = np.array(fromList[idx, :])
    try:
        print(mergeData)
        return mergeData
    except:
        return []

def append_names(toList, mergeData):
    toList = np.array(toList)
    newList = np.vstack((toList, mergeData))
    np.savetxt('{}/AnewList.csv'.format(dataDir), newList, delimiter = ',', fmt = '%s')





mergeData = merge_data(dataAnewList, dataVUW, 1)
if len(mergeData) == 0:
    print('-'*80,'\n')
    print("No new entries")

# append_names(dataAnewList, mergeData)
