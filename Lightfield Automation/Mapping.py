# Import the .NET class library
import clr

# Import python sys module
import sys

# Import os module
import os, glob, string

# Import System.IO for saving and opening files
from System.IO import *
from System.Threading import AutoResetEvent
# Import c compatible List and String
from System import String
from System.Collections.Generic import List

# config file save
import json

# Add needed dll references
sys.path.append(os.environ['LIGHTFIELD_ROOT'])
sys.path.append(os.environ['LIGHTFIELD_ROOT']+"\\AddInViews")
clr.AddReference('PrincetonInstruments.LightFieldViewV5')
clr.AddReference('PrincetonInstruments.LightField.AutomationV5')
clr.AddReference('PrincetonInstruments.LightFieldAddInSupportServices')

# PI imports
from PrincetonInstruments.LightField.Automation import Automation
from PrincetonInstruments.LightField.AddIns import ExperimentSettings
from PrincetonInstruments.LightField.AddIns import DeviceType
from PrincetonInstruments.LightField.AddIns import SpectrometerSettings
from PrincetonInstruments.LightField.AddIns import CameraSettings

#GRBL import
# from GRBLcommands import*

def pause():
    input("Press Enter to continue...")

def experiment_completed(sender, event_args):
    print("...Acquisition Completed")
    acquireCompleted.Set()

def InitializeFileParams():
        # Set the base file name
        experiment.SetValue(
            ExperimentSettings.FileNameGenerationBaseFileName,
            Path.GetFileName(filename))

        # Option to Increment, set to false will not increment
        experiment.SetValue(
            ExperimentSettings.FileNameGenerationAttachIncrement,
            False)

        # Option to add date
        experiment.SetValue(
            ExperimentSettings.FileNameGenerationAttachDate,
            False)

        # Option to add time
        experiment.SetValue(
            ExperimentSettings.FileNameGenerationAttachTime,
            False)


def AcquireAndLock(name):
    print("Acquiring...", end="")
    # name += "add values for map locations here"
    # experiment.SetValue(ExperimentSettings.FileNameGenerationBaseFileName, name)
    experiment.Acquire()
    acquireCompleted.WaitOne()

# GRBL commands
import serial
import time
import numpy as np
import matplotlib.pyplot as plt

def send_gcode(code, delay = None):
    if isinstance(code, str):
        print('Sending: ' + str(code))
        s.write(str.encode(str(code)+'\n'))
        grbl_out = s.readline() # Wait for grbl response with carriage return
        print(' : ' + str(grbl_out.strip()))
    elif isinstance(code, list):
        for item in code:
            print('Sending: ' + str(item))
            s.write(str.encode(str(item)+'\n'))
            grbl_out = s.readline() # Wait for grbl response with carriage return
            print(' : ' + str(grbl_out.strip()))
            if delay:
                time.sleep(delay)
    else:
        print('Incorrect code format: please enter gcode as a string or list of strings.')

def move_absolute(pos):
    # send_gcode('G90')
    if isinstance(pos, tuple):
        xPos, yPos = pos
        send_gcode('G1 X'+str(xPos)+' Y'+str(yPos))
        # currentPos = update_pos(currentPos, pos)
    if isinstance(pos, str):
        if 'x' in pos or 'X' in pos:
            xPos = pos.lstrip('xX')
            # currentPos = update_pos_x(currentPos, pos)
        if 'y' in pos or 'Y' in pos:
            yPos = pos.lstrip('yY')
            # currentPos = update_pos_y(currentPos, pos)

def move_relative(pos):
    send_gcode('G91')
    if isinstance(pos, tuple):
        xPos, yPos = pos
        send_gcode('G1 X'+str(xPos)+' Y'+str(yPos))
        currentPos = update_pos(currentPos, pos)
    if isinstance(pos, str):
        if 'x' in pos or 'X' in pos:
            xPos = pos.lstrip('xX')
            currentPos = update_pos_x(currentPos, pos)
        if 'y' in pos or 'Y' in pos:
            yPos = pos.lstrip('yY')
            currentPos = update_pos_y(currentPos, pos)


