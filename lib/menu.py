import PySimpleGUI as sg

class Menu(object):
    """Class for all GUIs"""

    def __init__(self, shared):
        self.sh = shared
        self.theFont = 'Arial 24'

    def main(self):
        """Present the main menu"""
        ## To be implemented next so as to get away from argument passing
        pass

    def problem(self):
        """Present the math problem"""
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
        self.sh.window['mth'].update('{0} = ?'.format(prb))
        self.sh.window.TKroot.title('Question #{0}'.format(self.sh.counter))
