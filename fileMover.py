import os
import time
import shutil

def grab_files(exportDir, fileDir, seriesName, waitDelay = 0.01, copy = True):
    files = []
    print('checking')

    files = [file for file in os.listdir(exportDir) if '{}'.format(seriesName) in file]
    dirList = [file for file in os.listdir(fileDir) if '{}'.format(seriesName) in file]
    time.sleep(waitDelay)

    for file in files:
        try:
            if file in dirList:
                # print('{} already in dir. Skipping.'.format(file))
                pass
            else:
                move_files(file, exportDir, fileDir, copy = copy)
                if file.endswith('.csv'):
                    print(file)

        except Exception as e:
            print("permission error")
            print(e)
            time.sleep(waitDelay)
            waitDelay += 1
            return waitDelay

    # time.sleep(5)
    return waitDelay

def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def move_files(file, dirInitial, dirFinal, copy = None):
    make_dir(dirFinal)
    if copy == True:
        shutil.copyfile('{}/{}'.format(dirInitial, file), '{}/{}'.format(dirFinal, file))
    else:
        shutil.move('{}/{}'.format(dirInitial, file),'{}/{}'.format(dirFinal, file)) #


seriesName = "flaketest33"
exportDir = r"C:\Users\sjbrooke\Documents\tempData\flaketest14"
fileDir = r"H:\PhD\Raman\2021\4-27-21 CVD"+"\{}".format(seriesName)
waitDelay = 0.01

make_dir(fileDir)
while True:
    waitDelay = grab_files(exportDir, fileDir, seriesName, waitDelay = waitDelay, copy = True)
    time.sleep(1)