def update_pos(currentPos, posData):
    if isinstance(posData, tuple):
        currentPos = (float(currentPos[0])+float(posData[0]), float(currentPos[1])+float(posData[1]))
    print("New position:", str(currentPos))
    # longAxis = max(abs(posData[0], abs(posData[1])))
    # travelTime = float(longAxis)*.08
    # if travelTime <= 1:
    #     travelTime = 1
    return currentPos

def update_pos_x(currentPos, pos):
    currentPos = (float(currentPos[0])+float(pos), float(currentPos[1]))
    print("New position:", str(currentPos))
    return currentPos

def update_pos_y(currentPos, pos):
    currentPos = (float(currentPos[0]), float(currentPos[1])+float(pos))
    print("New position:", str(currentPos))
    return currentPos

def set_home(currentPos, pos = None):
    homePos = currentPos
    if pos:
        homePos = pos
    return homePos

def prep_linescan(start, finish, increment):
    posHome = start
    posFinish

def get_command(commandList):
    while True:
        command = str(input("Enter command:\n"))
        # if str(command) in commandDict.keys():
        if command in commandList:
            return (command, "command")
        else:
            try:
                if command[0] == "X" or command[0] == "x" or command[0] == "Y" or command[0] == "y":
                    print("triggered")
                    return (command, "move")
                    break
            except:
                pass

            if command == "quit":
                break
            else:
                print(str(command)+": Command not recognised")
                continue

def interpret_move(currentPos, command):
    xPos, yPos = False, False
    for x in ["x", "X"]:
        if x in command:
            xIndex = command.index(x)
            xPos = True
    for y in ["y", "Y"]:
        if y in command:
            yIndex = command.index(y)
            yPos = True

    if xPos == True and yPos == True:
        xPos = command[xIndex+1:yIndex]
        yPos = command[yIndex+1:]
        # print("new pos: ("+xPos+',', yPos+")")
        currentPos = update_pos(currentPos, (xPos, yPos))
    if xPos == True and yPos == False:
        xPos = command[xIndex+1:]
        # print("new pos: X", xPos)
        currentPos = update_pos_x(currentPos, xPos)
    if xPos == False and yPos == True:
        yPos = command[yIndex+1:]
        # print("new pos: Y", yPos)
        currentPos = update_pos_y(currentPos, yPos)

    return(currentPos)

def runLinescan(lineScanList, acquisitionTime):
    for pos in lineScanList:
        currentPos = pos
        move_absolute(pos)
        time.sleep(acquisitionTime)
    print("Linescan complete")
    time.sleep(10)
    quit()


