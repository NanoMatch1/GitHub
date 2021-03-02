from ipywidgets import *
# import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
import matplotlib.patches as patches
import os

import sys
sys.path.insert(0, 'C:/GitHub/Raman/Raman')
from Modular_Raman_Analyser import *
from Header_Finder import *


#set the directory to the desired data directory
#Hint: Right-click in the address bar in File Explorer and copy the address
# os.chdir(r'2D_map_data')

fileDir = r"C:\Users\sjbro\OneDrive - Massey University\Sam\PhD\Data\Raman\2021\3-2-21 Maps and scans\Calibration tests\Line 2x36 series"
# fileDir = r'C:\OneDrive\OneDrive - Massey University\Sam\PhD\Data\Raman\Collabs\DaveMcMorran\09-28-20\785'
dataDir = r'data\{}'.format(fileDir)

#check the current directory.
os.chdir(dataDir)


#dir_path = "./data/" #Path to data directory
basefile = "Trimyristin beta-in-shell A" # Base file name
ext = ".dat" # Extension

filenames = [basefile + "_" + str(i) + ext for i in range(1,2501)]
df = pd.concat([pd.read_table(f, delim_whitespace=True, index_col=0, header=None, names=[None, str(i+1)]).transpose() for i, f in enumerate(filenames)])
df.head(10)

#
# cube = df.values.reshape(50,50,1600).transpose(1,0,2)
# print(cube.shape)
#
# print('Number of spectra =',cube.shape[0]*cube.shape[1])

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


# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# img = ax.imshow(baselined[:,:,1194], interpolation='bilinear', cmap='hot')
# color_bar = plt.colorbar(img)
#
# def update_im(idx):
#     img.set_data(baselined[:,:,idx-1])
#     fig.canvas.draw()
#     return "Wave number: " + str(df.columns[(idx-1)+lp])
# interact(update_im, idx=(1,baselined.shape[2],1));



# # ENTER WAVE NUMBER INDEX OF INTEREST
# w = 1192
#
# # ENTER COORDINATES HERE
# x0 = 22
# y0 = 5
# x1 = 22
# y1 = 43
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
