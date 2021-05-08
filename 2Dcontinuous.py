import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
import matplotlib.patches as patches
import os
import json
from matplotlib.widgets import Slider, Button
# from ipywidgets import *
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


def move_files(file, dirInitial, dirFinal, copy = None):
    make_dir(dirFinal)
    if copy == True:
        shutil.copyfile('{}/{}'.format(dirInitial, file), '{}/{}'.format(dirFinal, file))
    else:
        shutil.move('{}/{}'.format(dirInitial, file),'{}/{}'.format(dirFinal, file)) #

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

def grab_files(exportDir, fileDir, copy = False):
    files = []
    new = []
    print('checking')

    files = [file for file in os.listdir(exportDir) if file.endswith('.csv')]
    dirList = [file for file in os.listdir(fileDir) if file.endswith('.csv')]

    for file in files:
        try:
            if file in dirList:
                # print('{} already in dir. Skipping.')
                pass
            else:
                new.append(file)
                move_files(file, exportDir, fileDir, copy = copy)
                print(file)

        except Exception as e:
            print(e)
            time.sleep(1)


    time.sleep(0.01)
    return new

def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def simple_background(dataDict, headerDict, dataDir, moveFiles = False, singleBG = True, viewEach = True, saveAll = False, iterate = False, normaliseRange = False, baseline = (100000, 0.001)):
    import matplotlib
    dataList = []

    for file, data in dataDict.items():
        print(file)
        if "BG" in file:
            BGbool = True
            print('found bool')
            BG_Y = data[:, 1]
            BG_X = list(range(len(BG_Y)))
            data = np.column_stack((BG_X, BG_Y))
            if normaliseRange !=False and normaliseRange !=None:
            #     # BG_Y = baseline_show(data, file, baseline[0], baseline[1])
            #     # matplotlib.rc('font', size = 20)
                BG_Y = normalise_variable(data, 'BACKGROUND', normaliseRange, baseline = False, showGraph = False)
            #     print('BG_Y', BG_Y)
            background = np.column_stack((BG_X, BG_Y))

        else:
            dataList.append(file)
    try:
        if BG_Y.any():
            pass
    except NameError:
        print('Error: No background files found')
        BGbool = False
        print('BGbool =', BGbool)
        return dataDict, BGbool


    print('Test: only visible with background file')
    for idx, file in enumerate(dataList):
        data = dataDict[file]
        dataY = data[:, 1]
        dataX = data[:, 0]
        dataX = list(range((len(dataY))))
        data = np.column_stack((dataX, dataY))
        if normaliseRange != False:
            # dataY = baseline_show(data, file, baseline[0], baseline[1])
            dataY = normalise_variable(data, file, normaliseRange, baseline = False, showGraph = False)
        data = np.column_stack((dataX, dataY))

        if iterate == True:
            BG_Y = iterate(data, BG_Y, sensitivity = 0.1) # removes negative intensity artifacts around rayleigh from BG subtraction. Iterates over a bacground subtraction, reducing the background intensity by the sensitivity factor until the resulting subtracted data is above zero (near rayleigh)

        dataYsub = dataY-BG_Y

        if viewEach == True:
            plt.cla()
            plt.figure(figsize = (8,8))
            plt.plot(dataX, dataY, label = file+' raw')
            plt.plot(dataX, dataYsub, label = file+' subbed')
            plt.plot(dataX, BG_Y, color = 'purple', label = 'Background')
            plt.legend()
            plt.title('Check background sub is legit: '+file)
            plt.ion()
            plt.show()
            plt.draw()
            plt.pause(0.001)

        scaleFactor = 1
        while singleBG == True:
            scaleInput = input('Enter scaling factor, or press "enter" to continue with current scale. Type "skip" to skip this file.')
            plt.close(1)
            plt.close(2)
            try:
                if any(scaleInput):
                    print('scaling factor = ', scaleInput)
                    if scaleInput == "skip":
                        break
                    # try:
                    #     if float(scaleFactor):
                    #         pass
                    # except NameError:
                    #     scaleFactor = 1

                    scaleFactor = eval(scaleInput)/scaleFactor
                    dataYsub = dataY-(BG_Y/scaleFactor)

                    plt.cla()
                    plt.figure(figsize = (8,8))
                    plt.ion()
                    # plt.show()
                    plt.plot(dataX, dataY, label = file+' raw')
                    plt.plot(dataX, dataYsub, label = file+' subbed')
                    plt.plot(dataX, (BG_Y/scaleFactor), color = 'purple', label = 'Background')
                    plt.legend()
                    plt.title('Check background sub is legit: '+file)
                    if viewEach == True:
                        plt.show()
                        plt.draw()
                        plt.pause(0.001)

                elif not any(scaleInput):
                    print('no input for:', scaleInput)
                    break
            except:
                print('Command not recognised, please try again.')
                continue

        dataSub = np.column_stack((dataX, dataYsub))
        if saveAll == True:
            # plt.figure(figsize = (8,8))
            # plt.plot(dataX, dataYsub, label = file+' subbed')
            # plt.legend()
            # plt.title(file+ 'BS')
            os.chdir(dataDir)
            make_dir('output/background subtracted')

            # plt.savefig('output/background subtracted/{}_BS.png'.format(file[:-4]))
            np.savetxt('output/background subtracted/{}_BS.csv'.format(file[:-4]), dataSub, delimiter=',', fmt='%s')
            if moveFiles == True:
                os.chdir('{}/data'.format(dataDir))
                make_dir('pre-BS')
                move_file(file, '{}/'.format(os.getcwd()), 'pre-BS/')

        try:
            dataDictSub[file] = dataSub
        except NameError:
            dataDictSub = {file:dataSub}


    dataDict = dataDictSub
    return dataDict, BGbool


