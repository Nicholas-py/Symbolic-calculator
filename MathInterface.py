from abc import *
from numbers import Number

class MathInterface(ABC):
    @abstractmethod
    def __init__(self, arg):
        pass

    def simplified(self):
        from simplify import simplify
        return simplify(self)

    def issimplified(self):
        return False

    def setsimplified(self, val=True):
        self.issimplified = lambda : val

    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def derivative(self, respectto):
        pass

    @abstractmethod
    def evaluate(self, var, value):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def latex(self):
        pass
    
    @abstractmethod
    def canaddcombine(self,other):
        pass

    @abstractmethod
    def __add__(self, other):
        pass
    def __radd__(self, other):
        return self+other
    def __sub__(self,other):
        return self + other.__neg__()
    def __rsub__(self,other):
        return self.__neg__() + other
    
    def __neg__(self):
        return -1 * self

    @abstractmethod
    def __mul__(self, other):
        pass
    def __rmul__(self, other):
        return self * other
    def __pow__(self, other):
        if (isinstance(other, int)):
            if other == 0:
                return 1
            elif other < 0:
                return 1/(self ** (-other))
            a = self.copy()
            for i in range(other-1):
                a = a * self
            return a
        return NotImplemented
        
    
    def __truediv__(self, other):
        return self * (1/other)
    
    @abstractmethod
    def oneoverself(self):
        pass

    def __rtruediv__(self, other):
        return other * self.oneoverself()
    
    @abstractmethod
    def equalszero(self):
        pass

    def __eq__(self, other):
        if not (isinstance(other, MathInterface) or isinstance(other, Number)):
            return False
        #print('Callfromeq', type(self))
        simp = self.simplified()
        
        if other == 0:
            if isinstance(simp, Number):
                return simp == 0
            return simp.equalszero()
        return simp-other == 0