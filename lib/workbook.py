import random
from configparser import ConfigParser

class Workbook(object):
    def __init__(self):
        self.math = {'x':10000,
                     'y':10000,
                     'result':0,
                     'symbol': '+'}

         ## Setup defaults
        parser = ConfigParser()
        parser.read('homework.conf')
        self.addXmin = int(parser.get('addition', 'xMin'))
        self.addXmax = int(parser.get('addition', 'xMax'))
        self.addYmin = int(parser.get('addition', 'yMin'))
        self.addYmax = int(parser.get('addition', 'yMax'))
        self.divXmin = int(parser.get('division', 'xMin'))
        self.divXmax = int(parser.get('division', 'xMax'))
        self.divYmin = int(parser.get('division', 'yMin'))
        self.divYmax = int(parser.get('division', 'yMax'))
        self.mulXmin = int(parser.get('multiplication', 'xMin'))
        self.mulXmax = int(parser.get('multiplication', 'xMax'))
        self.mulYmin = int(parser.get('multiplication', 'yMin'))
        self.mulYmax = int(parser.get('multiplication', 'yMax'))
        self.subXmin = int(parser.get('subtraction', 'xMin'))
        self.subXmax = int(parser.get('subtraction', 'xMax'))
        self.subYmin = int(parser.get('subtraction', 'yMin'))
        self.subYmax = int(parser.get('subtraction', 'yMax'))


    def addition(self, x = None, y = None):
        """ x + y """
        if x is None and y is None:
            x = random.randint(self.addXmin, self.addXmax)
            y = random.randint(self.addYmin, self.addYmax)
        self.math["x"] = x
        self.math["y"] = y
        self.math["result"] = x + y
        self.math["symbol"] = '+'
        self.opr = "addition"


    def division(self, x = None, y = None):
        """ x / y """
        if x is None and y is None:
            x = random.randint(self.divXmin, self.divXmax)
            y = x * random.randint(self.divYmin, self.divYmax)  ## No remainder
        self.math["x"] = x
        self.math["y"] = y
        self.math["result"] = x / y
        self.math["symbol"] = '/'
        self.opr = "division"


    def handler(self, opr = 'addition', x = None, y = None):
        self.opr = opr
        if opr == 'addition':
            if x is None and y is None:
                self.addition()
            else:
                self.addition(x, y)
        elif opr == 'subtraction':
            if x is None and y is None:
                self.subtraction()
            else:
                self.subtraction(x, y)
        elif opr == 'multiplication':
            if x is None and y is None:
                self.multiplication()
            else:
                self.multiplication(x, y)
        elif opr == 'division':
            if x is None and y is None:
                self.division()
            else:
                self.division(x, y)


    def multiplication(self, x = None, y = None):
        """ x * y """
        if x is None and y is None:
            x = random.randint(self.mulXmin, self.mulXmax)
            y = random.randint(self.mulYmin, self.mulYmax)
        self.math["x"] = x
        self.math["y"] = y
        self.math["result"] = x * y
        self.math["symbol"] = '*'
        self.opr = "multiplication"


    def subtraction(self, x = None, y = None):
        """ x - y || y - x """
        if x is None and y is None:
            x = random.randint(self.subXmin, self.subXmax)
            y = random.randint(self.subYmin, self.subYmax)
        if x > y:
            self.math["x"] = x
            self.math["y"] = y
            self.math["result"] = x - y
        else:
            self.math["x"] = y
            self.math["y"] = x
            self.math["result"] = y - x
        self.math["symbol"] = '-'
        self.opr = "subtraction"
