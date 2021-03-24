import matplotlib.pyplot as plt
import sys
import os
import numpy as np
import csv
import fnmatch
import shutil
import random
import math
sys.path.insert(0, r'C:\Users\sjbro\github\Raman\SimpleRaman package/')
from data_processing.baseline import baseline_als


def pause(text = 'Press Enter to continue...'):
    input(text)

def open_csv(file, dir = 'data'):
    with open(r'{}\{}'.format(dir, file), 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        data = list(reader)
        return data



def parse_header_simple(data, searchLen = 5): # need to turn into an object with classes
    try:
        data = np.array(data)
    except:
        print('data shape is non standard. Header not removed. Please pre-format data.')
        return
    shape = np.shape(data)


    # def get_data_index(data, searchLen):
    searchList = []
    NAcol = None
    # shape = np.shape(data)

    for row in list(range(searchLen)):
        for col in list(range(shape[1])):
            if data[row, col] == 'N/A':
                NAcol = True
                dataIdx = 1
            hasString = None
            hasNumber = None
            for char in data[row, col]:
                # print('CHAR = ', char)
                if char.isalpha() == True:
                    hasString = True
                    # print('alphabetical')
                if char.isdecimal() == True:
                    hasNumber = True
                    # print('number')
                # pause(/)

            if hasString == True and hasNumber == True:
                searchList.append('mixed')
            if hasString == True and hasNumber == None:
                searchList.append('alphabetical')
            if hasString == None and hasNumber == True:
                searchList.append('numerical')

    while NAcol == None:
        try:
            searchList = np.reshape(searchList, (searchLen, shape[1]))
            for x in list(range(searchLen)):
                if searchList[x, 0] == 'numerical' and searchList[x, 1] == 'numerical':
                    dataIdx = x
            else:
                dataIdx = False
        except:
            print('reshape failed')
            dataIdx = 0
        break



    try:
        data = np.array(data)
    except:
        print("Array failed - check data structure")
        return

    data = data[dataIdx:, :]
    if NAcol == True:
        data = np.column_stack((list(range(len(data[:, 1]))), data[:, 1]))
    header = data[:dataIdx, :]
    return data, header

def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def move_file(file, dirInitial, dirFinal):
    make_dir(dirFinal)
    shutil.move('{}{}'.format(dirInitial, file),'{}{}'.format(dirFinal, file)) #

def simple_load_files(fileDir, searchLen = 5):

    files = [file for file in os.listdir(fileDir) if file.endswith('.csv')]
    BG = None

    for file in files:
        data = open_csv(file, fileDir)

        data, header = parse_header_simple(data, searchLen)
        data = np.array(data).astype('float')

        if 'BG' in file: # edit later to search for BG folder - write function to check
            # os.chdir(fileDir)
            # move_file(file, fileDir, os.getcwd()+'/BG/')
            BG = np.array(data).astype('float')
            continue


        try:
            dataDict[file] = data
        except NameError:
            dataDict = {file:data}

        try:
            headerDict[file] = header
        except NameError:
            headerDict = {file:header}

    return dataDict, headerDict, BG



# class LineBuilder:
#     def __init__(self, line):
#         self.line = line
#         self.xs = list(line.get_xdata())
#         self.ys = list(line.get_ydata())
#         self.cid = line.figure.canvas.mpl_connect('button_press_event', self) # function could also call 'LineBuilder(line)' again to remake, but 'self' reuses current object and means redrawing the fig is cleaner than making a new one
#
#     def __call__(self, event): # function to run when object is recalled, i.e. LineBuilder(line) or new obj, or self
#         print('click', event)
#         if event.inaxes!=self.line.axes: return # in mpl_connect(), if a click is in the axes, event.inaxes is set to the actual plot object axes, therefore this will return if a click is out of bounds
#         self.xs.append(event.xdata)
#         self.ys.append(event.ydata)
#         self.line.set_data(self.xs, self.ys)
#         self.line.figure.canvas.draw()

class DataSet:

    processDict = {}

    def __init__(self, dataDir):
        self.rawData, self.header, self.BG = simple_load_files(dataDir)
        self.dataDir = dataDir
        self.currentData = self.rawData

    def check_BG(self, dataDir): # edit later to search for BG folder - write function to check
        pass

    def subtract_BG(self, normaliseRange = None, baseline = False):
        if self.BG is None:
            print('No backgound file found.')
            return
        BGx = self.BG[:, 0]
        BGy = self.BG[:, 1]

        if baseline == True:
            self.currentData = self.baseline_all()

        for file, data in self.currentData.items():
            dataX = data[:, 0]
            dataY = data[:, 1]



            if normaliseRange:
                BGy = BGy-min(BGy[normaliseRange[0]:normaliseRange[1]])
                BGy = BGy/max(BGy[normaliseRange[2]:normaliseRange[3]])
                dataY = dataY-min(dataY[normaliseRange[0]:normaliseRange[1]])
                dataY = dataY/max(dataY[normaliseRange[2]:normaliseRange[3]])



            dataYsub = dataY - BGy

            try:
                dataBGsub[file] = np.column_stack((dataX, dataYsub))
            except NameError:
                dataBGsub = {file: np.column_stack((dataX, dataYsub))}

        self.processDict['BGsub'] = dataBGsub
        self.BGsub = dataBGsub
        self.currentData = dataBGsub

        return dataBGsub

        # if normaliseRange:

    def baseline_all(self, lam = 10000, p = 0.001, showGraph = True):
        from data_processing.baseline import baseline_als

        # baseline the BG file
        BGy = self.BG[:, 1]
        baseline = baseline_als(BGy, lam, p)
        BGyBase = BGy - baseline
        BGdata = np.column_stack((self.BG[:, 0], BGyBase))
        self.BG = BGdata

        # prepare all files for baseline
        for file, data in self.currentData.items():
            try:
                dataList.append((file,data))
            except NameError:
                dataList = [data]

        fig, ax = plt.subplots(2,2)
        plt.subplots_adjust(bottom=0.2)
        ax = ax.flatten()
        # print(dataList)

        randList = [random.randint(0, len(self.currentData)) for x in list(range(4))]
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

        for file, data in self.currentData.items():
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

        self.processDict['baselined'] = dataDictBaselined
        self.baselined = dataDictBaselined
        self.currentData = dataDictBaselined
        return dataDictBaselined

    def normalise(self, normaliseRange):
        print(normaliseRange)

    def access_data_set(dataset):
        dataDict = self.processDict[dataset]
        return dataDict

    def plot_current(self, normaliseRange = None, legend = "off"):
        dataDict = self.currentData
        for file, data in dataDict.items():
            dataX = data[:, 0]
            dataY = data[:, 1]
            if normaliseRange:
                dataY = (dataY**2)**0.5
                dataY = dataY-min(dataY[normaliseRange[0]:normaliseRange[1]])
                dataY = dataY/max(dataY[normaliseRange[2]:normaliseRange[3]])
            plt.plot(dataX, dataY, label = file)
        if legend == 'on':
            plt.legend()
        plt.show()

    def plot_BG(self):
        data = self.BG
        plt.plot(data[:, 0], data[:, 1])
        plt.show()

    def data_absolute(self):
        for file, data in self.currentData.items():
            dataX = data[:, 0]
            dataY = data[:, 1]
            dataY = (dataY**2)**0.5
            data = np.column_stack((dataX, dataY))

            try:
                dataAbsoluteDict[file] = data
            except NameError:
                dataAbsoluteDict = {file:data}

        self.processDict['absolute'] = dataAbsoluteDict
        self.dataAbsolute = dataAbsoluteDict
        self.currentData = dataAbsoluteDict

        return dataAbsoluteDict

class ProcessData(DataSet):
    def __init__(self, dataDir):
        DataSet.__init__(self, dataDir)

    # def simple_load_files(fileDir, searchLen = 5):
    #
    #     files = [file for file in os.listdir(fileDir) if file.endswith('.csv')]
    #     BG = None
    #
    #     for file in files:
    #         data = open_csv(file, fileDir)
    #
    #         data, header = parse_header_simple(data, searchLen)
    #         data = np.array(data).astype('float')
    #
    #         if 'BG' in file:
    #             # os.chdir(fileDir)
    #             # move_file(file, fileDir, os.getcwd()+'/BG/')
    #             BG = data
    #             continue
    #
    #
    #         try:
    #             dataDict[file] = data
    #         except NameError:
    #             dataDict = {file:data}
    #
    #         try:
    #             headerDict[file] = header
    #         except NameError:
    #             headerDict = {file:header}
    #
    #     return dataDict, headerDict, BG

class LinescanGraph:
    def __init__(self, lineAxis, spectrumAxis, linescanList, normaliseRange = None): # linescan should be a 2D array of position(real) and intensity at a mode, or a 1D array of just intensities.
        self.linescanList = linescanList
        self.lineAxis = lineAxis
        self.spectrumAxis = spectrumAxis
        if normaliseRange != None:
            self.normMin = min(linescanList[0][normaliseRange[0]:normaliseRange[1], 1])
            self.normMax = max(linescanList[0][normaliseRange[0]:normaliseRange[1], 1])
            self.spectrumAxis.set_ylim(self.normMin, self.normMax)
        self.spectrumLine2D, = spectrumAxis.plot(self.linescanList[0][:, 0],self.linescanList[0][:, 1]) #makes 2D line object of plot of spectrum
        self.shape = np.shape(lineAxis)
        self.dataDict = dataDict
        self.lineIndex = 0
        self.cid = lineAxis.figure.canvas.mpl_connect('button_press_event', self)# function could also call 'LineBuilder(line)' again to remake, but 'self' reuses current object and means redrawing the fig is cleaner than making a new one



    def __call__(self, event):
        if event.inaxes!=self.lineAxis.axes:
            return # in mpl_connect(), if a click is in the axes, event.inaxes is set to the actual plot object axes, therefore this will return if a click is out of bounds

        self.lineIndex = round(event.xdata)
        if normaliseRange != None:
            self.normMin = min(linescanList[0][normaliseRange[0]:normaliseRange[1], 1])
            self.normMax = max(linescanList[0][normaliseRange[0]:normaliseRange[1], 1])
            self.spectrumAxis.set_ylim(self.normMin, self.normMax)
        self.dataX = self.linescanList[self.lineIndex][:, 0]
        self.dataY = self.linescanList[self.lineIndex][:, 1]
        self.spectrumLine2D.set_data(self.dataX, self.dataY)
        self.spectrumAxis.set_title('Spectrum of Index '+str(self.lineIndex))
        self.spectrumAxis.figure.canvas.draw()



def plot_peakDict(axis, linescanList, peakDict):
    for peakLabel, (rangeMin, rangeMax) in peakDict.items():
        runningList = []
        for spec in linescanList:
            runningList.append(max(spec[rangeMin:rangeMax, 1])) # range is performed for non-calibrated axis (i.e. it works for pixels only)
        # print(runningList)
        axis.plot(list(range(len(runningList))), runningList, label = peakLabel)

    return axis

fileDir = r"D:\OneDrive - Massey University\Sam\PhD\Data\Raman\2021\3-23-21 scans\f19/"

mainData = DataSet(fileDir)
mainData.baseline_all()
mainData.subtract_BG(normaliseRange = (20, 80, 20, 80))
mainData.data_absolute()

# mainData.plot_BG()
mainData.plot_current(normaliseRange = None, legend = 'on')
pause()

# dataDict, headerDict = simple_load_files(fileDir)

fig, (ax1, ax2) = plt.subplots(1, 2)

peakDict = {'LA':(673,683), 'E2g':(745, 755)}

for file, data in dataDict.items():
    scanIndex = file[file.index('#')+2:]
    scanIndex = int(scanIndex[:scanIndex.index('#')-1])
    try:
        scanDict[scanIndex] = data
    except NameError:
        scanDict = {scanIndex: data}


# pause()
linescanList = [scanDict[idx] for idx in list(range(len(scanDict)))]


lineIndex = 0
ax1.set_title('Linescan data')
ax2.set_title('spectrum of Index '+str(lineIndex))

lineAxis = plot_peakDict(ax1, linescanList, peakDict)


# ax2.plot(list(range(len(linescanList[0][:, 0]))), linescanList[0][:, 1])

# plt.show()
# linebuilder = LineBuilder(line)
normaliseRange = (650, 800)
lineGraph = LinescanGraph(lineAxis, ax2, linescanList, normaliseRange)
plt.show()
