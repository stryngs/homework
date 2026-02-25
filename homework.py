#!/usr/bin/python3

import logging
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from lib.menu import Menu
from lib.notebook import Notebook
from lib.workbook import Workbook


class Shared(object):
    """Shared namespace"""

    def __init__(self, wb, nb):
        self.wb = wb
        self.nb = nb
        self.windowMain = None
        self.windowProblem = None
        self.counter = 1
        self.oprList = []
        self.runs = 0
        self.firstRun = True

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

    def update_workbook_from_vars():
        sh.wb.addXmin = int(mn.vars['addXmin'].get())
        sh.wb.addXmax = int(mn.vars['addXmax'].get())
        sh.wb.addYmin = int(mn.vars['addYmin'].get())
        sh.wb.addYmax = int(mn.vars['addYmax'].get())

        sh.wb.divXmin = int(mn.vars['divXmin'].get())
        sh.wb.divXmax = int(mn.vars['divXmax'].get())
        sh.wb.divYmin = int(mn.vars['divYmin'].get())
        sh.wb.divYmax = int(mn.vars['divYmax'].get())

        sh.wb.mulXmin = int(mn.vars['mulXmin'].get())
        sh.wb.mulXmax = int(mn.vars['mulXmax'].get())
        sh.wb.mulYmin = int(mn.vars['mulYmin'].get())
        sh.wb.mulYmax = int(mn.vars['mulYmax'].get())

        sh.wb.subXmin = int(mn.vars['subXmin'].get())
        sh.wb.subXmax = int(mn.vars['subXmax'].get())
        sh.wb.subYmin = int(mn.vars['subYmin'].get())
        sh.wb.subYmax = int(mn.vars['subYmax'].get())

        sh.wb.selectedAddition = mn.vars['selectedAddition'].get()
        sh.wb.selectedDivision = mn.vars['selectedDivision'].get()
        sh.wb.selectedMixedNumberAddition = mn.vars['selectedMixedNumberAddition'].get()
        sh.wb.selectedMixedNumberSubtraction = mn.vars['selectedMixedNumberSubtraction'].get()
        sh.wb.selectedMultiplication = mn.vars['selectedMultiplication'].get()
        sh.wb.selectedSubtraction = mn.vars['selectedSubtraction'].get()

        sh.wb.runsAddition = int(mn.vars['runsAddition'].get())
        sh.wb.runsDivision = int(mn.vars['runsDivision'].get())
        sh.wb.runsMixedNumberAddition = int(mn.vars['runsMixedNumberAddition'].get())
        sh.wb.runsMixedNumberSubtraction = int(mn.vars['runsMixedNumberSubtraction'].get())
        sh.wb.runsMultiplication = int(mn.vars['runsMultiplication'].get())
        sh.wb.runsSubtraction = int(mn.vars['runsSubtraction'].get())

    def build_opr_list():
        if sh.wb.selectedAddition is True:
            add_list = ['addition'] * sh.wb.runsAddition
        else:
            add_list = []
        if sh.wb.selectedDivision is True:
            div_list = ['division'] * sh.wb.runsDivision
        else:
            div_list = []
        if sh.wb.selectedMixedNumberAddition is True:
            mix_add_list = ['mixedNumberAddition'] * sh.wb.runsMixedNumberAddition
        else:
            mix_add_list = []
        if sh.wb.selectedMixedNumberSubtraction is True:
            mix_sub_list = ['mixedNumberSubtraction'] * sh.wb.runsMixedNumberSubtraction
        else:
            mix_sub_list = []
        if sh.wb.selectedMultiplication is True:
            mul_list = ['multiplication'] * sh.wb.runsMultiplication
        else:
            mul_list = []
        if sh.wb.selectedSubtraction is True:
            sub_list = ['subtraction'] * sh.wb.runsSubtraction
        else:
            sub_list = []
        return add_list + div_list + mul_list + sub_list + mix_add_list + mix_sub_list

    def on_problem_close():
        if sh.windowProblem is not None and sh.windowProblem.winfo_exists():
            sh.windowProblem.destroy()
        sh.windowProblem = None
        root.deiconify()

    def on_submit():
        if sh.firstRun is True:
            sh.firstRun = False
            try:
                mn.probGen(sh.oprList.pop(0))
            except IndexError:
                on_problem_close()
            return

        ## Math layout
        prb = f'{wb.math.get("x")} {wb.math.get("symbol")} {wb.math.get("y")}'

        rst = mn.answer_var.get()
        try:
            ## Convert to expecteds
            eRst = wb.math.get('result')
            eType = type(eRst)

            ## apples to apples
            if eType == str:
                if wb.math.get('symbol') == '/':
                    vRst = ''.join(rst.split())
            elif eType is int:
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
            nb.pad.update({sh.counter - 1: (datetime.now().strftime("%Y%m%d %I:%M:%S"),
                                            prb,
                                            cVal,
                                            eRst,
                                            vRst)})
            logging.info({sh.counter - 1: (prb, cVal, eRst, vRst)})

        except Exception:
            cVal = False
            logging.debug({sh.counter - 1: (prb, cVal, eRst, rst)})
            nb.pad.update({sh.counter - 1: (datetime.now().strftime("%Y%m%d %I:%M:%S"),
                                            prb,
                                            cVal,
                                            eRst,
                                            rst)})

        ## Store the wrong answers so they can retry
        if cVal is False:
            x = prb.split()[0]
            o = prb.split()[1]
            y = prb.split()[2]
            nb.retries.update({sh.counter: (x, o, y)})

        ## Counter check
        if sh.counter == sh.runs + 1:
            ## Retry logic
            if len(nb.retries) > 0:
                for k, v in nb.retries.items():
                    pass  ## Start here for retry functionality

            ## Notate how well
            tCorrect = 0
            for v in nb.pad.values():
                if v[2] is True:
                    tCorrect += 1
            passPct = "{:.2f}".format(tCorrect * (100 / sh.runs)) + '%'
            logging.info(f'Correct answers ~~> {tCorrect} out of {sh.runs} ~~> {passPct}')
            logging.info(f'{sh.runs} runs met, exiting\n')

            ## Close out current problem window
            on_problem_close()

            ## Reset counter
            sh.counter = 1
        else:
            ## Load new problem
            try:
                mn.probGen(sh.oprList.pop(0))
            except IndexError:
                pass

        if mn.answer_var is not None:
            mn.answer_var.set('')

    def on_launch():
        if sh.windowProblem is not None and sh.windowProblem.winfo_exists():
            return

        update_workbook_from_vars()
        sh.oprList = build_opr_list()
        sh.runs = len(sh.oprList)
        if sh.runs == 0:
            messagebox.showwarning('No problems selected',
                                   'Select at least one problem type.')
            return

        sh.firstRun = True

        ### Some kind of bug with smaller initial strings for auto_size_text
        sh.wb.math.update({'x': 10000})
        sh.wb.math.update({'y': 10000})
        sh.wb.math.update({'z': 10000})
        sh.wb.math.update({'a': 10000})
        sh.wb.math.update({'b': 10000})
        sh.wb.math.update({'c': 10000})

        problem = tk.Toplevel(root)
        problem.title('! PRACTICE QUESTION !')
        sh.windowProblem = problem
        mn.problem(problem, on_submit)
        problem.protocol('WM_DELETE_WINDOW', on_problem_close)
        root.withdraw()

    ## Grab a Workbook and Notebook
    wb = Workbook()
    nb = Notebook()
    sh = Shared(wb, nb)

    mn = Menu(sh)

    root = tk.Tk()
    root.title('Homework settings')
    root.geometry('1368x1280')
    sh.windowMain = root

    mn.main(root, on_launch)
    root.mainloop()


## Setup logging - <Date> <Time> <Math problem #> <Math problem> <Pass or Fail> <Expected answer> <Student answer>
logging.basicConfig(filename = 'student.log',
                    format = "%(asctime)s %(message)s",
                    datefmt = "%Y%m%d %I:%M:%S",
                    level = logging.DEBUG)

if __name__ == '__main__':
    main()
