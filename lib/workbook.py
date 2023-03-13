import random
from configparser import ConfigParser
from decimal import Decimal
from fractions import Fraction
from math import gcd

class Workbook(object):
    def __init__(self):
        self.math = {'x':10000,
                     'y':10000,
                     'result':0,
                     'symbol': '+'}

         ## Setup defaults
        parser = ConfigParser()
        parser.read('homework.conf')

        ## addition parameters
        self.addXmin = int(parser.get('addition', 'xMin'))
        self.addXmax = int(parser.get('addition', 'xMax'))
        self.addYmin = int(parser.get('addition', 'yMin'))
        self.addYmax = int(parser.get('addition', 'yMax'))

        ## division parameters
        self.divXmin = int(parser.get('division', 'xMin'))
        self.divXmax = int(parser.get('division', 'xMax'))
        self.divYmin = int(parser.get('division', 'yMin'))
        self.divYmax = int(parser.get('division', 'yMax'))

        ## mixed number parameters
        self.mixXmin = int(parser.get('mixedNumber', 'xMin'))
        self.mixXmax = int(parser.get('mixedNumber', 'xMax'))
        self.mixYmin = int(parser.get('mixedNumber', 'yMin'))
        self.mixYmax = int(parser.get('mixedNumber', 'yMax'))
        self.mixZmin = int(parser.get('mixedNumber', 'zMin'))
        self.mixZmax = int(parser.get('mixedNumber', 'zMax'))
        self.mixAmin = int(parser.get('mixedNumber', 'aMin'))
        self.mixAmax = int(parser.get('mixedNumber', 'aMax'))
        self.mixBmin = int(parser.get('mixedNumber', 'bMin'))
        self.mixBmax = int(parser.get('mixedNumber', 'bMax'))
        self.mixCmin = int(parser.get('mixedNumber', 'cMin'))
        self.mixCmax = int(parser.get('mixedNumber', 'cMax'))

        ## multiplication parameters
        self.mulXmin = int(parser.get('multiplication', 'xMin'))
        self.mulXmax = int(parser.get('multiplication', 'xMax'))
        self.mulYmin = int(parser.get('multiplication', 'yMin'))
        self.mulYmax = int(parser.get('multiplication', 'yMax'))

        ## subtraction parameters
        self.subXmin = int(parser.get('subtraction', 'xMin'))
        self.subXmax = int(parser.get('subtraction', 'xMax'))
        self.subYmin = int(parser.get('subtraction', 'yMin'))
        self.subYmax = int(parser.get('subtraction', 'yMax'))


    def handler(self, opr = 'addition',
                x = None, y = None, z = None, a = None, b = None, c = None):
        self.opr = opr
        if opr == 'addition':
            if x is None and y is None:
                self.addition()
            else:
                self.addition(x, y)
        elif opr == 'division':
            if x is None and y is None:
                self.division()
            else:
                self.division(x, y)
        elif opr == 'subtraction':
            if x is None and y is None:
                self.subtraction()
            else:
                self.subtraction(x, y)
        elif opr == 'mixedNumberAddition':
            if x is None and y is None and z is None and a is None and b is None and c is None:
                self.mixedNumber('addition')
            else:
                self.mixedNumber('addition', x, y, z, a, b, c)
        elif opr == 'mixedNumberSubtraction':
            if x is None and y is None and z is None and a is None and b is None and c is None:
                self.mixedNumber('subtraction')
            else:
                self.mixedNumber('subtraction', x, y, z, a, b, c)
        elif opr == 'multiplication':
            if x is None and y is None:
                self.multiplication()
            else:
                self.multiplication(x, y)

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
        """ x / y || y / x """
        if x is None and y is None:
            x = random.randint(self.divXmin, self.divXmax)
            y = random.randint(self.divYmin, self.divYmax)

        ## Long divison conversions
        if x > y:
            self.math["x"] = x
            self.math["y"] = y
            v = x / y
            mod = x % y
            if mod == 0:
                val = str(v).split('.')[0]
            else:
                val = str(v).split('.')[0] + f'r{mod}'
        else:
            self.math["x"] = y
            self.math["y"] = x
            v = y / x
            mod = y % x
            if mod == 0:
                val = str(v).split('.')[0]
            else:
                val = str(v).split('.')[0] + f'r{mod}'
        self.math["result"] = val
        self.math["symbol"] = '/'
        self.opr = "division"


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


    def mixedNumber(self, opr, x = None, y = None, z = None,
                               a = None, b = None, c = None):
        """ x y/z +||- a b/c """
        if x is None:
            x = random.randint(self.mixXmin, self.mixXmax)
        if y is None:
            y = random.randint(self.mixYmin, self.mixYmax)
        if z is None:
            z = random.randint(self.mixZmin, self.mixZmax)
        if a is None:
            a = random.randint(self.mixAmin, self.mixAmax)
        if b is None:
            b = random.randint(self.mixBmin, self.mixBmax)
        if c is None:
            c = random.randint(self.mixCmin, self.mixCmax)

        ## Proper fractions
        if y > z:
            self.tY = z
            self.tZ = y
        else:
            self.tY = y
            self.tZ = z
        y = self.tY
        z = self.tZ
        if b > c:
            self.tB = c
            self.tC = b
        else:
            self.tB = b
            self.tC = c
        b = self.tB
        c = self.tC

        ## Keep the numbers positive
        print(x, y, z, a, b, c)
        if a + Fraction(f'{b}/{c}') > x + Fraction(f'{y}/{z}'):
            self.tA = x
            self.tB = y
            self.tC = z
            self.tX = a
            self.tY = b
            self.tZ = c
            a = self.tA
            b = self.tB
            c = self.tC
            x = self.tX
            y = self.tY
            z = self.tZ

        ## Left side denom * whole
        _x = Decimal(z) * Decimal(x)
        _y = _x + Decimal(y)                                                    ## _y is now the left numerator

        ## Right side denom * whole
        x_ = Decimal(c) * Decimal(a)
        y_ = x_ + Decimal(b)                                                    ## y_ is the right numerator

        ## Shortcut the work and increase both denominators
        _z_ = Decimal(z) * Decimal(c)

        ## Left new numerator
        __y = _y * Decimal(c)

        ## Right new numerator
        y__ = y_ * Decimal(z)

        ## Operator work
        if opr == 'addition':
            _y_ = __y + y__
        elif opr == 'subtraction':
            _y_ = __y - y__

        ## Now convert _y_ / _z_ to a mixed number.
        X = Decimal(_y_) / Decimal(_z_)
        Y = str(X).split('.')[0]
        Z = Decimal(_y_) % Decimal(_z_)

        ## Remainders
        if Z != Decimal(0):
            v = gcd(int(Z), int(_z_))
            Z = Z / v
            _z_ = _z_ / v
            self.math["result"] = f'{Y} {Z}/{_z_}'
        else:
            self.math["result"] = str(X)

        self.math["x"] = f'{x} {y}/{z}'
        self.math["y"] = f'{a} {b}/{c}'
        if opr == 'addition':
            self.math["symbol"] = '+'
            self.opr = 'mixedNumberAddition'
        elif opr == 'subtraction':
            self.math["symbol"] = '-'
            self.opr = 'mixedNumberSubtraction'
