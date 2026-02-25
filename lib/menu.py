import tkinter as tk


class Menu(object):
    """Class for all GUIs"""

    def __init__(self, shared):
        self.sh = shared
        self.theFont = ('Arial', 22)
        self.setFont = ('Courier', 22)
        self.vars = {}
        self.problem_text_var = None
        self.answer_var = None
        self.problem_window = None

    def _build_scrollable(self, parent):
        container = tk.Frame(parent)
        container.pack(fill = 'both', expand = True)

        canvas = tk.Canvas(container, highlightthickness=0)
        vscroll = tk.Scrollbar(container, orient = 'vertical', command = canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind('<Configure>',
                          lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window = scroll_frame, anchor = 'nw')
        canvas.configure(yscrollcommand = vscroll.set)

        canvas.pack(side = 'left', fill = 'both', expand = True)
        vscroll.pack(side = 'right', fill = 'y')

        def _on_mousewheel(event):
            if event.delta:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

        canvas.bind_all('<MouseWheel>', _on_mousewheel)
        return scroll_frame

    def _add_minmax_section(self, parent, title, xmin_key, xmax_key, ymin_key, ymax_key,
                            xmin_default, xmax_default, ymin_default, ymax_default):
        frame = tk.Frame(parent)
        frame.pack(fill = 'x', padx = 10, pady = 8)

        tk.Label(frame,
                 text = title,
                 font = self.theFont).grid(row = 0,
                                           column = 0,
                                           columnspan = 4,
                                           sticky = 'w',
                                           pady = (0, 6))

        self.vars[xmin_key] = tk.IntVar(value = xmin_default)
        self.vars[xmax_key] = tk.IntVar(value = xmax_default)
        self.vars[ymin_key] = tk.IntVar(value = ymin_default)
        self.vars[ymax_key] = tk.IntVar(value = ymax_default)

        tk.Label(frame,
                 text = 'Minimum X',
                 font = self.theFont).grid(row = 1,
                                           column = 0,
                                           sticky = 'w')
        tk.Scale(frame,
                 variable = self.vars[xmin_key],
                 from_ = 0,
                 to = 10000,
                 orient = 'horizontal',
                 length = 400).grid(row = 1,
                                    column = 1,
                                    sticky = 'w')
        tk.Label(frame,
                 text = 'Maximum X',
                 font = self.theFont).grid(row = 1,
                                           column = 2,
                                           sticky = 'w',
                                           padx = (20, 0))
        tk.Scale(frame,
                 variable = self.vars[xmax_key],
                 from_ = 0,
                 to = 10000,
                 orient = 'horizontal',
                 length = 400).grid(row = 1,
                                    column = 3,
                                    sticky = 'w')

        tk.Label(frame,
                 text = 'Minimum Y',
                 font = self.theFont).grid(row = 2,
                                           column = 0,
                                           sticky = 'w')
        tk.Scale(frame,
                 variable = self.vars[ymin_key],
                 from_ = 0,
                 to = 10000,
                 orient = 'horizontal',
                 length = 400).grid(row = 2,
                                    column = 1,
                                    sticky = 'w')
        tk.Label(frame,
                 text = 'Maximum Y',
                 font = self.theFont).grid(row = 2,
                                           column = 2,
                                           sticky = 'w',
                                           padx = (20, 0))
        tk.Scale(frame,
                 variable = self.vars[ymax_key],
                 from_ = 0,
                 to = 10000,
                 orient = 'horizontal',
                 length = 400).grid(row = 2,
                                    column = 3,
                                    sticky = 'w')

    def _add_selection_section(self, parent, on_launch):
        frame = tk.Frame(parent)
        frame.pack(fill = 'x', padx = 10, pady = 8)

        def add_row(row, label, var_key, run_key, default_selected, default_runs):
            self.vars[var_key] = tk.BooleanVar(value = default_selected)
            self.vars[run_key] = tk.IntVar(value = default_runs)
            tk.Checkbutton(frame,
                           text = label,
                           font = self.setFont,
                           variable = self.vars[var_key]).grid(row = row,
                                                               column = 0,
                                                               sticky = 'w')
            tk.Label(frame,
                     text = 'Problem count ~~>',
                     font = self.setFont).grid(row = row,
                                               column = 1,
                                               sticky = 'w',
                                               padx = (10, 0))
            tk.Scale(frame,
                     variable = self.vars[run_key],
                     from_ = 0,
                     to = 100,
                     orient = 'horizontal',
                     length = 400).grid(row = row,
                                        column = 2,
                                        sticky = 'w')

        add_row(0,
                'Addition',
                'selectedAddition',
                'runsAddition',
                True,
                10)
        add_row(1,
                'Division',
                'selectedDivision',
                'runsDivision',
                False,
                10)
        add_row(2,
                'Mixed Number Addition',
                'selectedMixedNumberAddition',
                'runsMixedNumberAddition',
                False,
                10)
        add_row(3,
                'Mixed Number Subtraction',
                'selectedMixedNumberSubtraction',
                'runsMixedNumberSubtraction',
                False,
                10)
        add_row(4,
                'Multiplication',
                'selectedMultiplication',
                'runsMultiplication',
                False,
                10)
        add_row(5,
                'Subtraction',
                'selectedSubtraction',
                'runsSubtraction',
                False,
                10)

        launch_frame = tk.Frame(parent)
        launch_frame.pack(fill = 'x', padx = 10, pady = (10, 20))
        tk.Button(launch_frame,
                  text = 'Launch',
                  font = self.theFont,
                  command = on_launch).pack(pady = 10)

    def main(self, parent, on_launch):
        """Present the main menu"""
        scroll = self._build_scrollable(parent)

        self._add_minmax_section(scroll,
                                 'Addition settings',
                                 'addXmin',
                                 'addXmax',
                                 'addYmin',
                                 'addYmax',
                                 self.sh.wb.addXmin,
                                 self.sh.wb.addXmax,
                                 self.sh.wb.addYmin,
                                 self.sh.wb.addYmax)
        tk.Frame(scroll,
                 height = 2,
                 bd = 1,
                 relief = 'sunken').pack(fill = 'x',
                                         padx = 5,
                                         pady = 6)

        self._add_minmax_section(scroll,
                                 'Division settings',
                                 'divXmin',
                                 'divXmax',
                                 'divYmin',
                                 'divYmax',
                                 self.sh.wb.divXmin,
                                 self.sh.wb.divXmax,
                                 self.sh.wb.divYmin,
                                 self.sh.wb.divYmax)
        tk.Frame(scroll,
                 height = 2,
                 bd = 1,
                 relief = 'sunken').pack(fill = 'x',
                                         padx = 5,
                                         pady = 6)

        self._add_minmax_section(scroll,
                                 'Multiplication settings',
                                 'mulXmin',
                                 'mulXmax',
                                 'mulYmin',
                                 'mulYmax',
                                 self.sh.wb.mulXmin,
                                 self.sh.wb.mulXmax,
                                 self.sh.wb.mulYmin,
                                 self.sh.wb.mulYmax)
        tk.Frame(scroll,
                 height = 2,
                 bd = 1,
                 relief = 'sunken').pack(fill = 'x',
                                         padx = 5,
                                         pady = 6)

        self._add_minmax_section(scroll,
                                 'Subtraction settings',
                                 'subXmin',
                                 'subXmax',
                                 'subYmin',
                                 'subYmax',
                                 self.sh.wb.subXmin,
                                 self.sh.wb.subXmax,
                                 self.sh.wb.subYmin,
                                 self.sh.wb.subYmax)
        tk.Frame(scroll,
                 height = 2,
                 bd = 1,
                 relief = 'sunken').pack(fill = 'x',
                                         padx = 5,
                                         pady = 6)

        self._add_selection_section(scroll, on_launch)

    def problem(self, parent, on_submit):
        """Present the math problem"""
        self.problem_window = parent
        frame = tk.Frame(parent)
        frame.pack(fill = 'both',
                   expand = True,
                   padx = 20,
                   pady = 20)

        self.problem_text_var = tk.StringVar(value = f'{self.sh.wb.math.get("x")} {self.sh.wb.math.get("symbol")} {self.sh.wb.math.get("y")} = ?')
        tk.Label(frame,
                 textvariable = self.problem_text_var,
                 font = self.theFont).pack(pady = 10)

        tk.Label(frame,
                 text = 'Your answer:',
                 font = self.theFont).pack(pady = (10, 0))
        self.answer_var = tk.StringVar()
        entry = tk.Entry(frame,
                         textvariable = self.answer_var,
                         font = self.theFont)
        entry.pack(pady=10)
        entry.focus_set()

        tk.Button(frame,
                  text = 'Ok',
                  font = self.theFont,
                  command = on_submit).pack(pady = 10)
        parent.bind('<Return>', lambda event: on_submit())

    def probGen(self, opr):
        ## Load new math problem from list
        self.sh.wb.handler(opr)

        ## Update the stdout
        self.sh.counter += 1
        prb = f'{self.sh.wb.math.get("x")} {self.sh.wb.math.get("symbol")} {self.sh.wb.math.get("y")}'
        if self.problem_text_var is not None:
            self.problem_text_var.set(f'{prb} = ?')
        if self.problem_window is not None:
            self.problem_window.title(f'Question #{self.sh.counter - 1}')
