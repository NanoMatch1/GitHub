import matplotlib.pyplot as plt
import sys
import os
import numpy as np
import csv
import fnmatch
import shutil
from shutil import copyfile
import random
import math
import time
import json
import pickle


sys.path.insert(0, r'C:\Users\sjbro\github\Raman\SimpleRaman package/')
sys.path.insert(0, 'C:\GitHub\Raman\Raman')
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
        dataAll = np.array(data)
    except:
        print("Array failed - check data structure")
        return

    data = dataAll[dataIdx:, :]
    if NAcol == True:
        data = np.column_stack((list(range(len(data[:, 1]))), data[:, 1]))
    header = dataAll[:dataIdx, :]
    return data, header

def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def move_file(file, dirInitial, dirFinal):
    make_dir(dirFinal)
    shutil.move('{}{}'.format(dirInitial, file),'{}{}'.format(dirFinal, file)) #

def grab_files(exportDir, fileDir):
    files = []
    print('checking')

    files = [file for file in os.listdir(exportDir) if file.endswith('.csv')]

    for file in files:
        while True:
            try:
                move_file(file, exportDir, fileDir)
                print(file)
                break
            except Exception as e:
                print("Cannot grab files:")
                print(e)
                time.sleep(10)
                break

    time.sleep(5)
    return files

