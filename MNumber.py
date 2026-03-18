

from MathInterface import MathInterface
from numbers import Number


#+, -, *, /, should support ordinary numbers
#Note that val is accessed in MathTerm
class MNumber(MathInterface):
    def __init__(self, val=0):
        if not isinstance(val, Number):
            raise SyntaxError('Non-number '+str(val)+' passed to MNumber')
        self.val = val
    
    def __repr__(self):
        if self.val % 1 == 0:
            return str(int(self.val))
        return str(self.val)
    def latex(self):
        return str(self)
    
    def copy(self):
        return MNumber(self.val)
    
    def canaddcombine(self, other):
        return isinstance(other, MNumber) or isinstance(other, Number) or isinstance(other, Polynomial)
    
    def equalszero(self):
        return self.val == 0
    def derivative(self, respectto):
        return MNumber(0)

    def __add__(self, other):
        if isinstance(other, MNumber):
            return MNumber(self.val + other.val)
        if isinstance(other, Number):
            return MNumber(self.val + other)
        return NotImplemented
    def __mul__(self, other):
        if isinstance(other, MNumber):
            return MNumber(self.val * other.val)
        if isinstance(other, Number):
            return MNumber(self.val * other)
        return NotImplemented

    def oneoverself(self):
        return MNumber(1/self.val)

    def evaluate(self, var, value):
        return self.copy()
    def simplified(self):
        return self.copy()
    
    def __float__(self):
        return float(self.val)
    

a = MNumber(1)

from Polynomial import Polynomial