import sys
# sys.path.insert(0, 'C:/GitHub/Raman/Raman')
from Modular_Raman_Analyser import *
from Header_Finder import *



# fileDir = 'C:/OneDrive/OneDrive - Massey University/Sam/PhD/Data/Raman/Collabs/Fonterra/output/summed'# /29-4-19 MoS2/output/summed/plot/recal/comp'
fileDir = 'C:/OneDrive/OneDrive - Massey University/Sam/PhD/Data/AS 2019-3 THz/Comparisons/output'
dataDir = '{}'.format(fileDir)
# os.chdir(dataDir)
files = [file for file in os.listdir(dataDir) if file.endswith('.dpt')]
import os
for file in files:
    filename = file
    filename = file[:-4]
    os.rename(r'{}/{}.dpt'.format(fileDir, filename),r'{}/{}.csv'.format(fileDir, filename))

# dataDict, headerDict = load_files(dir = dataDir, viewGraph = False, rangeFrom = 50)
# organise_files(fileDir = fileDir)
# process_files(fileDir = fileDir, sumFrames = True)

# baseline_batch(dir = dataDir, lam = 100000, p = 0.01, edge = True, moveFiles = False, IR = False, saveFile = True, clearOnComplete = False, skipGraph = False)

# print(dataDict[0][276,:])

# move_file(file, '', 'data/')

# killDict, queryDict = find_cosmic_rays(dir = dataDir, dataX = None, dataY = None, multiFrameKill = True)
# print('printTime')
# print(killDict)

# sum_frames()

# for i, file in enumerate(files):
#     find_peaks(dataDir, dataDict, headerDict, files, rangeLow = 350, rangeHigh = 474, dataOutput = True, showFig = True, overwrite = False, fileNumber = i, flipAxis = False, manualPeaks = [379, 405, 445, 428], fixedPeaks = [])
# dataX, dataY = plot_data(dataDict = dataDict, headerDict = headerDict, dataDir = dataDir, offset = 0.75, rangeLow = 675, rangeHigh = 4000)
# sum_files(fileDir, dataDir, saveFig = False, saveData = True, analysisFolder = False, sumType = 'single')
#
# overlay_plot(dataDir = dataDir, saveFig = False, graphTheme = None, useColours = False, markerType = None,
# normLow = 150, normHigh = 3000, normalise = True, axisXRange = None, axisYRange = (-0.1, 1.1),
# offset = 0, xLabel = 'Raman Shift', yLabel = 'Normalised Intensity', subplot = False, calShift = None, legendLoc = 'best')
