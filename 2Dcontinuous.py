import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
import matplotlib.patches as patches
import os
import json
from matplotlib.widgets import Slider, Button
import time
import shutil
import sys
import random
sys.path.insert(0, 'C:/GitHub/Raman/Raman')
from Modular_Raman_Analyser import *
from Header_Finder import *

def baseline_all(dataDict, lam = 1000, p = 1000, showGraph = True):
    from data_processing.baseline import baseline_als

    for file, data in dataDict.items():
        try:
            dataList.append((file,data))
        except NameError:
            dataList = [data]


    fig, ax = plt.subplots(2,2)
    plt.subplots_adjust(bottom=0.2)
    ax = ax.flatten()


    randList = [random.randint(0, len(dataDict)) for x in list(range(4))]
    if showGraph == True:
        for idx, x in enumerate(randList):
            file, data = dataList[x]
            dataX = data[:, 0]
            dataY = data[:, 1]


            baseline = baseline_als(dataY, lam, p)

            ax[idx].set_title(str(file))
            ax[idx].plot(dataX, dataY, label = 'raw')
            ax[idx].plot(dataX, baseline, label = 'baseline')
            ax[idx].plot(dataX, dataY-baseline, label = 'subrtacted')

        plt.legend()
        plt.show()
        pause('Continue to baseline all.')

    for file, data in dataDict.items():
        dataX = data[:, 0]
        dataY = data[:, 1]
        baseline = baseline_als(dataY, lam, p)
        dataYbase = dataY - baseline
        data = np.column_stack((dataX, dataYbase))

        try:
            dataDictBaselined[file] = data
        except NameError:
            dataDictBaselined = {file:data}

    plt.close()
    plt.cla()
    return dataDictBaselined

def make_scanList(dataDict):
    peakDict = {'LA':(673,683), 'E2g':(745, 755)}
    # dataDict, headerDict = load_files(dir = fileDir, viewGraph = False)


    scanDict = {}
    scanDictRunning = {}
    scanNameList = []
    scanGroup = -1
    runningDict = {}
    for file, data in dataDict.items():
        scanName = file[:file.index('#')]
        print(scanName)
        # if not scanName in scanNameList:
        #     scanNameList.append(scanName)
        scanIndex = file[file.index('#')+2:]
        scanIndex = scanIndex[:scanIndex.index('#')-1]
        print(scanIndex)
        if scanName == scanGroup:
            runningDict[scanIndex] = data
        else:
            if scanGroup != -1:
                scanDict[scanGroup] = runningDict
            scanGroup = scanName
            runningDict = {}
            runningDict[scanIndex] = data
            print(runningDict)
    scanDict[scanGroup] = runningDict
    return scanDict


def plot_lines(dataDir):
    peakDict = {'LA':(673,683), 'E2g':(745, 755)}
    # dataDict, headerDict = load_files(dir = dataDir, viewGraph = False)


    scanDict = {}
    scanDictRunning = {}
    scanNameList = []
    scanGroup = -1
    runningDict = {}
    for file, data in dataDict.items():
        scanName = file[:file.index('#')]
        print(scanName)
        # if not scanName in scanNameList:
        #     scanNameList.append(scanName)
        scanIndex = file[file.index('#')+2:]
        scanIndex = scanIndex[:scanIndex.index('#')-1]
        print(scanIndex)
        if scanName == scanGroup:
            runningDict[scanIndex] = data
        else:
            if scanGroup != -1:
                scanDict[scanGroup] = runningDict
            scanGroup = scanName
            runningDict = {}
            runningDict[scanIndex] = data
            print(runningDict)
    scanDict[scanGroup] = runningDict

        #
        # try:
        #     scanDict[str(scanName+scanIndex)] = data
        # except NameError:
        #     scanDict = {str(scanName)+str(scanIndex): data}
    maxDict = {}
    for key, item in scanDict.items():

        # print('filename, ',key, 'scan indexes', item)

        E2gList = []
        LAlist = []
        for scanIdx in list(range(len(item))):
            data = item[str(scanIdx)]
            dataX, dataY = (data[:, 0], data[:, 1])
            E2g = max(dataY[745:755])
            # LA = peakDict['LA']
            LA = max(dataY[673:683])
            E2gList.append(E2g)
            LAlist.append(LA)

        # for fileIndex, data in item.items():
        #     dataX = data[:, 0]
        #     dataY = data[:, 1]
        #     E2g = max(dataY[743:756]) # this works for pixels only - use find_nearest() for calibrated axes
        #     E2gList.append(E2g)
            # print('index:', fileIndex, 'data:', data)
            # if int(fileIndex) < 10:
            #     plt.plot(data[:, 0], data[:, 1], label = (str(key)+str(fileIndex)))
            #     count += 1
        plt.ion()

        plt.show()
        plt.plot(list(range(len(E2gList))), E2gList, label = key+'-E2g')
        plt.plot(list(range(len(LAlist))), LAlist, label = key+'-LA')
        E2gList = []
        # plt.show()
    plt.legend()


    plt.draw()
    plt.pause(0.001)