def main_loop(s, currentPos, commandDict, commandList, filename = 'filename', currentMode = "raman"):
    acquireTime = None

    try:
        home
    except:
        home = currentPos
    while True:
        command, type = get_command(commandList)
        if type == "move":
            currentPos = interpret_move(currentPos, command)
            move_absolute(currentPos)

        if type == "command":
            if command == 'filename':
                filename = str(input("Enter filename:\n"))
            if command == 'traveltime':
                travelTime = input("Enter new travel time for scans in seconds:\n")
            if command == 'sethome':
                home = currentPos
            if command == 'gohome':
                print('moving to '+str(home))
            if command == 'ramanmode':
                currentMode = ramanMode(currentMode)
            if command == 'imagemode':
                currentMode = imageMode(currentMode)
            if command == 'adjustpower':
                adjustPower()
            if command == 'quit':
                s.close()
            if command == 'gcode':
                command = input('Enter gcode to send. WARNING - DONT BREAK SOMETHING')
                send_gcode(str(command))
            if command == 'light':
                while True:
                    pwr = input('Enter power from 0 to 150.')
                    try:
                        pwr = int(pwr)
                        if pwr <= 255 and pwr >= 0:
                            break
                    except:
                        pass
                lightOn(pwr)
            if command == 'linescan':
                lineStart, lineFinish = None, None
                print('Preparing for linescan:')
                while True:
                    command, type = get_command(commandList)
                    if type == 'move':
                        currentPos = interpret_move(currentPos, command)
                        move_absolute(currentPos)
                    if command == 'start':
                        lineStart = currentPos
                        print("Start position entered:", lineStart)
                    if command == 'finish':
                        lineFinish = currentPos
                        print("Finish position entered:", lineFinish)

                    if command == 'gcode':
                        command = input('Enter gcode to send. WARNING - DONT BREAK SOMETHING')
                        send_gcode(str(command))
                    if command == 'quit':
                        s.close()
                    if command == 'ramanmode':
                        currentMode = ramanMode(currentMode)
                    if command == 'imagemode':
                        currentMode = imageMode(currentMode)
                    if command == 'adjustpower':
                        currentMode = adjustPower()
                    if command == 'light':
                        while True:
                            pwr = input('Enter power from 0 to 150.')
                            try:
                                pwr = int(pwr)
                                if pwr <= 255 and pwr >= 0:
                                    break
                            except:
                                pass
                        lightOn(pwr)

                    if lineStart and lineFinish:
                        break
                while True:
                    lineScanRes = input("Enter number of points on line to scan:\n")
                    try:
                        lineScanRes = int(lineScanRes)
                        break
                    except:
                        print("Number of points not recognised - please enter an interger number.")
                xInt = (lineFinish[0] - lineStart[0])/(lineScanRes-1)
                yInt = (lineFinish[1] - lineStart[1])/(lineScanRes-1)
                lineScanX = [lineStart[0]+(xInt*index) for index in list(range(lineScanRes))]
                lineScanY = [lineStart[1]+(yInt*index) for index in list(range(lineScanRes))]
                # print(lineScanX)
                # print(lineScanY)
                lineScanList = [(lineScanX[idx], lineScanY[idx]) for idx in list(range(len(lineScanX)))]

                while True:
                    acquisitionTime = input("Enter acquisition time per frame (seconds):\n")
                    try:
                        acquisitionTime = float(acquisitionTime)
                        break
                    except:
                        print("Acquisition time value not recognised. Please enter an number.")

                print("Linescan ready:")
                print(lineScanList)
                print("Returning to start position.")
                currentPos = interpret_move(currentPos, lineScanList[0])
                move_absolute(lineScanList[0])
                while True:
                    com3 = input("Press 'Enter' to run linescan, or enter a command. Close console to quit.\n")
                    if command == 'gcode':
                        send_gcode(str(command))

                    if com3 == 'ramanmode':
                        currentMode = ramanMode(currentMode)
                    if com3 == 'imagemode':
                        currentMode = imageMode(currentMode)
                    if com3 == 'adjustpower':
                        currentMode = adjustPower()
                    if command == 'light':
                        while True:
                            pwr = input('Enter power from 0 to 150.')
                            try:
                                pwr = int(pwr)
                                if pwr <= 255 and pwr >= 0:
                                    break
                            except:
                                pass
                        lightOn(pwr)
                    if com3 == '':
                        break
                if currentMode == 'image':
                    currentMode == ramanMode(currentMode)
                return lineScanList, acquisitionTime, filename

            if command == 'map':
                mapStart, mapFinish = None, None
                print('Preparing for 2D map:')
                while True:
                    command, type = get_command(commandList)
                    if type == 'move':
                        currentPos = interpret_move(currentPos, command)
                        move_absolute(currentPos)
                    if command == 'filename':
                        filename = str(input("Enter filename:\n"))
                    if command == 'start':
                        mapStart = currentPos
                        print("Start position entered:", mapStart)
                    if command == 'finish':
                        mapFinish = currentPos
                        print("Finish position entered:", mapFinish)

                    if command == 'gcode':
                        command = input('Enter gcode to send. WARNING - DONT BREAK SOMETHING')
                        send_gcode(str(command))


                    if command == 'quit':
                        s.close()
                    print('currentMode =', currentMode)
                    if command == 'ramanmode':
                        currentMode = ramanMode(currentMode)
                    if command == 'imagemode':
                        currentMode = imageMode(currentMode)
                    if command == 'adjustpower':
                        currentMode = adjustPower()
                    if command == 'light':
                        while True:
                            pwr = input('Enter power from 0 to 150.')
                            try:
                                pwr = int(pwr)
                                if pwr <= 255 and pwr >= 0:
                                    break
                            except:
                                pass
                        lightOn(pwr)

                    if mapStart and mapFinish:
                        break
                while True:
                    print('map size is '+str(mapFinish[0]-mapStart[0])+' x '+str(mapFinish[1]-mapStart[1]))

                    mapRes = input("Enter scan resolution in microns:\n")
                    try:
                        resolution = float(mapRes)
                        break
                    except:
                        print("Number not recognised - please enter a number.")


                xArray, yArray = generate_2D_arrays(mapStart, mapFinish, resolution)

                while True:
                    acquisitionTime = input("Enter acquisition time per frame (seconds):\n")
                    try:
                        acquisitionTime = float(acquisitionTime)
                        break
                    except:
                        print("Acquisition time value not recognised. Please enter an number.")



                print("Map ready:")
                runTime = len(xArray[:, 0])*len(xArray[0, :])*acquisitionTime
                # print("Calculated run time:"
                print("Returning to start position.")
                mapHome = (xArray[0, 0], yArray[0, 0])
                mapEndPos = (xArray[-1, -1], yArray[-1, -1])
                currentPos = interpret_move(currentPos, mapHome)
                move_absolute(mapHome)

                filename = filename+r' #{}x{}#{}s#'.format(len(xArray[0, :]), len(yArray[:, 0]), acquisitionTime)
                print('Estimated run time: {} sec, or \n{} min, or \n{} hours'.format(runTime, runTime/60, runTime/3600))
                while True:
                    com3 = input("Press 'Enter' to run map, or enter a command. Close console to quit.\n")
                    if com3 == 'show':
                            move_absolute(mapHome)
                            move_absolute(mapEndPos[0], mapHome[0])
                            move_absolute(mapEndPos)
                            move_absolute(mapHome[0], mapEndPos[1])
                            move_absolute(mapHome)
                    if com3 == 'ramanmode':
                        currentMode = ramanMode(currentMode)
                    if com3 == 'imagemode':
                        currentMode = imageMode(currentMode)
                    if com3 == 'adjustpower':
                        currentMode = adjustPower()
                    if command == 'gcode':
                        command = input('Enter gcode to send. WARNING - DONT BREAK SOMETHING')
                        send_gcode(str(command))
                    if command == 'light':
                        while True:
                            pwr = input('Enter power from 0 to 150.')
                            try:
                                pwr = int(pwr)
                                if pwr <= 255 and pwr >= 0:
                                    break
                            except:
                                pass
                        lightOn(pwr)

                    if com3 == '':
                        break
                if currentMode == 'image':
                    currentMode == ramanMode(currentMode)
                return xArray, yArray, acquisitionTime, filename

