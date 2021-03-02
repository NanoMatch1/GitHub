import numpy as np
import math
import csv
import os


start = (-0, -0)
finish = (-10, 30)

res = 5

def pause():
    input('Pause')



def generate_2D_arrays(start, finish, resolution):
    deltaX = finish[0]-start[0]
    deltaY = finish[1]-start[1]

    if deltaX > 0:
        xStep = res
    if deltaX < 0:
        xStep = res*-1

    if deltaY > 0:
        yStep = res
    if deltaY < 0:
        yStep = res*-1

    print(xStep)
    lenX = math.floor(abs(deltaX/xStep))
    lenY = math.floor(abs(deltaY/yStep))

    xScan = [start[0]+(xStep*index) for index in list(range(lenX+1))]
    yScan = [start[1]+(yStep*index) for index in list(range(lenY+1))]

    print('xScan:', xScan)
    print('yScan:', yScan)

    if len(xScan) == 0 or len(yScan)== 0:
        print('resolution error - please enter appropriate resolution for image size')

    for idx, x in enumerate(xScan):
        rowX = []
        rowY = []
        for y in yScan:
            rowX.append(x)
            rowY.append(y)

        try:
            xArray = np.column_stack((xArray, rowX))
            yArray = np.column_stack((yArray, rowY))
        except NameError:
            xArray = np.array(rowX).astype(float)
            yArray = np.array(rowY).astype(float)


    print('LenX', len(xScan), 'lenY', len(yScan))
    return xArray, yArray


def run_2D_map(xArray, yArray, acquisitionTime):
    for i in list(range(len(xArray))):
        for j in list(range(len(yArray))):
            print(xArray[i, j], yArray[i, j])
        print('linebreak reset')


xArray, yArray = generate_2D_arrays(start, finish, res)

print('X')
print(xArray)
print('-----------------------------------')
print('Y')
print(yArray)
# pause()
for i in list(range(len(xArray[:, 0]))):
    for j in list(range(len(xArray[0, :]))):
        print(xArray[i, j], yArray[i, j])
    print('linebreak reset')

print('LenX col', len(xArray[0, :]))
print('LenX row', len(xArray[:,0]))
# print('start')
# print(xArray[0,0], yArray[0,0])
# print('finish')
# print(xArray[-1, -1], yArray[-1,-1])
#
# print(len(xArray[0, :]))
posDict = {}
print([xArray, yArray])
for i in list(range(len(xArray[:, 0]))):
    for j in list(range(len(xArray[0, :]))):
        pos = (xArray[i, j], yArray[i, j])
        posDict[(i,j)] = pos
# print([posDict])
# mapEndPos = (xArray[-1, -1], yArray[-1, -1])
#

dir = 'Lightfield Automation/'
files = [file for file in os.listdir('Lightfield Automation') if file.endswith('.json')]
# print('jh')
# for file in files:
#     if 'quick' in file:
#         with open(dir+file, mode='r', newline = ',') as csv_file:
#             csv_reader = csv.DictReader(csv_file)
#             for row in csv_reader:
#                 print(row)
import json

with open(dir+files[0], 'r') as fp:
    data = json.load(fp)

print(data['(0, 0)'])
# print(data)
            # line_count = 0
            # for row in csv_reader:
            #     if line_count == 0:
            #         print(f'Column names are {", ".join(row)}')
            #         line_count += 1
            #     print(f'\t{row["name"]} works in the {row["department"]} department, and was born in {row["birthday month"]}.')
            #     line_count += 1
            # print(f'Processed {line_count} lines.')
# print('mapEnd[0]', mapEndPos[1])
# print(mapArray[0, 0])
# val = tuple(mapArray[0, 0])
# print(val[0])
# lineScanY = [lineStart[1]+(yInt*index) for index in list(range(lineScanRes))]


# print(lenX, lenY)
# pause()

# xScan = np.arange(start[0], finish[0], res)
# if xDir == 'pos':
#     xScan = np.arange(start[0], finish[0], res)
#
# elif xDir == 'neg':
#     xScan = (np.arange(abs(start[0]), abs(finish[0]), res))*-1

# for

# print(xScan)

# xInt = float((finish[0]-start[0])/res)
# yInt = float((finish[1]-start[1])/res)
# # print('xInt:yInt', math.floor(xInt), math.floor(yInt))
#
# xScan = []
# yScan = []
# idx = 1
# while abs(xInt*idx) < abs(finish[0]):
#     xScan.append(xInt*idx)
#     idx += 1
# idx = 1
#
# while abs(yInt*idx) < abs(finish[1]):
#     yScan.append(yInt*idx)
#     idx += 1
#
#
# print(xScan, yScan)


# # xScan = [start[0]+(xInt*index) for index in list(range(xInt))]
# print(list(range(math.floor(xInt))))
# print(list(range(math.floor(yInt))))
# for x in list(range(math.floor(xInt))):
#     print(x)
#     for y in list(range(math.floor(yInt))):
#         pos = (x, y)
#         print(x, y)
#         pause()
#         try:
#             row.append(pos)
#         except NameError:
#             row = [pos]
#     try:
#         mapArray = np.vstack((mapArray, row))
#     except NameError:
#         mapArray = np.array(row)
#
# print(mapArray)
# # print(xScan)
#
# print(xInt, yInt)
