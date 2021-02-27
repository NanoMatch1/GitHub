from GRBLcommands import*
import math
# initializeGRBL()

x = abs(-50)
print(x)

list1 = [(0, 0), (25, 0), (50, 0), (75, 0), (100, 0)]
currentPos = (0, 0)


mapStart = (0, 0)
mapFinish = (50,100)
mapRes = 0.5
acquisitionTime = 180
filename = 'map'

pos = (3,56)
xScan = np.arange(mapStart[0], mapFinish[0], mapRes)
yScan = np.arange(mapStart[1], mapFinish[1], mapRes)

filename = filename+r' #{}x{}#{}s#({},{})#'.format(len(xScan), len(yScan), acquisitionTime, str(pos[0]), str(pos[1]))
print(filename)
print(len(xScan))
print(len(yScan))
# print(p)
# mapArray = [(xScan[idx], yScan[idx]) for idx in list(range(len(xScan)))]
#
# mapArray = np.array(mapArray)


for index, x in enumerate(xScan):
    col = []
    for idx, y in enumerate(yScan):
        col.append((x, y))

        # if (index+1)%2 == 0:
        #     col = col[-1]
    # col = np.array(col)
    if (index+1)%2 == 0:
        col = col[::-1]

    try:
        mapList.append(col)
    except NameError:
        mapList = col
    # try:
    #     mapArray = np.vstack((mapArray, col))
    # except NameError:
    #     mapArray = np.array(col)

for row in mapList:
    for x in row:
        print(x)

print(max(mapList))