def adjustPower(power = None):
    if power =='max':
        s.write(str.encode('T1\n'))
        grbl_out = s.readline() # Wait for grbl response with carriage return
        s.write(str.encode('G1 E5\n'))
        grbl_out = s.readline() # Wait for grbl response with carriage return
        return
    if power == 'min':
        s.write(str.encode('T1\n'))
        grbl_out = s.readline() # Wait for grbl response with carriage return
        s.write(str.encode('G1 E-5\n'))
        grbl_out = s.readline() # Wait for grbl response with carriage return
        return
    elif power != 'min' or power != 'max':
        while True:
            power = input('Enter power (-6 to 6)\n')
            try:
                power = float(power)
                s.write(str.encode('T1\n'))
                grbl_out = s.readline() # Wait for grbl response with carriage return
                s.write(str.encode('G1 E'+str(power)+'\n'))
                grbl_out = s.readline() # Wait for grbl response with carriage return
                break
            except:
                power = input('Incorrect value - please enter a float.\n')
    return

def lightOn(power = 255):
    s.write(str.encode('M106 P2 S{}\n'.format(power)))
    grbl_out = s.readline() # Wait for grbl response with carriage return

def ramanMode(currentMode):
    if currentMode == 'image':
        s.write(str.encode('T0\n'))
        grbl_out = s.readline() # Wait for grbl response with carriage return
        s.write(str.encode('G1 E-120\n'))
        grbl_out = s.readline() # Wait for grbl response with carriage return
        adjustPower(power = 'max')
    else:
        OVR = input('Error - already in Raman mode. Type "OVERWRITE" to change anyway, or enter to continue.')
        if OVR == 'OVERWRITE':
            s.write(str.encode('T0\n'))
            grbl_out = s.readline() # Wait for grbl response with carriage return
            s.write(str.encode('G1 E-120\n'))
            grbl_out = s.readline() # Wait for grbl response with carriage return
            adjustPower(power = 'max')
    currentMode = "raman"
    lightOn(0)
    return currentMode

