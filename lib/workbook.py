import random

class Workbook(object):
    def __init__(self, opr = 'addition'):
        self.math = {'x':0,
                     'y':0,
                     'result':0,
                     'symbol': None}
        self.handler(opr)


    def addition(self, x = None, y = None):
        """ x + y """
        if x is None and y is None:
            x = random.randint(0,100)
            y = random.randint(0,100)
        self.math["x"] = x
        self.math["y"] = y
        self.math["result"] = x + y
        self.math["symbol"] = '+'
        self.opr = "addition"


    def division(self, x = None, y = None):
        """ x / y """
        if x is None and y is None:
            x = random.randint(0,100)
            y = x * random.randint(1,100)  ## No remainder
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
            x = random.randint(0,100)
            y = random.randint(0,100)
        self.math["x"] = x
        self.math["y"] = y
        self.math["result"] = x * y
        self.math["symbol"] = '*'
        self.opr = "multiplication"


    def subtraction(self, x = None, y = None):
        """ x - y || y - x """
        if x is None and y is None:
            x = random.randint(0,100)
            y = random.randint(0,100)
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
