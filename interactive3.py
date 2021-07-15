import numpy as np
import matplotlib.pyplot as plt
import keyboard
import time
# import tty
# import termios

def main():
    dataX = np.array([1,2,3,4]).astype(float)
    dataY = np.array(dataX**2).astype(float)
    plt.ion()
    fig, ax = plt.subplots()

    ax.plot(dataX, dataY)

    while True:
        inp = input('Com\n')
        print('INPUT:{}'.format(inp))

        if inp == 'quit':
            break

        if inp == 'title':
            inp2 = input('Enter new title:\n')
            try:
                ax.set_title(str(inp2))
            except:
                pass


# main()


import curses
from curses import wrapper
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from curses.textpad import Textbox, rectangle
import locale

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

def stdp(stdscr, text, pos = (1, 2)):
    stdscr.addstr(*pos, str(text))
    stdscr.refresh()
    stdscr.getkey()


def main(stdscr):
    # Clear screen
    stdscr.clear()
    # turn off echo
    curses.noecho()
    # react to keys instantly
    curses.cbreak()
    #bring text onstreen
    curses.nocbreak()
    curses.echo()
    stdscr.keypad(False)

    # # This raises ZeroDivisionError when i == 10.
    # for i in range(0, 11):
    #     v = i-10
    #     stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))

    # stdscr.addstr(2,2,str(print(curses)))
    # stdp(stdscr, curses.is_term_resized(30,120))
    curses.resize_term(50, 50)
    # stdp(stdscr, dir(stdscr))
    # stdp(stdscr, dir(stdscr.border))
    stdscr.refresh()

    # stdscr.getkey()

    cursesRows = curses.LINES
    cursesCols = curses.COLS
    # curses.LINES =100
    # curses.COLS = 400
    # stdscr.refresh()



    colour_schemes = {'magenta':(1000, 0, 1000), 'blue':(0, 500, 1000), 'green':(0, 0, 1000), 'cyan':(0, 1000,1000)}
    curses.start_color()
    curses.init_color(7, *colour_schemes['magenta']) # colour 7 is while - text

    begin_x = 0; begin_y = 0
    height = 50; width = 50
    win = curses.newwin(height, width, begin_y, begin_x)
    for x in range(width):
        for y in range(height):
            if x == 0 or x == width-2:
                win.addch(y,x, '|')
            elif y == 0 or y == height-2:
                win.addch(y,x, '_')
    # win.addstr(5,5, 'number of lines: '+str(curses.LINES))
    # win.addstr(6,5, 'number of cols: '+str(curses.COLS))

    # win.addstr(2,50, 'HELP')
    win.refresh()
    # stdscr.getkey()

    pad = curses.newpad(100, 30)
    # These loops fill the pad with letters; addch() is
    # explained in the next section
    for y in range(0, 10):
        for x in range(0, 10):
            pad.addch(y,x, 'V', curses.color_pair(3))
    #         # curses.delay_output(1)

    pad.refresh(0,0, 0,0, 30,49)

    curses.flash()

    # Displays a section of the pad in the middle of the screen.
    # (0,0) : coordinate of upper-left corner of pad area to display.
    # (5,5) : coordinate of upper-left corner of window area to be filled
    #         with pad content.
    # (20, 75) : coordinate of lower-right corner of window area to be
    #          : filled with pad content.

    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
    pad2 = curses.newpad(100,100)
    pad2.addstr(2,2, str(curses.can_change_color()), curses.color_pair(3))
    pad2.addstr(3,2, 'Different colour 1')
    pad2.refresh(1,0, 2,5, 5,30)

    stdscr.addstr(0, 0, "Menu1")
    stdscr.addstr(1, 0, "Menu2")

    editwin = curses.newwin(5,30, 2,1)
    # rect = patches.Rectangle(0,0,10,10)

    rectangle(stdscr, 5,5, 10, 30)
    stdscr.refresh()
    # curses.beep()

    box = Textbox(editwin)

    # Let the user edit until Ctrl-G is struck.
    # box.edit()


    # Get resulting contents
    # message = box.gather()

    # pad.refresh( 0,0, 5,5, 20,75)


    stdscr.getkey()

wrapper(main)
# print(curses.color_content(2))
# print(curses.LINES)
