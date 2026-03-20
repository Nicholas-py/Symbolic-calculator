

from MathInterface import MathInterface
from numbers import Number
from math import log
from Function import MFunction
from math import pi, sin, cos


class Sin(MFunction):
    
    def __repr__(self):
        return 'sin('+str(self.contents)+')'
    
    def copy(self):
        return Sin(self.contents.copy())
    
    def canaddcombine(self, other):
        if isinstance(other, Sin):
            if self.contents == other.contents:
                return True
            return False
        if isinstance(other, MathTerm):
            return other.canaddcombine(self)
        return isinstance(other, Polynomial)
    
    
    def equalszero(self):
        if isinstance(self.contents, MNumber):
            return self.contents.val/pi % 1 == 0
        return False
    
    def derivative(self, respectto):
        return Cos(self.contents) * self.contents.derivative(respectto)

    def __add__(self, other):
        if isinstance(other,Number):
            return Polynomial(terms=[self.copy(),MNumber(other)])
        if self.canaddcombine(other):
            if isinstance(other, Sin):
                if self.contents == other.contents:
                    return 2 * self
            return NotImplemented
        if isinstance(other, Polynomial):
            return NotImplemented
        return Polynomial(terms=[self.copy(), other.copy()])
    def __mul__(self, other):
        if isinstance(other, Number):
            other = MNumber(other)
        if isinstance(other, MathTerm) or isinstance(other, Polynomial) or isinstance(other, RationalFunction):
            return NotImplemented
        return MathTerm([self.copy(),other.copy()])


    def evaluate(self, var, value):
        interior = self.contents.evaluate(var, value)
        if isinstance(interior, MNumber):
            return MNumber(sin(interior.val))
        return Sin(interior)

class Cos(MFunction):
    
    def __repr__(self):
        return 'cos('+str(self.contents)+')'
    
    def copy(self):
        return Cos(self.contents.copy())
    
    def canaddcombine(self, other):
        if isinstance(other, Cos):
            if self.contents == other.contents:
                return True
            return False
        if isinstance(other, MathTerm):
            return other.canaddcombine(self)
        return isinstance(other, Polynomial)
    
    #Temporary, ideall
    def equalszero(self):
        self.contents = self.contents.simplified()
        if isinstance(self.contents, MNumber):
            return self.contents.val/pi % 1 == 0
        return False
    
    def derivative(self, respectto):
        return -Sin(self.contents) * self.contents.derivative(respectto)

    def __add__(self, other):
        if isinstance(other,Number):
            return Polynomial(terms=[self.copy(),MNumber(other)])
        if self.canaddcombine(other):
            if isinstance(other, Cos):
                if self.contents == other.contents:
                    return 2 * self
            return NotImplemented
        if isinstance(other, Polynomial):
            return NotImplemented
        return Polynomial(terms=[self.copy(), other.copy()])
    def __mul__(self, other):
        if isinstance(other, Number):
            other = MNumber(other)
        if isinstance(other, MathTerm) or isinstance(other, Polynomial) or isinstance(other, RationalFunction):
            return NotImplemented
        return MathTerm([self.copy(),other.copy()])


    def evaluate(self, var, value):
        interior = self.contents.evaluate(var, value)
        if isinstance(interior, MNumber):
            return MNumber(cos(interior.val))
        return Cos(interior)
        

from MNumber import MNumber
from Polynomial import Polynomial
from RationalFunction import RationalFunction
from MathTerm import MathTerm
a = Sin(MNumber(16))
print(a)