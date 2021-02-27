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
        elif command[0] == "X" or command[0] == "x" or command[0] == "Y" or command[0] == "y":
            print("triggered")
            return (command, "move")
            break
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


def main_loop(s, currentPos, commandDict, commandList):
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
                baseFilename = str(input("Enter filename:\n"))
            if command == 'traveltime':
                travelTime = input("Enter new travel time for scans in seconds:\n")
            if command == 'sethome':
                home = currentPos
            if command == 'gohome':
                print('moving to '+str(home))
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
                input("Press 'Enter' to run linescan. Close console to quit.")
                return lineScanList, acquisitionTime
                break

            if command == 'map':
                mapStart, mapFinish = None, None
                print('Preparing for 2D map:')
                while True:
                    command, type = get_command(commandList)
                    if type == 'move':
                        currentPos = interpret_move(currentPos, command)
                        move_absolute(currentPos)
                    if command == 'start':
                        mapStart = currentPos
                        print("Start position entered:", lineStart)
                    if command == 'finish':
                        mapFinish = currentPos
                        print("Finish position entered:", lineFinish)
                    if mapStart and mapFinish:
                        break
                while True:
                    mapRes = input("Enter scan resolution in microns:\n")
                    try:
                        lineScanRes = float(mapRes)
                        break
                    except:
                        print("Number of points not recognised - please enter an interger number.")

                xScan = np.arange(mapStart[0], mapFinish[0], mapRes)
                yScan = np.arange(mapStart[1], mapFinish[1], mapRes)

                filename = filename+r' #{}x{}#{}s#({},{})#'.format(len(xScan), len(yScan), acquisitionTime, str(pos[0]), str(pos[1]))

                for index, x in enumerate(xScan):
                    col = []
                    for y in yScan:
                        col.append((x, y))
                    if (index+1)%2 == 0:
                        col = col[::-1]
                    try:
                        mapList.append(col)
                    except NameError:
                        mapList = col

                while True:
                    acquisitionTime = input("Enter acquisition time per frame (seconds):\n")
                    try:
                        acquisitionTime = float(acquisitionTime)
                        break
                    except:
                        print("Acquisition time value not recognised. Please enter an number.")

                print("Map ready:")
                print(mapList)
                print("Returning to start position.")
                currentPos = interpret_move(currentPos, mapList[0])
                move_absolute(mapList[0])
                input("Press 'Enter' to run linescan. Close console to quit.")
                return mapList, acquisitionTime
                break



def initializeGRBL():
    # Open grbl serial port
    s = serial.Serial('COM6',115200)

    # Wake up grbl
    s.write(str.encode("hello"))
    time.sleep(2)   # Wait for grbl to initialize
    s.flushInput()  # Flush startup text in serial input

    # Stream g-code to grbl
    s.write(str.encode('G90 F1000'+'\n'))
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print('Moving in absolute coordinates : ' + str(grbl_out.strip()))

    commandDict = {"quit": "quit", "sethome": "sethome"}
    commandList = ['quit','sethome','linescan', 'gohome', 'start', 'finish', 'acquire', 'traveltime', 'filename']
    currentPos = (0,0)

    return s, currentPos, commandDict, commandList


auto = Automation(True, List[String]())

experiment = auto.LightFieldApplication.Experiment
acquireCompleted = AutoResetEvent(False)

experiment.Load("Automation")
experiment.ExperimentCompleted += experiment_completed
# experiment.SetValue(SpectrometerSettings.gratingSelected, '[500nm, 1200][1][0]')
# InitializeFileParams()


# exposures = [50, 100]
# specPositions = [560, 435, 546]
baseFilename = "f1Linescan"
travelTime = 2
inp = input("Change settings, then press <Enter> to continue")

s, currentPos, commandDict, commandList = initializeGRBL()


while True:
    scanList, acquisitionTime = main_loop(s, currentPos, commandDict, commandList)
    experiment.SetValue(CameraSettings.ShutterTimingExposureTime, acquisitionTime*1000)

    for pos in scanList:
        name = str(baseFilename)+'#{}'.format(str(pos))
        experiment.SetValue(ExperimentSettings.FileNameGenerationBaseFileName, name)
        print('setting exp params')
        print('Moving to {}'.format(pos))
        # currentPos, travelTime = update_pos(pos)
        # travelTime = (float(max(abs(currentPos[0]-pos[0]), abs(currentPos[1]-pos[1]))))*.1
        # if travelTime <= 1:
        #     travelTime = 1
        move_absolute(pos)
        currentPos = pos
        # time.sleep(acquisitionTime)
        # print("Linescan complete")
        print('sleeping for travel time: ', travelTime)
        time.sleep(travelTime)
        AcquireAndLock(baseFilename)
    print('#'*100, '\nScan complete! Moving to starting position:', scanList[0])
    move_absolute(scanList[0])
    currentPos = scanList[0]
