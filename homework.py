#!/usr/bin/python3

import argparse
import logging
import math
import PySimpleGUI as sg
import sqlite3 as lite
# from configparser import ConfigParser
from datetime import datetime
from lib.menu import Menu
from lib.notebook import Notebook
from lib.workbook import Workbook
import time

class Shared(object):
    """Shared namespace"""
    def __init__(self, wb, nb):
        self.wb = wb
        self.nb = nb
        self.mainWindow = None
        self.problemWindow = None

        ### db thoughts
        # self.con = lite.connect('workbook.sqlite3')
        # self.db = self.con.cursor()
        #
        # self.db.execute("""
        #                 CREATE TABLE IF NOT EXISTS homework(id INTEGER,
        #                                                     qid INTEGER,
        #                                                     tstamp INTEGER,
        #                                                     x REAL,
        #                                                     y REAL,
        #                                                     symbol TEXT,
        #                                                     outcome REAL,
        #                                                     expected REAL,
        #                                                     actual REAL);
        #                 """)


def main():
    ## Grab a Workbook and Notebook
    wb = Workbook()
    nb = Notebook()
    sh = Shared(wb, nb)

    ## Drop the menu here, play later with arch layout/routines
    mn = Menu(sh)

    ## Notebook tracing
    sh.counter = 1

    ## Setup the main window layout
    layoutMain = mn.main()

    # Create the Window
    windowMain = sg.Window('Homework settings', layoutMain, resizable = True, size = (1368, 1280)).Finalize()
    windowProblem_active = False
    sh.windowMain = windowMain

    ## Launch the main loop
    while True:

        ## Read user input
        eventMain, valuesMain = windowMain.read()
        # print(valuesMain)

        ## Deal with main close
        if eventMain == sg.WIN_CLOSED:
            logging.critical('Main window closed\n')
            break

        ## Update shared config
        sh.wb.addXmin = int(valuesMain.get('addXmin'))  ## Offload to menu.py
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

        ## Selecteds
        sh.wb.selectedAddition = valuesMain.get('selectedAddition')
        sh.wb.selectedDivision = valuesMain.get('selectedDivision')
        sh.wb.selectedMixedNumberAddition = valuesMain.get('selectedMixedNumberAddition')
        sh.wb.selectedMixedNumberSubtraction = valuesMain.get('selectedMixedNumberSubtraction')
        sh.wb.selectedMultiplication = valuesMain.get('selectedMultiplication')
        sh.wb.selectedSubtraction = valuesMain.get('selectedSubtraction')

        ## Runs
        sh.wb.runsAddition = int(valuesMain.get('runsAddition'))
        sh.wb.runsDivision = int(valuesMain.get('runsDivision'))
        sh.wb.runsMixedNumberAddition = int(valuesMain.get('runsMixedNumberAddition'))
        sh.wb.runsMixedNumberSubtraction = int(valuesMain.get('runsMixedNumberSubtraction'))
        sh.wb.runsMultiplication = int(valuesMain.get('runsMultiplication'))
        sh.wb.runsSubtraction = int(valuesMain.get('runsSubtraction'))

        ## List loading
        if sh.wb.selectedAddition is True:
            addList = ['addition'] * sh.wb.runsAddition
        else:
             addList = []
        if sh.wb.selectedDivision is True:
            divList = ['division'] * sh.wb.runsDivision
        else:
             divList = []
        if sh.wb.selectedMixedNumberAddition is True:
            mixAddList = ['mixedNumberAddition'] * sh.wb.runsMixedNumberAddition
        else:
            mixAddList = []
        if sh.wb.selectedMixedNumberSubtraction is True:
            mixSubList = ['mixedNumberSubtraction'] * sh.wb.runsMixedNumberSubtraction
        else:
            mixSubList = []
        if sh.wb.selectedMultiplication is True:
            mulList = ['multiplication'] * sh.wb.runsMultiplication
        else:
            mulList = []
        if sh.wb.selectedSubtraction is True:
            subList = ['subtraction'] * sh.wb.runsSubtraction
        else:
            subList = []
        oprList = addList + divList + mulList + subList + mixAddList + mixSubList

        ## Settings accepted, move on to problem
        if eventMain == 'Launch' and not windowProblem_active:
            windowProblem_active = True
            windowMain.Hide()

            ### Some kind of bug with smaller initial strings for auto_size_text
            sh.wb.math.update({'x': 10000})
            sh.wb.math.update({'y': 10000})
            sh.wb.math.update({'z': 10000})
            sh.wb.math.update({'a': 10000})
            sh.wb.math.update({'b': 10000})
            sh.wb.math.update({'c': 10000})

            layoutProblem = mn.problem()
            windowProblem = sg.Window('! PRACTICE QUESTION !', layoutProblem, resizable = True)
            sh.windowProblem = windowProblem

            ## Loop through user input on problems
            runs = len(oprList)
            firstRun = True
            while True:

                ## Math layout
                prb = '{0} {1} {2}'.format(wb.math.get('x'),
                                           wb.math.get('symbol'),
                                           wb.math.get('y'))

                eventProblem, valuesProblem = windowProblem.read()

                ## Deal with problem closed
                if eventProblem == sg.WIN_CLOSED:
                    logging.critical('Problem window closed')
                    windowProblem.Close()
                    windowProblem_active = False
                    windowMain.UnHide()
                    break

                ## Store answer in notepad
                if firstRun is True:
                    firstRun = False
                    try:
                        mn.probGen(oprList.pop(0))

                    ## Handle situation where no options are selected
                    except:
                        windowProblem.Close()
                else:
                    rst = valuesProblem.get('answer')

                    try:
                        ## Convert to expecteds
                        eRst = wb.math.get('result')
                        eType = type(eRst)

                        ## apples to apples
                        if eType is int:
                            vRst = int(rst)
                        elif eType is float:
                            vRst = float(rst)
                        else:
                            vRst = rst

                        ## Verify the math
                        cVal = False
                        if vRst == eRst:
                            cVal = True

                        ## Update notebook
                        nb.pad.update({sh.counter - 1: (datetime.now().strftime("%Y%m%d %I:%M:%S"), prb, cVal, eRst, vRst)})
                        logging.info({sh.counter - 1: (prb, cVal, eRst, vRst)})

                    except:
                        cVal = False
                        logging.debug({sh.counter - 1: (prb, cVal, eRst, rst)})
                        nb.pad.update({sh.counter - 1: (datetime.now().strftime("%Y%m%d %I:%M:%S"), prb, cVal, eRst, rst)})

                    ## Store the wrong answers so they can retry
                    if cVal is False:
                        x = prb.split()[0]
                        o = prb.split()[1]
                        y = prb.split()[2]
                        nb.retries.update({sh.counter: (x, o, y)})

                    ## Counter check
                    if sh.counter == runs + 1:
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
                        try:
                            mn.probGen(oprList.pop(0))
                        except IndexError:
                            pass

## Setup logging - <Date> <Time> <Math problem #> <Math problem> <Pass or Fail> <Expected answer> <Student answer>
logging.basicConfig(filename = 'student.log', format = '%(asctime)s %(message)s',datefmt = '%Y%m%d %I:%M:%S', level = logging.DEBUG)

## Setup window theme
sg.theme('Dark')

if __name__ == '__main__':
    main()
