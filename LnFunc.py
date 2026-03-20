

from MathInterface import MathInterface
from numbers import Number
from math import log
from Function import MFunction

#+, -, *, /, should support ordinary numbers
#Note that val is accessed in MathTerm
class Ln(MFunction):
    
    def __repr__(self):
        return 'ln('+str(self.contents)+')'
    
    def copy(self):
        return Ln(self.contents.copy())
    
    #Possible update - add "settings" to decide whether to combine, say, ln(x) and ln(1-x) or ln(x) and ln(x^2)
    def canaddcombine(self, other):
        if isinstance(other, Ln):
            if self.contents == other.contents:
                return True
            if self.contents == 1/other.contents:
                return True
            return False
        if isinstance(other, MathTerm):
            return other.canaddcombine(self)
        return isinstance(other, Polynomial)
    
    def equalszero(self):
        return self.contents == 1
    def derivative(self, respectto):
        return (1/self.contents)* self.contents.derivative(respectto)

    def __add__(self, other):
        if isinstance(other,Number):
            return Polynomial(terms=[self.copy(), MNumber(other)])
        if self.canaddcombine(other):
            if isinstance(other, Ln):
                if self.contents == other.contents:
                    return 2 * self
                elif self.contents == 1/other.contents:
                    return MNumber(0)
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
            return MNumber(log(interior.val))
        return Ln(interior)
        

from MNumber import MNumber
from Polynomial import Polynomial
from RationalFunction import RationalFunction
from MathTerm import MathTerm
a = Ln(MNumber(16))