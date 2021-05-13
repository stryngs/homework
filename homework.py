#!/usr/bin/python3

import argparse
import logging
import math
import PySimpleGUI as sg
from configparser import ConfigParser
from datetime import datetime
from lib.menu import Menu
from lib.notebook import Notebook
from lib.workbook import Workbook
import time

"""
Logging format:
<Date> <Time> <Math problem #> <Math problem> <Pass or Fail> <Expected answer> <Student answer>
"""

class Shared(object):
    """Shared namespace"""
    def __init__(self, wb, nb):
        self.wb = wb
        self.nb = nb
        self.mainWindow = None
        self.problemWindow = None


def main(args):
    ## Max runs
    if args.r is not None:
        try:
            runs = int(args.r)
        except:
            runs = 10
    else:
        runs = 10

    ## Grab a Workbook and Notebook
    if args.t is None:
        wb = Workbook('addition')
    else:
        wb = Workbook(args.t)
    nb = Notebook()
    sh = Shared(wb, nb)

    ## Drop the menu here, play later with arch layout/routines
    mn = Menu(sh)

    ## Notebook tracing
    sh.counter = 1

    ## Setup the main window layout
    layoutMain = mn.main()

    # Create the Window
    windowMain = sg.Window('Homework settings', layoutMain).Finalize()
    windowProblem_active = False
    sh.windowMain = windowMain

    ## Launch the main loop
    while True:

        ## Read user input
        eventMain, valuesMain = windowMain.read()
        print(valuesMain)

        ## Deal with main close
        # if event is None:
        if eventMain == sg.WIN_CLOSED:
            logging.critical('Main window closed\n')
            break

        ## Update shared config
        sh.wb.addXmin = valuesMain.get('addXmin')  ## Offload to menu.py
        print(sh.wb.addXmin)
        print(valuesMain.get('addXmin'))
        sh.wb.addXmax = int(valuesMain.get('addXmax'))  ## Offload to menu.py
        sh.wb.addYmin = int(valuesMain.get('addYmin'))  ## Offload to menu.py
        sh.wb.addYmax = int(valuesMain.get('addYmax'))  ## Offload to menu.py

        sh.wb.divXmin = int(valuesMain.get('divXmin'))  ## Offload to menu.py
        sh.wb.divXmax = int(valuesMain.get('divXmax'))  ## Offload to menu.py
        sh.wb.divYmin = int(valuesMain.get('divYmin'))  ## Offload to menu.py
        sh.wb.divYmax = int(valuesMain.get('divYmax'))  ## Offload to menu.py

        sh.wb.mulXmin = int(valuesMain.get('mulXmin'))  ## Offload to menu.py
        sh.wb.mulXmax = int(valuesMain.get('mulXmax'))  ## Offload to menu.py
        sh.wb.mulYmin = int(valuesMain.get('mulYmin'))  ## Offload to menu.py
        sh.wb.mulYmax = int(valuesMain.get('mulYmax'))  ## Offload to menu.py

        sh.wb.subXmin = int(valuesMain.get('subXmin'))  ## Offload to menu.py
        sh.wb.subXmax = int(valuesMain.get('subXmax'))  ## Offload to menu.py
        sh.wb.subYmin = int(valuesMain.get('subYmin'))  ## Offload to menu.py
        sh.wb.subYmax = int(valuesMain.get('subYmax'))  ## Offload to menu.py

        ## Settings accepted, move on to problem
        if eventMain == 'Launch' and not windowProblem_active:
            windowProblem_active = True
            windowMain.Hide()
            layoutProblem = mn.problem()
            windowProblem = sg.Window('Question #1', layoutProblem)
            sh.windowProblem = windowProblem

            ## Loop through user input on problems
            while True:

                ## Math layout
                prb = '{0} {1} {2}'.format(wb.math.get('x'),
                                           wb.math.get('symbol'),
                                           wb.math.get('y'))

                eventProblem, valuesProblem = windowProblem.read()

                ## Deal with problem closed
                if eventProblem == sg.WIN_CLOSED:
                    print('CLOSED')
                    logging.critical('Problem window closed')
                    windowProblem.Close()
                    windowProblem_active = False
                    windowMain.UnHide()
                    break

                ## Store answer in notepad
                rst = valuesProblem.get('answer')

                try:
                    ## Convert to expecteds
                    eRst = wb.math.get('result')
                    eType = type(eRst)
                    if eType is int:
                        vRst = int(rst)
                    elif eType is float:
                        vRst = float(rst)

                    ## Verify the math
                    cVal = False
                    if vRst == eRst:
                        cVal = True
                    else:
                        cVal = False

                    ## Update notebook
                    nb.pad.update({sh.counter: (datetime.now().strftime("%Y%m%d %I:%M:%S"), prb, cVal, eRst, vRst)})
                    logging.info({sh.counter: (prb, cVal, eRst, vRst)})

                except:
                    cVal = False
                    logging.debug({sh.counter: (prb, cVal, eRst, rst)})
                    nb.pad.update({sh.counter: (datetime.now().strftime("%Y%m%d %I:%M:%S"), prb, cVal, eRst, rst)})

                ## Store the wrong answers so they can retry
                if cVal is False:
                    x = prb.split()[0]
                    o = prb.split()[1]
                    y = prb.split()[2]
                    nb.retries.update({sh.counter: (x, o, y)})

                ## Counter check
                if sh.counter == runs:
                    time.sleep(1)

                    ## Retry logic
                    if len(nb.retries) > 0:
                        for k, v in nb.retries.items():
                            pass ## Start here for retry functionality

                    ## Notate how well
                    tCorrect = 0
                    for v in nb.pad.values():
                        if v[2] is True:
                            tCorrect += 1
                    passPct = '{:.2f}'.format(tCorrect * (100 / runs)) + '%'
                    logging.info('Correct answers ~~> {0} out of {1} ~~> {2}'.format(tCorrect, runs, passPct))
                    logging.info('{0} runs met, exiting\n'.format(runs))

                    ## Close out current problem window
                    windowProblem.Close()
                    windowProblem_active = False
                    windowMain.UnHide()

                    ## Reset counter
                    sh.counter = 1

                else:
                    ## Load new problem
                    mn.probGen()

## Setup logging
logging.basicConfig(filename='student.log', format='%(asctime)s %(message)s',datefmt='%Y%m%d %I:%M:%S', level=logging.DEBUG)

## Setup window theme
sg.theme('Dark')

## Sounds -- lags on a pi, look for a better solution
# pSound = pyglet.media.load('sounds/pass.ogg', streaming = False)
# fSound = pyglet.media.load('sounds/fail.ogg', streaming = False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'homework')
    parser.add_argument('-t',
                        choices = ['addition',
                                   'division',
                                   'multiplication',
                                   'subtraction'],
                        help = 'Type of homework - Default is addition')
    parser.add_argument('-r',
                        help = 'Number of homework problems')
    main(parser.parse_args())
