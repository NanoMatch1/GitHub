from ipywidgets import *
# import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
import matplotlib.patches as patches
import os
import json
from matplotlib.widgets import Slider, Button

import sys
sys.path.insert(0, 'C:/GitHub/Raman/Raman')
from Modular_Raman_Analyser import *
from Header_Finder import *


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


#set the directory to the desired data directory
#Hint: Right-click in the address bar in File Explorer and copy the address
# os.chdir(r'2D_map_data')

fileDir = r"C:\Users\sjbro\OneDrive - Massey University\Sam\PhD\Data\Raman\2021\3-26-21 scans\CVD3"
# fileDir = r'C:\OneDrive\OneDrive - Massey University\Sam\PhD\Data\Raman\Collabs\DaveMcMorran\09-28-20\785'
dataDir = r'{}'.format(fileDir)
BG_sub = True
#check the current directory.
os.chdir(dataDir)
if not os.path.exists(r'{}\data\cubed'.format(dataDir)):
    dataDict, headerDict = load_files(dir = fileDir, viewGraph = False)
    # print('hi')
    # pause()
    # if BG_sub == True:
    #     simple_background(dataDict, headerDict, dataDir, moveFiles = False, singleBG = False, viewEach = False, saveAll = True, iterate = False, normaliseRange = (100, 200, 700, 720), baseline = (100000, 0.001))
    # pause()
    files = [key for key in dataDict.keys()]
    basefile = files[0][:files[0].index('(')-1]

    #dir_path = "./data/" #Path to data directory
    # basefile = "f1map1" # Base file name
    ext = ".csv" # Extension
    '''##################### enter array dims here'''
    arrayDims = (26,25)
    flatArray = []
    posList = []
    # orderedPosList = []
    arrayOrder = []
    filemap = r'C:\GitHub\Github\Lightfield Automation\ScanLists\{}_list.json'.format(basefile)

    with open(filemap) as json_file:
        mapDict = json.load(json_file)

    # for file in files:
    #     print(file[file.index(')')+2:-4])
    # pause()

    for x in list(range(arrayDims[0])):
        for y in list(range(arrayDims[1])):
            arrayOrder.append((y,x))

    #         orderedPosList.append('{}'.format(mapDict["({}, {})".format(y, x)]))
    # print(orderedPosList)
    # posList = [mapDict['{},{}'.format(x, y)] for x in list(range(arrayDims[0]+1)) for y in list(range(arrayDims[1]+1))]

    # print(orderedPosList)
    # pause()

    for file, data in dataDict.items():
        posIdx = file[file.index('(')+1:file.index(')')]
        print(posIdx)
        # posList.append(posIdx)
        basefile = file[:file.index('(')-1]
        # pos = float(posIdx[:posIdx.index(',')]), float(posIdx[posIdx.index(',')+1:])
        # print(str(pos))
        posX = int(posIdx[:posIdx.index(',')])
        posY = int(posIdx[posIdx.index(',')+1:])
        try:
            dataPosDict[(posX,posY)] = data
        except NameError:
            dataPosDict = {(posX,posY): data}


    print(dataPosDict.items())
    # pause()
    for order in arrayOrder:
        flatArray.append(dataPosDict[order][:, 1])

    # pause()
    flatArrayFinal = []
    # for spec in flatArray:
    #     flatArrayFinal.append()
    # print(posList)
    # print(dataPosDict)
    yflat = np.array(flatArray).flatten()
    print(yflat)
    print(len(yflat))

    cube = np.reshape(yflat, (arrayDims[0],arrayDims[1],1340))
    print(cube.shape)
    # pause()
    # print(len(dataPosDict))

    ''' Need to generate a 3D array or "cube" (x, y, spectra)'''
    # import or generate array/scan dimensions


    # dat = []
    # for idx, x in enumerate(xScan):
    #     rowX = []
    #     rowY = []
    #
    #     for y in yScan:
    #         rowX.append(x)
    #         rowY.append(y)
    #         data = dataPosDict[str(x)+'.0,'+str(y)+'.0']
    #         dat.append(data[:, 1])
    #
    #     try:
    #         xArray = np.column_stack((xArray, rowX))
    #         yArray = np.column_stack((yArray, rowY))
    #         # dataArray = np.column_stack((dataArray, dat))
    #     except NameError:
    #         xArray = np.array(rowX).astype('float')
    #         yArray = np.array(rowY).astype('float')
    # #         # dataArray = np.array(dat).astype(float)
    #
    # print(basefile)
    # # pause()

        # for key, pos in map.items():
        #     mapDict[key]



    # print(posList)
    # flatArray = []
    # for file, data in dataDict.items():
    #     for x in posList:
    #         pos = '({},{})'.format(x[0],x[1])
    #         print(pos)
            # if
    # newlist = []
    # pause()
    # for x in list(range(arrayDims[0]+1)):
    #     for y in list(range(arrayDims[1]+1)):
    #         newlist.append(mapDict['({}, {})'.format(x, y)])
    # print(newlist)
    # pause()
    # # for pos in posList:
    # # xScan = list(range(20))
    # # yScan = list(range(24))
    # print(flatArray)
    # pause()
    #
    # print(mapDict)
    # xArray = []
    # yArray = []
    # for index, pos in mapDict.items():
    #     xArray.append()
    # print(mapDict['(0, 0)'])
    # pause()
    # # print(xArray, yArray, dataArray)
    # print(len(dat))

    # dataArray = dataArray[:, 1]
    # print(dataArray)
    # pause()

    #
    # # cube = np.stack((xArray,yArray,dataArray))
    # xflat = xArray.flatten()
    # yflat = yArray.flatten()
    # dataArray = np.array(dat).astype('float')
    # dataflat = dataArray.flatten()
    # print(len(dataflat))
    # # pause()
    #
    # print(xflat, yflat,dataflat)
    # # cube = np.append(xflat,dataArray)
    #
    #
    # ''' dataArray = []
    # for i in list(range(31)):
    #     for j in list(range(21)):
    #         dataArray.append(dataPosDict[xArray[i,j],yArray[i,j]))'''
    # cube = np.reshape(dataflat, (31,21,1340))
    #
    #
    # pause('cubed')


    # filenames = [basefile + "_" + str(i) + ext for i in range(1,2501)]
    # df = pd.concat([pd.read_table(f, delim_whitespace=True, index_col=0, header=None, names=[None, str(i+1)]).transpose() for i, f in enumerate(filenames)])
    # df.head(10)

    #
    # cube = df.values.reshape(50,50,1600).transpose(1,0,2)
    # print(cube.shape)
    #
    print('Number of spectra =',cube.shape[0]*cube.shape[1])
    # Check the cube is transposed correctly
    print(cube[0,0,:])
    plt.plot(list(range(1340)), cube[0,0,:])
    plt.show()
    yflat = list(yflat)
    # for x in yflat:
    #     print(x)
    flatArrayFinal = [[float(x)] for x in yflat]
    print(flatArrayFinal)
    pause('Press <Enter> to save cube data file')
    make_dir('data/cubed')

    with open('{}/data/cubed/{}_cube.csv'.format(dataDir, basefile), 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(flatArrayFinal)
    np.savetxt('data/cubed/{}_cube_dims.txt'.format(basefile), (arrayDims[0], arrayDims[1], 1340), delimiter=',', fmt = '%s')

# pause()
if os.path.exists(r'{}\data\cubed'.format(dataDir)):
    files = [file for file in os.listdir('{}\data\cubed'.format(dataDir)) if file.endswith('.csv')]
    with open(r'{}\data\cubed\{}'.format(dataDir, files[0]), 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        data = list(reader)
    txtFile = [file for file in os.listdir('{}\data\cubed'.format(dataDir)) if file.endswith('.txt')]
    with open(r'{}\data\cubed\{}'.format(dataDir, txtFile[0]), 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        txtFile = list(reader)

    # dims = [txtFile[x][0] for x in list(range(len(txtFile)))]
    dims = (int(txtFile[0][0]),int(txtFile[1][0]),int(txtFile[2][0]))
    print(dims)
    # pause()
    yflat = []
    for x in list(range(len(data))):
        yflat.append(data[x][0])
    yflat = np.array(yflat).astype(float)
    cube = np.reshape(yflat, dims)

print(cube)
# pause()
# baseline removal

# import sys
# sys.path.insert(0, '../libs/')  # the location of libs is given relative to the working directory
# from data_processing.baseline import baseline_als
#
# fig, ax = plt.subplots(1,2, figsize=(10,6))
#
# lp = 100  #leftmost pixel index
# rp = 1600 #rightmost pixel index
#
# lam = 30000000 #smoothing parameter
# p = 0.05 #offset parameter
#
# pixel_domain = np.arange(lp,rp)
#
# baseline = baseline_als(cube[0,0,pixel_domain],lam,p)
# corrected = cube[0,0,pixel_domain] - baseline
#
# ax[0].plot(pixel_domain,cube[0,0,pixel_domain],pixel_domain,baseline)
# ax[1].plot(pixel_domain,corrected)

# do baseline correction for all spectra
#
#
# baselines = np.zeros((cube.shape[0],cube.shape[1],len(pixel_domain)))
# baselined = np.zeros((cube.shape[0],cube.shape[1],len(pixel_domain)))
#
# for i in np.arange(cube.shape[0]):
#     for j in np.arange(cube.shape[1]):
#         baselines[i,j] = baseline_als(cube[i,j,pixel_domain],lam,p)
#         baselined[i,j] = cube[i,j,pixel_domain] - baselines[i,j]
# print(baselined.shape)

# '''
# A simple check for cosmic spikes - compare max. value with
# standard deviation; a small number of cosmics are present if max value
# far exceeds std. dev.
# '''
#
# spec_err = np.std(baselined)
#
# print('max value:', baselined.max())
# print('Std. Dev. of baselined:', spec_err)

# remove cosmics spikes using a mask based on a median filter

# import scipy.signal
#
# baselined_medfilt = scipy.signal.medfilt(baselined, 5)  # apply median filter to dataset
#
# bad = (np.abs(baselined - baselined_medfilt) / spec_err) > 50.0  # set the criteria that defines a cosmic spike
# cosmic_locations = np.column_stack(np.where(bad))  # create a mask of cosmic spike locations
# print(cosmic_locations.shape)
#
#
# print('Number of cosmic spikes:',cosmic_locations.size)
#
# print('max value before filter:', baselined.max())
#
# baselined[bad] = baselined_medfilt[bad] # use the mask to replace the cosmic spikes with their median filtered equivalents
#
# print('max value after filter:', baselined.max())

# #check 10 randomly selected spectra, baselines and baselined spectra
# from numpy.random import randint
#
# fig, ax = plt.subplots(1,2, figsize=(10,6))
# for i in range(10):
#     for j in range(10):
#         i = randint(1,baselined.shape[0])
#         j = randint(1,baselined.shape[1])
#         ax[0].plot(pixel_domain,cube[i,j,lp:rp], pixel_domain, baselines[i,j,:])
#         ax[1].plot(pixel_domain, baselined[i,j,:])
#
'''
Explore
Use the slider widget below to move through the wave numbers.

Mouse over on image to see pixel coordinates.

Go slow! Use arrow keys to step for more control.'''



# a = np.random.random((16, 16))
# plt.imshow(a, cmap='hot', interpolation='nearest')
# plt.show()

# figure axis setup
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.15)
idx = 750
# display initial image
im_h = ax.imshow(cube[:, :, idx], cmap='hot', interpolation='nearest', vmin = 0)#, vmax = 1500)
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
plt.show()

#
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# img = ax.imshow(cube[:,:,678], interpolation='bilinear', cmap='hot')
# color_bar = plt.colorbar(img)
# dataX = list(range(1340))
# # plt.show()
#
# def update_im(idx):
#     img.set_data(cube[:,:,idx-1])
#     fig.canvas.draw()
#     return "Wave number: " + str(dataX[(idx-1)])
#
# update_im(idx=678)
# fig.show()
pause()

# ENTER WAVE NUMBER INDEX OF INTEREST
w = 1192

# ENTER COORDINATES HERE
x0 = 22
y0 = 5
x1 = 22
y1 = 43
#
#
#
# tol = 0.3
#
#
# # I pad the sampling line to enable me to see which pixels fall on the line.
# verts = [(x0-tol, y0+tol),
#          (x1-tol, y1+tol),
#          (x1+tol, y1-tol),
#          (x0+tol, y0-tol),
#          (x0-tol, y0+tol)]
#
# codes = [Path.MOVETO,
#          Path.LINETO,
#          Path.LINETO,
#          Path.LINETO,
#          Path.CLOSEPOLY]
#
# path = Path(verts, codes)
#
# xs, ys = zip(*verts)
#
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# img = ax.imshow(baselined[:,:,w], interpolation='bilinear', cmap='hot')
# color_bar = plt.colorbar(img)
# plt.plot(xs, ys, color='g', lw=2, marker='o', ms=3)
# plt.show()
#
# fig.savefig(basefile+"_raman_map.png",dpi=1200)

# SELECTING ALL PIXELS THAT FALL ON LINE

# x = np.arange(0, 50, 1)
# y = np.arange(0, 50, 1)
# xx, yy = np.meshgrid(x, y, indexing='xy')
#
# plt.figure()
# plt.plot(xx,yy, marker=',', color='w', linestyle='none')
# plt.show()
#
# points = np.hstack((xx.reshape((-1,1)), yy.reshape((-1,1))))
#
# mask = path.contains_points(points)
#
# mask.shape = xx.shape
#
# plt.imshow(mask)
# plt.plot(xs, ys, color='g', lw=2, marker='o', ms=3)


# fig = plt.figure()
# ax = fig.add_subplot(2, 1, 1)
# ax1, = ax.plot(baselined[mask][1])
# ax.set_title("Use sliders to move along sampling line and wave length")
# ax.set_ylim(top=baselined[mask].max())
# ax2 = ax.axvline(x=0, color='r')
# ax.set_xlabel("Wave number index")
#
# ax_b = fig.add_subplot(2, 1, 2)
# ax_b.set_ylim(top=baselined[mask].max(), bottom=baselined[mask].min())
# ax_b1, = ax_b.plot(baselined[mask][:,800])
# ax_b2 = ax_b.axvline(x=0, color='r')
# ax_b.set_xlabel("Point along line")
# plt.tight_layout()
#
# def update_plt(point=0, wavenumber=0):
#     ax1.set_ydata(baselined[mask][point-1])
#     ax.set_ylim(top=(baselined[mask][point-1].max()+5))
#     ax2.set_xdata(wavenumber-1)
#     ax_b1.set_ydata(baselined[mask][:,wavenumber])
#     ax_b.set_ylim(top=(baselined[mask][:,wavenumber].max()+5))
#     ax_b2.set_xdata(point)
#     fig.canvas.draw()
#     return "Wave number: " + str(df.columns[(wavenumber-1)+lp])
#
# interact(update_plt, point=(0,len(baselined[mask])-1,1), wavenumber=(1,cube.shape[2]-lp,1))
# # interact(update_wav, wav=(1,1600,1))
#
# fig.savefig(basefile+"_linescan_explore.png",dpi=600)


# # ENTER WAVE NUMBER INDEX OF INTEREST
# w = [940,649,588,1184]
# labels = ["{0:.1f}".format(df.columns[wn]) for wn in w]
# components = ['baseline', 'Trimyristin', 'beta-carotene', 'CH group']
#
# plt.figure()
# lines = plt.plot(baselined[mask][:,w])
# legend1 = plt.legend(lines, [str(label)+" cm"+r"$^{-1}$" for label in labels],loc=2)
# plt.legend(lines, ['baseline', 'Trimyristin', 'beta-carotene', 'CH group'],loc=1)
# plt.gca().add_artist(legend1)
# plt.xlabel('Line-scan position')
# plt.ylabel('Relative Intensity')
#
#
# plt.savefig(basefile+"_linescan_"+str(x0)+'_'+str(x1)+'_'+str(y0)+'_'+str(y1)+".png",dpi=1200)


# w = [95,361,428,1192] # ENTER WAVE NUMBER INDEX OF INTEREST
# RS = ["{0:.1f}".format(df.columns[wn]) for wn in w]
# labels = ['baseline', 'Unknown', 'beta-carotene', 'CH group']  # enter name of component that corresponds to peaks identified with w
#
# fig, ax = plt.subplots(1, figsize=(7,5))
# plotBox = ax.get_position()
# ax.set_position([plotBox.x0, plotBox.y0+0.12, plotBox.width, plotBox.height*0.9])
# lines = ax.plot(baselined[mask][:,w]) # create line objects to be used in legend
# ax.legend(lines, [label+"\n"+" "+str(RS)+" cm"+r"$^{-1}$" for label, RS in zip(labels,RS)],
#            loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=len(w), prop={'size': 10})
# ax.set_xlabel('Line-scan position')
# ax.set_ylabel('Relative Intensity')
#
#
# #plt.savefig(basefile+"_linescan_"+str(x0)+'_'+str(x1)+'_'+str(y0)+'_'+str(y1)+".png",dpi=600)

#
# w = [95,361,428,1192] # ENTER WAVE NUMBER INDEX OF INTEREST
# RS = ["{0:.1f}".format(df.columns[wn]) for wn in w]
# labels = ['baseline', 'Unknown', 'beta-carotene', 'CH group']  # enter name of component that corresponds to peaks identified with w
#
# fig, ax = plt.subplots(1, figsize=(7,5))
# plot_position = [0.125,0.10,0.82,0.85]
# ax.set_position(plot_position)
# plotBox = ax.get_position()
# ax.set_position([plotBox.x0, plotBox.y0, plotBox.width*0.6, plotBox.height])
# lines = ax.plot(baselined[mask][:,w])
# ax.legend(lines, [label+" ("+str(RS)+" cm"+r"$^{-1}$)" for label, RS in zip(labels,RS)],
#            loc='upper center', bbox_to_anchor=(1.4, 1.0))
# ax.set_xlabel('Line-scan position')
# ax.set_ylabel('Relative Intensity')
#
#
# #plt.savefig(basefile+"_linescan_"+str(x0)+'_'+str(x1)+'_'+str(y0)+'_'+str(y1)+".png",dpi=600)
# cube[mask][1][1]
# cube[mask].max()