def continuous_2D(fileDir, baseline = False):
    dataDir = r'{}'.format(fileDir)
    os.chdir(dataDir)
    newFiles = grab_files(exportDir, fileDir, copy = True)

    # if not os.path.exists(r'{}\data\cubed'.format(dataDir)):
    dataDict, headerDict = load_files(dir = fileDir, viewGraph = False)
    print(len(dataDict), 'files')

    files = [key for key in dataDict.keys()]
    basefile = files[0][:files[0].index('(')-1]

    print(files[0])
    arrayDims = files[0][files[0].index('#')+1:]
    arrayDims = arrayDims[:arrayDims.index('#')]

    arrayDims = (int(arrayDims[:arrayDims.index('x')]), int(arrayDims[arrayDims.index('x')+1:]))
    arrayDimsTotal = (arrayDims[0], arrayDims[1])

    flatArray = []
    posList = []

    arrayOrder = []


    for y in list(range(arrayDims[1])):
        for x in list(range(arrayDims[0])):
            arrayOrder.append((x,y))

    for file, data in dataDict.items():
        posIdx = file[file.index('(')+1:file.index(')')]
        print(posIdx)

        basefile = file[:file.index('(')-1]

        posX = int(posIdx[:posIdx.index(',')])
        posY = int(posIdx[posIdx.index(',')+1:])
        try:
            dataPosDict[(posX,posY)] = data
        except NameError:
            dataPosDict = {(posX,posY): data}

    blankData = np.array(list([575]*1340)).astype('float')

    for order in arrayOrder:
        rowEnd = None
        if rowEnd == None:
            try:
                flatArray.append(dataPosDict[order][:, 1])
            except Exception as e:
                print(e)
                rowEnd = order[1]
                firstZero = order
                print("Row end =", rowEnd)

                for x in range((arrayDims[0]-order[0])):
                    print(x)
                    print("Adding psuedoData to fill array")
                    flatArray.append(blankData)
                arrayDims = (arrayDims[0], rowEnd+1)
                break


    flatArrayFinal = []

    yflat = np.array(flatArray).flatten()


    cube = np.reshape(yflat, (arrayDims[1],arrayDims[0],1340))
    print(cube.shape)

    print('Number of spectra =',cube.shape[0]*cube.shape[1])

    flatArrayFinal = [[float(x)] for x in yflat]
    print('array length: ', len(flatArrayFinal))
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.15)
    idx = 678
    # display initial image
    im_h = ax.imshow(cube[:, :, idx], cmap='hot', interpolation='nearest')#, vmax = 1500)
    vmax = 1000
    color_bar = plt.colorbar(im_h)

    # setup a slider axis and the Slider
    ax_wavelength = plt.axes([0.23, 0.02, 0.56, 0.04])
    # ax_intensity = plt.axes([0.23, 0.05, 0.56, 0.07])

    slider_wavenumber = Slider(ax_wavelength, 'Wavenumber', 0, cube.shape[2]-1, valinit=idx)
    # slider_intensity = Slider(ax_intensity, 'Intensity Max', 0, cube.shape[2]-1, valinit=vmax)

    axpos1 = plt.axes([0.05, 0.1, 0.05, 0.03])
    axpos2 = plt.axes([0.93, 0.1, 0.05, 0.03])

    button1 = Button(axpos1, '<', color='w', hovercolor='b')
    button2 = Button(axpos2, '>', color='w', hovercolor='b')

    def forward(vl):
        pos = slider_wavenumber.val
        slider_wavenumber.set_val(slider_wavenumber.val+1)

    def backward(vl):
        pos = slider_wavenumber.val
        slider_wavenumber.set_val(slider_wavenumber.val-1)


    # update the figure with a change on the slider
    def update_wavenumber(val):
        idx = int(round(slider_wavenumber.val))
        im_h.set_data(cube[:, :, idx])
    # def update_intensity(val):
    #     idx = int(round(slider_intensity.val))
    #     im_h.set_xlim(xmin = 0, xmax = 2000)


    slider_wavenumber.on_changed(update_wavenumber)
    # slider_intensity.on_changed(update_intensity)
    button1.on_clicked(backward)
    button2.on_clicked(forward)

    while True:
        newFiles = grab_files(exportDir, fileDir, copy = True)
        if len(newFiles) == 0:
            # plt.show()
            time.sleep(5)
            continue
        else:
            try:
                dataDict, headerDict = load_files(dir = fileDir, viewGraph = False)

                files = [key for key in dataDict.keys()]
                basefile = files[0][:files[0].index('(')-1]

                arrayDims = files[0][files[0].index('#')+1:]
                arrayDims = arrayDims[:arrayDims.index('#')]

                arrayDims = (int(arrayDims[:arrayDims.index('x')]), int(arrayDims[arrayDims.index('x')+1:]))
                arrayDimsTotal = (arrayDims[0], arrayDims[1])

                flatArray = []
                posList = []
                arrayOrder = []

                for y in list(range(arrayDims[1])):
                    for x in list(range(arrayDims[0])):
                        arrayOrder.append((x,y))

                for file, data in dataDict.items():
                    posIdx = file[file.index('(')+1:file.index(')')]
                    basefile = file[:file.index('(')-1]
                    posX = int(posIdx[:posIdx.index(',')])
                    posY = int(posIdx[posIdx.index(',')+1:])
                    try:
                        dataPosDict[(posX,posY)] = data
                    except NameError:
                        dataPosDict = {(posX,posY): data}

                blankData = np.array(list([575]*1340)).astype('float')

                for order in arrayOrder:
                    rowEnd = None
                    if rowEnd == None:
                        try:
                            flatArray.append(dataPosDict[order][:, 1])
                        except Exception as e:
                            print(e)
                            rowEnd = order[1]
                            for x in range((arrayDims[0]-order[0])):
                                flatArray.append(blankData)
                            arrayDims = (arrayDims[0], rowEnd+1)
                            break


                flatArrayFinal = []
                yflat = np.array(flatArray).flatten()
                cube = np.reshape(yflat, (arrayDims[1],arrayDims[0],1340))
            except Exception as e:
                print(e)
                time.sleep(1)
                continue

        normVals = cube[:, :, idx]
        im_h.set_data(cube[:, :, idx])
        yExtent = len(cube[:, 0, 0])
        Left, Right, Bottom, Top = im_h.get_extent()
        im_h.set_extent((Left, Right, (yExtent-0.5), Top))
        im_h.set_clim(vmin = normVals.min(), vmax = normVals.max())
        plt.pause(0.5)

    # plt.show()





