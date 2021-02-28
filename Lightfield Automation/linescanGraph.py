import sys
sys.path.insert(0, 'C:/GitHub/Raman/Raman')
from Modular_Raman_Analyser import *
from Header_Finder import *

import numpy as np

fileDir = r"C:\Users\sjbro\OneDrive - Massey University\Sam\PhD\Data\Raman\2021\02-28-21 Map and Scans"
# fileDir = r'C:\OneDrive\OneDrive - Massey University\Sam\PhD\Data\Raman\Collabs\DaveMcMorran\09-28-20\785'


dataDir = '{}'.format(fileDir)
# os.chdir(dataDir)

dataDict, headerDict = load_files(dir = fileDir, viewGraph = False)

# organise_files(fileDir = fileDir, report = True)
# process_files(fileDir = fileDir, avgFrames = True, normalise = False, report = True, ignoreWarnings = True)

# pause()

def linescan_slider(dataDict,res=1, normaliseRange = None):
    from matplotlib.widgets import Slider
    from matplotlib.widgets import Cursor
    import matplotlib.cm as cmx
    posList = [0+((-40/39)*index) for index in list(range(40))]
    posList2 = [tuple((round(x, 2), 0.0)) for x in posList]
    print(len(posList2))
    print(posList2)
    # pause()
    for file, data in dataDict.items():


        try:
            hashTag = file[file.index('#'):]

            posX = round(float(hashTag[2:hashTag.index(',')]), 2)
            posY = round(float(hashTag[hashTag.index(',')+1:hashTag.index(')')]), 2)
            print('\n PoSx: ', posX, 'PosY', posY)
            posTag = (posX, posY)
        except:
            print('Error: position tags not found')

        try:
            posDataDict[posTag] = data[:, 1]
        except:
            posDataDict = {posTag: data[:, 1]}
        # try:
        #     posDataList.append(posTag)
        # except:
        #     posDataList = [posTag]

    dataX = data[:, 0]
    dataY = data[:, 1]
    print(posDataDict.keys())
    posDataListOrdered = []
    for x in posList2:
        print(x)
        posDataListOrdered.append(list(posDataDict[x]))


    print(posDataListOrdered[3])


    # print(posDataDict[(0.0, 0.0)])

    # deltaLam = config.BASELINE_SLIDER_LAM_DELTA
    # deltaP = config.BASELINE_SLIDER_P_DELTA
    # lam = config.BASELINE_DEFAULT_LAM
    # p = config.BASELINE_DEFAULT_P
    # sliderLamLimits = config.BASELINE_SLIDER_LAM_LIMITS
    # sliderPLimits = config.BASELINE_SLIDER_P_LIMITS

    lam = 0

    sliderLimits = (0,len(posDataListOrdered)-1)

    niter = 1


    fig,(ax1) = plt.subplots(1,1, sharex=False)
    # plt.subplots_adjust(bottom=0.2)
    ax1.plot(dataX, dataY)
    plt1, = ax1.plot(dataX, dataY)
    # plt2, = ax2.plot(dataX,dataY-baseline)
    if normaliseRange:
        dataYrange = (find_nearest(dataX, normaliseRange[0]), find_nearest(dataX, normaliseRange[1]))
        dataYrange = dataY[dataYrange[0]:dataYrange[1]]
        # ax1.axis([min(dataX), max(dataX), min(dataY[normaliseRange[0]:normaliseRange[1]]),
        # max(dataY[normaliseRange[0]:normaliseRange[1]])])
        ax1.axis([dataX[0], dataX[-1], min(dataYrange), max(dataYrange)])
        # ax2.axis([dataX[0], dataX[-1], min(dataYrange), max(dataYrange)])

    fig.canvas.draw()
    fig.canvas.flush_events()

    axcolor = 'lightgoldenrodyellow'
    axlam = plt.axes([0.2, 0, 0.65, 0.03], facecolor=axcolor)
    # axlam.set_xscale('log')
    # axp = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor=axcolor)
    # axp.set_xscale('log')

    slam = Slider(axlam, 'Point', *sliderLimits, valinit=0, valstep=niter)
    # sp = Slider(axp, 'p', *sliderPLimits, valinit=p, valstep=deltaP)

    def update(val):
        lam = slam.val
        # plt.cla()
        # pos = posDataList[lam]

        dataY = posDataListOrdered[lam]
        if normaliseRange:
            dataYrange = (find_nearest(dataX, normaliseRange[0]), find_nearest(dataX, normaliseRange[1]))
            dataYrange = dataY[dataYrange[0]:dataYrange[1]]
            # ax1.axis([min(dataX), max(dataX), min(dataY[normaliseRange[0]:normaliseRange[1]]),
            # max(dataY[normaliseRange[0]:normaliseRange[1]])])
            ax1.axis([dataX[0], dataX[-1], min(dataYrange), max(dataYrange)])
            # ax2.axis([dataX[0], dataX[-1], min(dataYrange), max(dataYrange)])
        plt1.set_ydata(dataY)
        # plt2.set_ydata(dataY-baseline)

    slam.on_changed(update)
    # sp.on_changed(update)

    plt.show()

linescan_slider(dataDict, normaliseRange = (600, 800))
