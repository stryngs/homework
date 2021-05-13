import PySimpleGUI as sg

class Menu(object):
    """Class for all GUIs"""

    def __init__(self, shared):
        self.sh = shared
        self.theFont = 'Arial 24'

    def main(self):
        """Present the main menu"""
        ## To be implemented next so as to get away from argument passing
        """Present the math problem"""
        addMenu = [[sg.Text('Addition settings', font = self.theFont)],
                   [sg.Text('Minimum X', font = self.theFont),
                    sg.Slider(range=(0, 10000),
                              default_value = self.sh.wb.addXmin,
                              orientation='h',
                              size = (50, 20),
                              key = 'addXmin'),
                    sg.Text('     '),
                    sg.Text('Maximum X', font = self.theFont),
                    sg.Slider(range=(0, 10000),
                              default_value = self.sh.wb.addXmax,
                              orientation='h',
                              size = (50, 20),
                              key = 'addXmax')],
                   [],
                   [sg.Text('Minimum Y', font = self.theFont),
                    sg.Slider(range=(0, 10000),
                              default_value = self.sh.wb.addYmin,
                              orientation='h',
                              size = (50, 20),
                              key = 'addYmin'),
                    sg.Text('     '),
                    sg.Text('Maximum Y', font = self.theFont),
                    sg.Slider(range=(0, 10000),
                              default_value = self.sh.wb.addYmax,
                              orientation='h',
                              size = (50, 20),
                              key = 'addYmax')]]

        divMenu = [[sg.Text('Division settings', font = self.theFont)],
                   [sg.Text('Minimum X', font = self.theFont),
                    sg.Slider(range=(0, 10000),
                              default_value = self.sh.wb.divXmin,
                              orientation='h',
                              size = (50, 20),
                              key = 'divXmin'),
                    sg.Text('     '),
                    sg.Text('Maximum X', font = self.theFont),
                    sg.Slider(range=(0, 10000),
                              default_value = self.sh.wb.divXmax,
                              orientation='h',
                              size = (50, 20),
                              key = 'divXmax')],
                   [],
                   [sg.Text('Minimum Y', font = self.theFont),
                    sg.Slider(range=(0, 10000),
                              default_value = self.sh.wb.divYmin,
                              orientation='h',
                              size = (50, 20),
                              key = 'divYmin'),
                    sg.Text('     '),
                    sg.Text('Maximum Y', font = self.theFont),
                    sg.Slider(range=(0, 10000),
                              default_value = self.sh.wb.divYmax,
                              orientation='h',
                              size = (50, 20),
                              key = 'divYmax')]]

        mulMenu = [[sg.Text('Multiplication settings', font = self.theFont)],
                   [sg.Text('Minimum X', font = self.theFont),
                    sg.Slider(range=(0, 10000),
                              default_value = self.sh.wb.mulXmin,
                              orientation='h',
                              size = (50, 20),
                              key = 'mulXmin'),
                    sg.Text('     '),
                    sg.Text('Maximum X', font = self.theFont),
                    sg.Slider(range=(0, 10000),
                              default_value = self.sh.wb.mulXmax,
                              orientation='h',
                              size = (50, 20),
                              key = 'mulXmax')],
                   [],
                   [sg.Text('Minimum Y', font = self.theFont),
                    sg.Slider(range=(0, 10000),
                              default_value = self.sh.wb.mulYmin,
                              orientation='h',
                              size = (50, 20),
                              key = 'mulYmin'),
                    sg.Text('     '),
                    sg.Text('Maximum Y', font = self.theFont),
                    sg.Slider(range=(0, 10000),
                              default_value = self.sh.wb.mulYmax,
                              orientation='h',
                              size = (50, 20),
                              key = 'mulYmax')]]

        subMenu = [[sg.Text('Subtraction settings', font = self.theFont)],
                   [sg.Text('Minimum X', font = self.theFont),
                    sg.Slider(range=(0, 10000),
                              default_value = self.sh.wb.subXmin,
                              orientation='h',
                              size = (50, 20),
                              key = 'subXmin'),
                    sg.Text('     '),
                    sg.Text('Maximum X', font = self.theFont),
                    sg.Slider(range=(0, 10000),
                              default_value = self.sh.wb.subXmax,
                              orientation='h',
                              size = (50, 20),
                              key = 'subXmax')],
                   [],
                   [sg.Text('Minimum Y', font = self.theFont),
                    sg.Slider(range=(0, 10000),
                              default_value = self.sh.wb.subYmin,
                              orientation='h',
                              size = (50, 20),
                              key = 'subYmin'),
                    sg.Text('     '),
                    sg.Text('Maximum Y'),
                    sg.Slider(range=(0, 10000),
                              default_value = self.sh.wb.subYmax,
                              orientation='h',
                              size = (50, 20),
                              key = 'subYmax')]]

        inpMenu = [[sg.Checkbox('Addition',
                                default = True,
                                font = self.theFont,
                                key = 'selectedAddition')],
                   [sg.Text()],
                   [sg.Checkbox('Division',
                                default = False,
                                font = self.theFont,
                                key = 'selectedDivision')],
                   [sg.Text()],
                   [sg.Checkbox('Multiplication',
                                default = False,
                                font = self.theFont,
                                key = 'selectedMultiplication')],
                   [sg.Text()],
                   [sg.Checkbox('Subtraction',
                                default = False,
                                font = self.theFont,
                                key = 'selectedSubtraction')],
                   [sg.Button('Launch', pad = (500, 0), bind_return_key = True,
                    font = self.theFont, )]]

        self.layout = addMenu + [[sg.Text('_' * 160)]] +\
                      divMenu + [[sg.Text('_' * 160)]] +\
                      mulMenu + [[sg.Text('_' * 160)]] +\
                      subMenu + [[sg.Text('_' * 160)]] +\
                      inpMenu
        return self.layout

    def problem(self):
        """Present the math problem"""
        print('break')
        print(self.sh.wb.math.get('x'))
        print('end break')
        self.layout = [[sg.Text('{0} {1} {2} = ?'.format(self.sh.wb.math.get('x'),
                                                         self.sh.wb.math.get('symbol'),
                                                         self.sh.wb.math.get('y')),
                        key = 'mth',
                        font = self.theFont)],
                       [sg.Text()],
                       [sg.Text('Your answer:',
                                font = self.theFont),
                        sg.InputText(do_not_clear = False,
                                     key = 'answer',
                                     font = self.theFont)],
                       [sg.Text()],
                       [sg.Button('Ok',
                                  bind_return_key = True,
                                  font = self.theFont)]]
        return self.layout


    def probGen(self):
        ## Load new math problem
        self.sh.wb.handler(self.sh.wb.opr)

        ## Update the stdout
        self.sh.counter += 1
        prb = '{0} {1} {2}'.format(self.sh.wb.math.get('x'),
                                   self.sh.wb.math.get('symbol'),
                                   self.sh.wb.math.get('y'))
        self.sh.windowProblem['mth'].update('{0} = ?'.format(prb))
        self.sh.windowProblem.TKroot.title('Question #{0}'.format(self.sh.counter))