def open_csv(file, dir = 'data'):
    with open(r'{}\{}'.format(dir, file), 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        data = list(reader)
        return data


def move_files(file, dirInitial, dirFinal):
    make_dir(dirFinal)
    shutil.move('{}{}'.format(dirInitial, file),'{}{}'.format(dirFinal, file)) #

def simple_import_files(file, dataDir):
    data = open_csv(file, dataDir)
    data = np.array(data)
    try:
        data = np.array(data[1:, :]).astype('float')
    except ValueError:
        dataX = list(range(len(data[1:, 0])))
        data = np.column_stack((dataX, data[1:, 1])).astype('float')

    return data

def data_dictionary(dataDir):
    dataFiles = [file for file in os.listdir(dataDir) if file.endswith('.csv')]
    for file in dataFiles:
        data = simple_import_files(file, dataDir)

        try:
            dataDict[file] = data
        except NameError:
            dataDict = {file: data}

    return dataDict

def extract_basename(file):
    basename = file[:file.index('[')]
    lineIndex = file[file.index('[')+1:file.index(']')]
    print(lineIndex)

    return basename, lineIndex

def line_dictionary(dataDict, lineDict):
    for file, data in dataDict.items():
        basename, lineIndex = extract_basename(file)
        if basename in lineDict.keys():
            if not lineIndex in lineDict.keys().keys():
                lineDict[basename][lineIndex] = data
            else:
                pass
        else:
            lineDict[basename][lineIndex] = data

    return lineDict

def grab_files(exportDir, fileDir):
    files = []
    print('checking')

    files = [file for file in os.listdir(exportDir) if file.endswith('.csv')]

    for file in files:
        while True:
            try:
                move_files(file, exportDir, fileDir)
                print(file)
                break
            except:
                print("permission error")
                time.sleep(10)
                break

    time.sleep(5)
    return files

def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)





peakDict = {'LA':(673,683), 'E2g':(745, 755)}

        # dataX, dataY = (data[:, 0], data[:, 1])
exportDir = r'H:\PhD\Raman\2021\3-18-21 Maps and lines/'
fileDir = r"C:\Users\sjbro\OneDrive - Massey University\Sam\PhD\Data\Raman\2021\3-18-21 Maps and lines\f17 map pol"+'/'
dataDir = fileDir

make_dir(fileDir)
plotList = []
acquisitionTime = 10.1

# grab_files(exportDir, fileDir)
# pause('files moved')

dataDict = data_dictionary(dataDir)
dataDict = baseline_all(dataDict, lam = 1000, p = 0.001, showGraph = True)
scanDict = make_scanList(dataDict)
plot_lines(dataDict)
plt.show()
pause()

count = 0
while True:
    exportFiles = grab_files(exportDir, fileDir)
    if len(exportFiles) > 0:
        print('New files')
        plt.close()
        dataDict = data_dictionary(dataDir)
        # dataDict = baseline_all(dataDict, lam = 1000, p = 1000, showGraph = True)
        scanDict = make_scanList(dataDict)
        plot_lines(dataDir)
        plt.show()
    if len(exportFiles) == 0:
        count += 1
