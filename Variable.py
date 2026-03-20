from MathInterface import MathInterface

class Variable(MathInterface):
    def __init__(self, arg):
        self.var = arg
    
    def __repr__(self):
        return self.var
    
    def copy(self):
        return Variable(self.var)
    
    def latex(self):
        if ',' not in self.var:
            return self.var
        elif self.var[-2] == ',':
            return self.var[0:-1]+'_'+self.var[-1]
        else:
            splt = self.var.split(',')
            return splt[0] + ',_{' + splt[1][1:-1] + '}'

    def derivative(self, respectto):
        if self.var == respectto:
            return MNumber(1)
        elif self.var[0] == respectto:
            return MNumber(0)
        if ',' not in self.var:
            return Variable(self.var +','+respectto)
        elif self.var[-2] == ',':
            l = [self.var[-1],respectto]
            l.sort()
            return Variable(self.var[0:-2]+',('+''.join(l)+')')
        else:
            splt = self.var.split(',')
            assert len(splt) == 2
            backterms = list(splt[1][1:-1])
            backterms.append(respectto)
            backterms.sort()
            return Variable(splt[0] + ',('+''.join(backterms)+')')

    def evaluate(self, var, value):
        if var == self.var:
            return value
        return self.copy()

    def canaddcombine(self, other):
        if isinstance(other, Variable):
            return other.var == self.var
        elif isinstance(other, Polynomial):
            return True
        elif isinstance(other, MathTerm):
            return other.canaddcombine(self)
        return False
    
    def __add__(self, other):
        if isinstance(other, Number):
            other = MNumber(other)

        if not self.canaddcombine(other):
            return Polynomial(terms=[self.copy(),other.copy()])
        #Can be combined with other
        elif isinstance(other, Variable):
            return self * 2
        return NotImplemented
    
    def equalszero(self):
        return False

    def __mul__(self, other):
        if isinstance(other, Number):
            other = MNumber(other)

        if isinstance(other, MathTerm):
            return NotImplemented
        mt = MathTerm(self)
        mt *= other
        return mt
        
    def oneoverself(self):
        mt = MathTerm(self)
        return 1/mt
    
    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.var == other.var
        return super().__eq__(other)


from Polynomial import Polynomial
from MathTerm import MathTerm
from MNumber import MNumber
from numbers import Number
a = Variable('x')