def simple_load_files(fileDir, searchLen = 5):

    try:
        files = [file for file in os.listdir(str(fileDir)+'/BG/') if file.endswith('.csv')]
        data = open_csv(files[0], fileDir+'/BG/')
        data, header = parse_header_simple(data, searchLen)
        data = np.array(data).astype('float')
        BG = data
    except Exception as e:
        print("Failed at finding folder")
        print(e)
        # pause()
    files = [file for file in os.listdir(fileDir) if file.endswith('.csv')]
    BG = None

    for file in files:
        data = open_csv(file, fileDir)

        data, header = parse_header_simple(data, searchLen)
        data = np.array(data).astype('float')

        if BG is None:
            if 'BG' in file: # edit later to search for BG folder - write function to check
                # os.chdir(fileDir)
                # move_file(file, fileDir, fileDir+'/BG/')
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


        # data = data.tolist()    # to save as json files, need numpy array to be a list
        # header = header.tolist()
        if BG is not None:
            BG = np.array(BG).astype('float')
            # BG = BG.tolist()

        # try:
        #     dataDictList[file] = data
        # except NameError:
        #     dataDictList = {file:data}
        #
        # try:
        #     headerDictList[file] = header
        # except NameError:
        #     headerDictList = {file:header}

        # processDict = {'raw': dataDictList, 'header':headerDictList,'BG':BG}

    return dataDict, headerDict, BG #, processDict



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

    scriptPath = os.path.realpath(__file__)
    mainFolder = scriptPath[:scriptPath.index('InstantRaman')+13]
    rawData = []
    header = []
    BG = []

    def __init__(self):
        pass

    def load_fileDir(self, dataDir):
        self.rawData, self.header, self.BG = simple_load_files(dataDir)

        self.meta = {'dir':dataDir, 'header':self.header}
        self.dataDir = dataDir
        self.currentData = self.rawData
        self.processDict = {'raw':self.rawData}


    def save_database(self):
        tagList = input('Enter tags separated by comma, or press enter to continue.\n').split(',')
        self.meta['tags'] = tagList

        seriesName = input('Enter name of data series:\n')
        series = {'meta':self.meta, 'data':self.processDict} # adds metadata and processDict data into dictionary with seires name as the key

        print('Saving to database...')

        try:
            with open('masterDatabase.P', 'rb') as handle: #opens masterDatabse file
                masterDatabase = pickle.load(handle)
            masterDatabase[seriesName] = series #appends to data from master database
            with open('masterDatabase.P', 'wb') as handle: # overwrites master database
                pickle.dump(masterDatabase, handle, protocol=pickle.HIGHEST_PROTOCOL)
            with open('{}/{}_database.P'.format(self.dataDir, seriesName), 'wb') as handle: # makes separate database file in dataDir folder as a redundancy
                pickle.dump(masterDatabase, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print('saved')
        except FileNotFoundError:
            print('No database file found - try moving database file to script folder:\n{}'.format(self.mainFolder))
            print('Making new database file...')
            with open('masterDatabase.P', 'wb') as handle:
                pickle.dump({seriesName:series}, handle, protocol=pickle.HIGHEST_PROTOCOL) # generates first database folder
            print('Save complete.')
            return

        print('Save complete.')

    def load_database(self):
        with open('masterDatabase.P', 'rb') as handle:
            self.masterDatabase = pickle.load(handle)

    def check_BG(self, dataDir): # edit later to search for BG folder - write function to check

        if self.BG is not None:
            print('BG attribute exists.')
            return
        files = [file for file in os.listdir(dataDir) if file.endswith('csv')]
        for file in files:
            if 'BG' in file:
                print('BG found.')
                return

        files = [file for file in os.listdir(str(dataDir)+'/BG/')]
        if len(files) == 0:
            print('BG file not found.')
            return
        for file in files:
            if 'BG' in file:
                copyfile(str(dataDir)+'/BG/', dataDir)
                self.rawData, self.header, self.BG = simple_load_files(dataDir)
                print('BG found.')
                return

    def subtract_BG(self, normaliseRange = None, baseline = False, showGraph = False):
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
            data = np.column_stack((dataX, dataYsub))
            if showGraph == True:
                plt.plot(dataX, dataY, label = 'raw')
                plt.plot(dataX, BGy, label = 'BG')
                plt.plot(dataX, dataYsub, label = 'subtracted')
                plt.legend()
                plt.show()

            # data = data.tolist()

            try:
                dataBGsub[file] = data
            except NameError:
                dataBGsub = {file:data}

        self.processDict['BGsub'] = dataBGsub
        self.BGsub = dataBGsub
        self.currentData = dataBGsub

        return dataBGsub

        # if normaliseRange:

    def baseline_all(self, lam = 10000, p = 0.001, showGraph = True):
        from data_processing.baseline import baseline_als

        # baseline the BG file
        if self.BG is not None:
            BGy = self.BG[:, 1]
            baseline = baseline_als(BGy, lam, p)
            BGyBase = BGy - baseline
            BGdata = np.column_stack((self.BG[:, 0], BGyBase))
            self.BG = BGdata
        elif self.BG is None:
            ans = input('BG not found. Press enter to continue without BG.')

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
            # pause('Continue to baseline all.')

        for file, data in self.currentData.items():
            dataX = data[:, 0]
            dataY = data[:, 1]
            baseline = baseline_als(dataY, lam, p)
            dataYbase = dataY - baseline
            data = np.column_stack((dataX, dataYbase))
            # data = data.tolist()

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

    def plot_current(self, normaliseRange = None, legend = "off", plotRange = 'all'):
        dataDict = self.currentData
        if plotRange == 'all':
            plotRange = (0, len(dataDict))

        for idx, (file, data) in enumerate(dataDict.items()):
            if plotRange[0] <= idx <= plotRange[1]:
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
            # data = data.tolist()

            try:
                dataAbsoluteDict[file] = data
            except NameError:
                dataAbsoluteDict = {file:data}

        self.processDict['absolute'] = dataAbsoluteDict
        self.dataAbsolute = dataAbsoluteDict
        self.currentData = dataAbsoluteDict

        return dataAbsoluteDict

    def linescan_plot(self, peakDict = None, normaliseRange = None):
        # plt.close()
        fig, (ax1, ax2) = plt.subplots(1, 2)

        if peakDict is None:
            peakDict = {'LA':678, 'E2g':750, 'TO':647, 'LA-2':676, 'LA-3':675}

        for file, data in self.currentData.items():
            scanIndex = file[file.index('#')+2:]
            scanIndex = int(scanIndex[:scanIndex.index('#')-1])
            try:
                scanDict[scanIndex] = data
            except NameError:
                scanDict = {scanIndex: data}

        linescanList = [scanDict[idx] for idx in list(range(len(scanDict)))]

        lineIndex = 0
        ax1.set_title('Linescan data')
        ax2.set_title('spectrum of Index '+str(lineIndex))
        ax2.set_xlim(500, 1000)
        lineAxis = plot_peakDict(ax1, linescanList, peakDict)
        ax1.legend()
        # ax2.plot(list(range(len(linescanList[0][:, 0]))), linescanList[0][:, 1])
        if normaliseRange is None:
            normaliseRange = (min(linescanList[0][:, 0]), max(linescanList[0][:, 0]))
        lineGraph = LinescanGraph(self.currentData, lineAxis, ax2, linescanList, normaliseRange)
        plt.show()

        return linescanList, peakDict

# class ProcessData(DataSet):
#     def __init__(self, dataDir):
#         DataSet.__init__(self, dataDir)

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
    def __init__(self, currentData, lineAxis, spectrumAxis, linescanList, normaliseRange = None): # linescan should be a 2D array of position(real) and intensity at a mode, or a 1D array of just intensities.
        self.linescanList = linescanList
        self.lineAxis = lineAxis
        self.spectrumAxis = spectrumAxis
        self.normalise = None
        self.dataY = linescanList[0][:, 1]
        if normaliseRange != None:
            self.normMin = normaliseRange[0]
            self.normMax = normaliseRange[1]
            self.yRange = (min(self.dataY[self.normMin:self.normMax]), max(self.dataY[self.normMin:self.normMax]))
            self.spectrumAxis.set_ylim(self.yRange[0], self.yRange[1])
            self.normalise = True
        self.spectrumLine2D, = spectrumAxis.plot(self.linescanList[0][:, 0],self.linescanList[0][:, 1]) #makes 2D line object of plot of spectrum
        self.shape = np.shape(lineAxis)
        self.currentDict = currentData
        self.lineIndex = 0
        self.cid = lineAxis.figure.canvas.mpl_connect('button_press_event', self)# function could also call 'LineBuilder(line)' again to remake, but 'self' reuses current object and means redrawing the fig is cleaner than making a new one



    def __call__(self, event):
        if event.inaxes!=self.lineAxis.axes:
            return # in mpl_connect(), if a click is in the axes, event.inaxes is set to the actual plot object axes, therefore this will return if a click is out of bounds

        self.lineIndex = round(event.xdata)
        self.dataX = self.linescanList[self.lineIndex][:, 0]
        self.dataY = self.linescanList[self.lineIndex][:, 1]
        if self.normalise is not None:
            self.yRange = (min(self.dataY[self.normMin:self.normMax]), max(self.dataY[self.normMin:self.normMax]))
            self.spectrumAxis.set_ylim(self.yRange[0], self.yRange[1])
        self.spectrumLine2D.set_data(self.dataX, self.dataY)
        self.spectrumAxis.set_title('Spectrum of Index '+str(self.lineIndex))
        self.spectrumAxis.figure.canvas.draw()



def plot_peakDict(axis, linescanList, peakDict):

    for peakLabel, value in peakDict.items():
        runningList = []
        print(peakLabel)
        for spec in linescanList:
            # print(spec)
            # print(spec[value])
            # pause()
            runningList.append(spec[value, 1]) # range is performed for non-calibrated axis (i.e. it works for pixels only)
        print(runningList)
        axis.plot(list(range(len(runningList))), runningList, label = peakLabel)

    return axis

fileDir = r"D:\OneDrive - Massey University\Sam\PhD\Data\Raman\2021\3-29-21 scans\line1/"
# make_dir(fileDir)
# grab_files(r'H:\PhD\Raman\2021\3-29-21 scan/', fileDir)
# pause()

mainData = DataSet()
mainData.load_database()
print(mainData.masterDatabase.keys())


# mainData.load_fileDir(fileDir)
# mainData.save_database()

# for key, item in mainData.masterDatabase.items():
#     print(key)
#     print(mainData.masterDatabase[key])
# print('\n'*5)

pause()
# print(mainData.processDict)
# mainData.load_data_npz()
# print(mainData.databaseKeys)
# print(mainData.masterDatabase['baselined'])

    # for x in dataset:
    #     print(x)
    # # print(key, item)
    #     pause()

# print(mainData.processDict)
# # print(mainData.header)
pause()
# mainData.check_BG(fileDir)
# mainData.plot_current(legend = 'on', plotRange = (10, 12))
# # pause()

mainData.baseline_all(lam = 10000, p = 0.0001)
# mainData.subtract_BG(normaliseRange = (10, 80, 10, 90), showGraph = False)
mainData.data_absolute()

# mainData.plot_BG()
# mainData.plot_current(normaliseRange = None, legend = 'on')
linescanList, peakDict = mainData.linescan_plot(peakDict = {'LA':678, 'E2g':750, 'ZA(M)':647, 'LA-1':677, 'TA(M)':634}, normaliseRange = (650, 900))
# mainData.save_data_json(fileDir, indexKey = 'OneDrive')
# mainData.save_data_npz(fileDir, indexKey = 'OneDrive')
pause()

# dataDict, headerDict = simple_load_files(fileDir)
#
# fig, (ax1, ax2) = plt.subplots(1, 2)
#
# peakDict = {'LA':(673,683), 'E2g':(745, 755)}
#
# for file, data in dataDict.items():
#     scanIndex = file[file.index('#')+2:]
#     scanIndex = int(scanIndex[:scanIndex.index('#')-1])
#     try:
#         scanDict[scanIndex] = data
#     except NameError:
#         scanDict = {scanIndex: data}
#
#
# # pause()
# linescanList = [scanDict[idx] for idx in list(range(len(scanDict)))]
#
#
# lineIndex = 0
# ax1.set_title('Linescan data')
# ax2.set_title('spectrum of Index '+str(lineIndex))
#
# lineAxis = plot_peakDict(ax1, linescanList, peakDict)
#
#
# # ax2.plot(list(range(len(linescanList[0][:, 0]))), linescanList[0][:, 1])
#
# # plt.show()
# # linebuilder = LineBuilder(line)
# normaliseRange = (650, 800)
# lineGraph = LinescanGraph(lineAxis, ax2, linescanList, normaliseRange)
# plt.show()
