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
                print(lineScanX)
                print(lineScanY)
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
                break

    return lineScanList, acquisitionTime
                # runLinescan(lineScanList, acquisitionTime)





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
    commandList = ['quit','sethome','linescan', 'gohome', 'start', 'finish', 'acquire']
    currentPos = (0,0)

    return s, currentPos, commandDict, commandList
#
#
# s, currentPos, commandDict, commandList = initializeGRBL()
# main_loop(currentPos, commandDict, commandList)
#
# # Wait here until grbl is finished to close serial port and file.
# input("  Press <Enter> to exit and disable grbl.")
#
# # Close file and serial port
# # f.close()
# s.close()



# Open g-code file
# f = open('gcodetest.gcode','r');
#


#
#
# lineGcode = [1,2,3,4,5]

# #
# for xPos in lineGcode:
#     print('Sending: ' + str(xPos))
#     s.write(str.encode('G0 X'+str(xPos)+'\n'))
#     grbl_out = s.readline() # Wait for grbl response with carriage return
#     print(' : ' + str(grbl_out.strip()))
#     time.sleep(acquireTime)
#     # s.write(str.encode('G4 P'+str(acquireTime)+'\n'))
#     # grbl_out = s.readline() # Wait for grbl response with carriage return
#     # print(' : ' + str(grbl_out.strip()))
#
#
#
#
# # Wait here until grbl is finished to close serial port and file.
# input("  Press <Enter> to exit and disable grbl.")
#
# # Close file and serial port
# f.close()
# s.close()