def imageMode(currentMode):
    if currentMode == 'raman':
        s.write(str.encode('T0\n'))
        grbl_out = s.readline() # Wait for grbl response with carriage return
        s.write(str.encode('G1 E120\n'))
        grbl_out = s.readline() # Wait for grbl response with carriage return
        adjustPower(power = 'min')
    else:
        OVR = input('Error - already in Image mode. Type "OVERWRITE" to change anyway, or enter to continue.')
        if OVR == 'OVERWRITE':
            s.write(str.encode('T0\n'))
            grbl_out = s.readline() # Wait for grbl response with carriage return
            s.write(str.encode('G1 E120\n'))
            grbl_out = s.readline() # Wait for grbl response with carriage return
            adjustPower(power = 'min')
    currentMode = "image"
    lightOn()
    return currentMode

def initializeGRBL(motorSpeed = 1000, comPort = 'COM8'):
    # Open grbl serial port
    s = serial.Serial(comPort ,115200)

    # Wake up grbl
    # s.write(str.encode("hello"))
    time.sleep(2)   # Wait for grbl to initialize
    s.flushInput()  # Flush startup text in serial input

    # Stream g-code to grbl
    s.write(str.encode('G90 F{}'.format(motorSpeed)+'\n'))
    grbl_out = s.readline() # Wait for grbl response with carriage return
    # s.write(str.encode('M350 E256:1\n')) # sets microstepping of power controller to 1 # NOTE: redundant if config file changed
    # grbl_out = s.readline() # Wait for grbl response with carriage return
    print('Moving in absolute coordinates : ' + str(grbl_out.strip()))

    commandDict = {"quit": "quit", "sethome": "sethome"}
    commandList = ['light','gcode','quit','sethome','linescan', 'gohome', 'start', 'finish', 'acquire', 'traveltime', 'filename', 'map', 'imagemode', 'ramanmode', 'adjustpower']


    currentPos = (0,0)
    s.write(str.encode('G92 X0 Y0 Z0 E0\n')) # sets absolute coordinates for all axes to zero
    grbl_out = s.readline() # Wait for grbl response with carriage return
    return s, currentPos, commandDict, commandList

def generate_2D_arrays(start, finish, resolution):
    import math

    deltaX = finish[0]-start[0]
    deltaY = finish[1]-start[1]

    if deltaX > 0:
        xStep = resolution
    if deltaX < 0:
        xStep = resolution*-1

    if deltaY > 0:
        yStep = resolution
    if deltaY < 0:
        yStep = resolution*-1

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


    return xArray, yArray




# '''LightField Section'''
auto = Automation(True, List[String]())