peakDict = {'LA':(673,683), 'E2g':(745, 755)}

        # dataX, dataY = (data[:, 0], data[:, 1])
exportDir = r'H:\PhD\Raman\2021\4-27-21 CVD\flaketest35'
fileDir = r"C:\Users\sjbro\OneDrive - Massey University\Sam\PhD\Data\Raman\2021\4-27-21 CVD\flaketest34"
dataDir = fileDir



make_dir(fileDir)
plotList = []
acquisitionTime = 10.1

# grab_files(exportDir, fileDir, copy = True)
continuous_2D(fileDir, baseline = False)

pause('files moved')

dataDict = data_dictionary(dataDir)
dataDict = baseline_all(dataDict, lam = 1000, p = 0.01, showGraph = True)
scanDict = make_scanList(dataDict)
plot_lines(dataDict)
plt.show()
# pause()

count = 0
while True:
    exportFiles = grab_files(exportDir, fileDir)
    if len(exportFiles) > 0:
        print('New files')
        plt.close()
        dataDict = data_dictionary(dataDir)
        dataDict = baseline_all(dataDict, lam = 1000, p = 0.01, showGraph = False)
        scanDict = make_scanList(dataDict)
        plot_lines(dataDir)
        plt.show()
    if len(exportFiles) == 0:
        count += 1
