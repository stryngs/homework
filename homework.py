#!/usr/bin/python3

import argparse
import logging
import pyglet
import PySimpleGUI as sg
from datetime import datetime
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

def probGen(sh):
    ## Load new math problem
    sh.wb.handler(sh.wb.opr)

    ## Update the stdout
    sh.counter += 1
    prb = '{0} {1} {2}'.format(sh.wb.math.get('x'),
                               sh.wb.math.get('symbol'),
                               sh.wb.math.get('y'))
    sh.window['mth'].update('{0} = ?'.format(prb))
    sh.window.TKroot.title('Question #{0}'.format(sh.counter))


def main(args):
    ## Max runs
    if args.r is not None:
        try:
            runs = int(args.r)
        except:
            runs = 10

    ## Grab a Workbook and Notebook
    if args.t is None:
        wb = Workbook('addition')
    else:
        wb = Workbook(args.t)
    nb = Notebook()
    sh = Shared(wb, nb)

    ## Notebook tracing
    sh.counter = 1

    ## Setup the window layout
    layout = [[sg.Text('{0} {1} {2} = ?'.format(wb.math.get('x'),
                                                wb.math.get('symbol'),
                                                wb.math.get('y')),
               key = 'mth',
               font = theFont)],
              [sg.Text()],
              [sg.Text('Your answer:',
                       font = theFont),
               sg.InputText(do_not_clear = False,
                            key = 'answer',
                            font = theFont)],
              [sg.Text()],
              [sg.Button('Ok',
                         bind_return_key = True,
                         font = theFont)]]

    # Create the Window
    window = sg.Window('Question #1', layout).Finalize()
    sh.window = window

    ## Run the homework
    while True:

        ## Math layout
        prb = '{0} {1} {2}'.format(wb.math.get('x'),
                                   wb.math.get('symbol'),
                                   wb.math.get('y'))

       ## Launch
        event, values = window.read()

        ## Store answer in notepad
        try:
            rst = values.get('answer')
        except:
            logging.critical('User closed program?')
            break

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
                pSound.play()
            else:
                cVal = False
                fSound.play()

            ## Update notebook
            nb.pad.update({sh.counter: (datetime.now().strftime("%Y%m%d %I:%M:%S"), prb, cVal, eRst, vRst)})
            logging.info({sh.counter: (prb, cVal, eRst, vRst)})

        except:
            cVal = False
            fSound.play()
            logging.debug({sh.counter: (prb, cVal, eRst, rst)})
            nb.pad.update({sh.counter: (datetime.now().strftime("%Y%m%d %I:%M:%S"), prb, cVal, eRst, rst)})

        ## Store the wrong answers so they can retry

        if cVal is False:
            x = prb.split()[0]
            o = prb.split()[1]
            y = prb.split()[2]
            nb.retries.update({sh.counter: (x, o, y)})

        ## Close
        if event is None:
            logging.critical('Window closed\n')
            break

        ## Load new problem
        probGen(sh)

        ## Counter check
        if sh.counter == runs + 1:
            time.sleep(1)

            ## Retry logic
            if len(nb.retries) > 0:
                for k, v in nb.retries.items():
                    pass ## Start here for retry functionality

            ## Correct marks
            tCorrect = 0
            for v in nb.pad.values():
                if v[2] is True:
                    tCorrect += 1
            logging.info('Correct answers ~~> {0} out of {1}'.format(tCorrect, runs))
            logging.info('{0} runs met, exiting\n'.format(runs))
            break

    ## guiExit
    window.close()

## Setup logging
logging.basicConfig(filename='student.log', format='%(asctime)s %(message)s',datefmt='%Y%m%d %I:%M:%S', level=logging.DEBUG)

## Setup window theme
sg.theme('Dark')

## Setup font
theFont = 'Arial 24'

## Sounds
pSound = pyglet.media.load('sounds/pass.ogg', streaming = False)
fSound = pyglet.media.load('sounds/fail.ogg', streaming = False)

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