experiment = auto.LightFieldApplication.Experiment
acquireCompleted = AutoResetEvent(False)

experiment.Load("Automation")
experiment.ExperimentCompleted += experiment_completed

comPort = 'COM8'
filename = "f5map1"
motorSpeed = 500
travelTime = 2
while True:
    currentMode = input('Enter current mode: "raman" or "image":\n')
    if currentMode == "raman" or currentMode =='image':
        break
    else:
        print('Error - please enter "Raman" or "Image".')

inp = input("Change directory and run tests, then press <Enter> to continue")

s, currentPos, commandDict, commandList = initializeGRBL(motorSpeed, comPort)


while True:
    scanType = None
    scanType = input('Specify collection type: "line", or "map".')
    if scanType == 'line':

        scanList, acquisitionTime, filename = main_loop(s, currentPos, commandDict, commandList, filename, currentMode = currentMode)
        experiment.SetValue(CameraSettings.ShutterTimingExposureTime, acquisitionTime*1000)
        np.savetxt('ScanLists/{}_list.meta'.format(filename), (scanList), delimiter=',', fmt = '%s')

        for idx, pos in enumerate(scanList):
            name = str(filename)+'#[{}]#'.format(str(idx))
            experiment.SetValue(ExperimentSettings.FileNameGenerationBaseFileName, name)
            print('setting exp params')
            print('Moving to {}'.format(pos))
            move_absolute(pos)
            currentPos = pos
            print('sleeping for travel time: ', travelTime)
            time.sleep(travelTime)
            AcquireAndLock(filename)
        print('#'*100, '\nScan complete! Moving to starting position:', scanList[0])
        move_absolute(scanList[0])
        currentPos = scanList[0]

    if scanType == 'map':
            # try:
        xArray, yArray, acquisitionTime, filename = main_loop(s, currentPos, commandDict, commandList, filename, currentMode)

        posDict = {}
        for i in list(range(len(xArray[:, 0]))):
            for j in list(range(len(xArray[0, :]))):
                pos = (xArray[i, j], yArray[i, j])
<<<<<<< HEAD
                posDict[str((j,i))] = '{},{}'.format(str(pos[0]), str(pos[1]))
=======

                posDict[(i,j)] = '({},{})'.format(str(pos[0]), str(pos[1]))
>>>>>>> 08f04113ccd90076cf1d89da2983aca3f60994c9

        with open('ScanLists/{}_list.json'.format(filename), 'w') as jsonfile:
            json.dump(posDict, jsonfile)

        experiment.SetValue(CameraSettings.ShutterTimingExposureTime, acquisitionTime*1000)
        pause()
        for i in list(range(len(xArray[:, 0]))):
            for j in list(range(len(xArray[0, :]))):
                pos = (xArray[i, j], yArray[i, j])
                name = str(filename)+'#({},{})#'.format(str(j), str(i))
                print(pos)
                experiment.SetValue(ExperimentSettings.FileNameGenerationBaseFileName, name)

                print('Moving to ({}, {})'.format(pos[0], pos[1]))
                print('sleeping for travel time: ', travelTime)
                move_absolute(pos)
                currentPos = pos
                time.sleep(travelTime)
                AcquireAndLock(filename)
            print('linebreak reset. Sleeping for 10 seconds')
            try:
                pos = (xArray[i, j-j], yArray[i, j-j])
                move_absolute(pos)
                currentPos = pos
                pos = (xArray[i+1, j-j], yArray[i+1, j-j])
                move_absolute(pos)
                currentPos = pos
                time.sleep(10)
            except IndexError:
                pass
        print('#'*100, '\nScan complete! Moving to starting position:', str(xArray[0, 0])+', '+str(yArray[0, 0]))
        pos = (xArray[0, 0], yArray[0, 0])
        move_absolute(pos)
        currentPos = pos
            # except:
                # continue
    # experiment.SetValue(CameraSettings.ShutterTimingExposureTime, acquisitionTime*1000)
