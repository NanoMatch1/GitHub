import numpy as np
def pause(text = '...'):
    input(text)

numPlates = input("Enter number of wellplates (1 or 2)")

xArray = [x*5 for x in range(7)]
yArray = [y*5 for y in range(3)]

wellDict = {}

for row, y in enumerate(yArray):
    if row == 0:
        label = 'A'
    if row == 1:
        label = 'B'
    if row == 2:
        label = 'C'

    for col, x in enumerate(xArray):
        wellDict[(x, y)] = '{}{}'.format(label, col+1)

print(wellDict)
pause()



for idx, y in enumerate(yArray):
    if idx >= 1:
        xArray = xArray[::-1]
    for x in xArray:
        print(wellDict[(x, y)])
        pause()

if numPlates == '2':
    wellDict = {}
    for row, y in enumerate(yArray):
        if row == 0:
            label = 'xA'
        if row == 1:
            label = 'xB'
        if row == 2:
            label = 'xC'

        for col, x in enumerate(xArray):
            wellDict[(x, y+25)] = '{}{}'.format(label, col+1)

    print(wellDict)

    for idx, y in enumerate(yArray):
        y += 25
        xArray = xArray[::-1]
        for x in xArray:
            print(wellDict[(x, y)])
            pause()
