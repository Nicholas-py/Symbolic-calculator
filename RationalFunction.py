from MathInterface import MathInterface
from numbers import Number
from warnings import warn
from Polynomial import Polynomial

#Guaranteed a numerator, but not a denominator
class RationalFunction(MathInterface):
    def __init__(self,arg=None):
        self.numerator = None
        self.denominator = None
        if arg == None:
            self.numerator = MNumber(1)
            return
        if isinstance(arg, Number):
            self.numerator = MNumber(arg)
        elif isinstance(arg, str):
            split = arg.split('/')
            for i in split:
                if i[0] == '(' and i[-1] == ')':
                    i = i[1:-1]
                if self.numerator:
                    if self.denominator is None:
                        self.denominator = MNumber(1)
                    self.denominator *= i
                else:
                    self.numerator = i
        elif isinstance(arg,list):
            functions = arg
            self.numerator = functions[0]
            for i in range(1,len(functions)):
                if self.denominator is None:
                    self.denominator = MNumber(1)
                self.denominator *= functions[i]
            #print('FOUND',self.numerator,self.denominator)
        elif isinstance(arg, Polynomial):
            self.numerator = arg
        elif isinstance(arg, MathTerm):
            self.numerator = Polynomial(terms = [arg])
        else:
            self.numerator = Polynomial()
        if self.denominator is None:
            warn('RationalFunction '+str(self.numerator)+' created without denominator')

    def simplified(self):
        numerator = self.numerator.simplified()
        if self.denominator is None:
            return numerator
        denominator = self.denominator.simplified()
        if denominator == 0:
            raise ZeroDivisionError()
        elif denominator == 1:
            return numerator
        elif isinstance(denominator, MNumber):
            return numerator/denominator
        return RationalFunction([numerator, denominator])

    def canaddcombine(self, other):
        return True
                
    
    def copy(self):
        a = RationalFunction()
        a.numerator = self.numerator.copy()
        a.denominator = self.denominator.copy() if self.denominator is not None else None
        return a

    def __repr__(self):
        #print('NUM=',self.numerator, 'DENOM=',self.denominator)
        if self.denominator is None:
            return str(self.numerator)
        if self == 0:
            return '0'
        s = '('
        s += str(self.numerator)
        s += ')/('
        s += str(self.denominator)
        s += ')'
        return s
    def latex(self):
        if self == 0:
            return '0'

        if self.denominator is None:
            return self.numerator.latex()
        s = '\\frac{'
        s += self.numerator.latex()
        s += '}{'
        s += self.denominator.latex()
        s += '}'
        return s
    
    
    def oneoverself(self):
        a = self.copy()
        a.numerator, a.denominator = a.denominator, a.numerator
        if a.numerator is None:
            a.numerator = MNumber(1)
        return a.simplified()

    def __add__(self, other):
        if other == 0:
            return self.copy()
        if isinstance(other, RationalFunction):
            a = RationalFunction()
            d1 = self.denominator if self.denominator is not None else MNumber(1)
            d2 = other.denominator if other.denominator is not None else MNumber(1)
            a.denominator = d1 * d2
            a.numerator = self.numerator * d2 + other.numerator * d1
            a = a.simplified()
            return a
        elif isinstance(other, MathInterface) or isinstance(other, Number):
            if self.denominator is None:
                return self.numerator * other
            a = RationalFunction()
            a.denominator = self.denominator
            a.numerator = self.numerator + other * self.denominator
            return a.simplified()
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, RationalFunction):
            a = RationalFunction()
            d1 = self.denominator if self.denominator is not None else MNumber(1)
            d2 = other.denominator if other.denominator is not None else MNumber(1)
            a.denominator = d1*d2
            a.numerator = self.numerator * other.numerator
            return a.simplified()
        elif isinstance(other, MathInterface) or isinstance(other, Number):
            a = self.copy()
            a.numerator = a.numerator * other
            return a.simplified()
        return NotImplemented
                
    def __pow__(self, other):
        if isinstance(other, Number):
            a  = self.copy()
            a.numerator = a.numerator ** other
            if a.denominator:
                a.denominator = a.denominator**other
                return a
            else:
                return a.numerator
        return NotImplemented

    def equalszero(self):
        return self.numerator == 0
    
    def evaluate(self,val, value):
        return self.numerator.evaluate(val, value)/self.denominator.evaluate(val, value)

    def derivative(self,respectto):
        if self.denominator is None:
            return self.numerator.derivative(respectto)
        num =  self.numerator.derivative(respectto) * self.denominator - self.denominator.derivative(respectto) * self.numerator
        denom = self.denominator**2
        a = RationalFunction([num, denom])
        return a.simplified()


from MathTerm import MathTerm
from MNumber import MNumber