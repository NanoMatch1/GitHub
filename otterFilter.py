import matplotlib.pyplot as plt
import numpy as np
import os
import csv
import sys
sys.path.insert(0, 'C:/GitHub/Raman/Raman')
from data_processing.baseline import baseline_als
import random


filename = r'C:\Users\sjbro\Downloads\Ag Cubes Crystal Violet 10-9M 10mW  1.csv'

with open(filename) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    data = list(reader)

data = np.array(data).astype(float)

def run_fast(data, shape = (1024, 600)):
    WN = data[:1024, 0]
    data = np.reshape(data[:, 1], shape)


    return WN, data

def run_slow(data):
    for idx, wn in enumerate(data[:, 0]):
        data = np.reshape(data[:, 1], ())
        print(np.shape(data))
        print(np.shape(data)[0]/1024)


WN, data = run_fast(data)

# print(WN)

# for idx in range(len(data[0, :])):
#     if idx > 100:
#         break
#     else:
#         plt.plot(WN, data[:, idx], label = 'Frame {}'.format(idx))

lam = 1000
p = 0.001
frameDict = {str(frame):np.column_stack((WN, data[:, frame])) for frame in range(len(data[0, :]))}

print(frameDict)


# pause()
showGraph = False

if showGraph == True:
    randList = [int(random.randint(0, len(frameDict))) for x in list(range(4))]
    print('randList = ',randList)
    fig, ax = plt.subplots(2,2)
    plt.subplots_adjust(bottom=0.2)
    ax = ax.flatten()
    for idx, x in enumerate(randList):
        dataY = frameDict[str(x)]
        baseline = baseline_als(dataY, lam, p)

        ax[idx].set_title('frame {}'.format(x))
        ax[idx].plot(WN, dataY, label = 'raw')
        ax[idx].plot(WN, baseline, label = 'baseline')
        ax[idx].plot(WN, dataY-baseline, label = 'subrtacted')

    plt.legend()
    plt.show()

def normalise(dataY, range = (0, 700)):
    norm = (dataY-min(dataY[range[0]:range[1]]))/(max(dataY[range[0]:range[1]]-min(dataY[range[0]:range[1]])))
    return norm


def baseline_all():
    frameDictBaseline = {}
    for key, data in frameDict.items():
        baseline = baseline_als(data, lam, p)
        dataY = data - baseline
        # dataY = normalise(dataY)
        data = np.column_stack((WN, dataY))
        frameDictBaseline[key] = data

# for key, data in dataDict.items():
#     dataX = data[:, 0]
#     dataY = data[:, 1]
#
# for frame, data in frameDict.items():
data = frameDict['0']
deltaList = []
for idx, inten in enumerate(data[:700, 1]):
    try:
        intenL = data[idx-1, 1]
        deltaI = inten - intenL
        deltaList.append(deltaI)
    except:
        continue

def pause():
    input('Paused')

def moving_average(dataY, range = 5):
    avg = np.sum(dataY[:range])/range
    movAvg = [avg]*(range+1)
    for idx, inten in enumerate(dataY):
        if idx > range:
            avg = ((np.sum(dataY[idx-(range-1):idx]))+inten)/range
            movAvg.append(avg)

    print(len(movAvg))
    return movAvg



# print(deltaList)

# print(sfda)
# plt.hist(deltaList, 150)
# plt.show()
broadness = 5
testData = [random.random() for x in range(1024)]

count = 0
for idx, x in enumerate(testData):
    print(x)
    if count > broadness:
        if x >= 0.99:
            testData[idx] = x*broadness
            for a in range(1, broadness+1):
                try:
                    testData[idx-a] = x*(broadness-a)
                    testData[idx+a] = x*(broadness-a)
                except IndexError:
                    pass
            count = 0
    else:
        count += 1
        continue

# plt.plot(data[:, 0], testData)
# plt.show()

# conditional: if the magnitude of gradient of movAvg[idx-5:idx] is greater than some value, its a peak
# greate a noise filter that make a running total average that ignores regions of greater change that certain vaiue

# or simple - baseline agressively then filter on intensity above explicitly defined noise
lam = 100
p = 0.1
movAvg = moving_average(testData, range = 5)
baseline = baseline_als(movAvg, lam, p)
print(movAvg)
plt.scatter(data[:, 0], testData)
plt.plot(data[:, 0], baseline, c = 'purple')
plt.plot(data[:, 0], movAvg, c = 'red')
plt.show()








lam = 100
p = 0.1
movAvg = moving_average(data[:, 1])
baseline = baseline_als(movAvg, lam, p)
print(movAvg)
plt.scatter(data[:, 0], data[:, 1])
plt.plot(data[:, 0], baseline, c = 'purple')
plt.plot(data[:, 0], movAvg, c = 'red')
plt.show()

print('done')


# for idx in range(len(data[0, :])):
#     if idx > 10:
#         break
#     else:
#         plt.plot(WN, frameDict[str(idx)], label = 'frame {}'.format(idx))
#
# plt.legend()
# plt.show()
