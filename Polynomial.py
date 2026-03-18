from MathInterface import MathInterface


numberchars = '0123456789.'
mischars = ',()\'"=-+'
powerchars = '⁰¹²³⁴⁵⁶⁷⁸⁹'


class Polynomial(MathInterface):
    def __init__(self, string='', terms = []):
        if isinstance(string, Number):
            self.terms = [MathTerm(string)]
        elif string != '':
            self.terms = self.getterms(string)
            self.combineterms()
        elif terms != []:
            for i in range(len(terms)):
                if isinstance(terms[i], Number):
                    terms[i] = MNumber(terms[i])
            self.terms = terms
        else:
            self.terms = []

    def getterms(self, string):
        if string == '':
            return []
        if '(' in string:
            raise SyntaxError("Brackets not supported")
        ex = string.replace(' ','')
        ex = ex[0] + ex[1:].replace('-', '+-')
        split = ex.split('+')
        for i in range(len(split)):
            split[i]= MathTerm(split[i])
        return split
    
    def copy(self):
        new = Polynomial()
        for i in self.terms:
            new.terms.append(i.copy())
        return new
    
    def combineterms(self):
        new = Polynomial()
        for i in self.terms:
            for j in range(len(new.terms)):
                if new.terms[j].canaddcombine(i):
                    new.terms[j] = (new.terms[j]+i).simplified()
                    if new.terms[j] == 0:
                        new.terms.pop(j)
                    break
            else:
                new = new+ i
        self.terms = new.terms

    def removepolynomials(self):
        toadds = []
        j = 0
        for i in range(len(self.terms)):
            if isinstance(self.terms[i-j], Polynomial):
                toadds.append(self.terms.pop(i-j))
                j += 1
        for i in toadds:
            for j in i.terms:
                for k in range(len(self.terms)):
                    if self.terms[k].canaddcombine(j):
                        self.terms[k] += j
                        break
                else:
                    self.terms.append(j)


    def clearzeroes(self):
        j = 0
        for i in range(len(self.terms)):
            if self.terms[i-j] == 0:
                self.terms.pop(i-j)
                j += 1
    
    def canaddcombine(self, other):
        return True
        

    def simplified(self):
        c = self.copy()
        for i in range(len(c.terms)):
            c.terms[i] = c.terms[i].simplified()
        c.removepolynomials()
        c.combineterms()
        c.removepolynomials()
        c.combineterms()
        c.clearzeroes()

        if len(c.terms) == 0:
            return MNumber(0)
        if len(c.terms) == 1:
            return c.terms[0]
        return c

    def __mul__(self,other):
        if other == 0:
            return MNumber(0)
        if isinstance(other, RationalFunction):
            return NotImplemented
        elif isinstance(other, MathInterface):
            new = Polynomial()
            for i in self.terms:
                new += other*i
            new = new.simplified()
            return new
        elif isinstance(other, Number):
            new = Polynomial()
            for i in self.terms:
                new.terms.append(i * other)
            return new
        return NotImplemented
                    
    def __imul__(self,other):
        self.terms = (self*other).terms
        return self

    def __repr__(self, latex = False):
        #self.simplify()
        if self.terms == []:
            return '0'
        string = ''
        for n in range(len(self.terms)):
            i = self.terms[n]
            if (not ((isinstance(i, MathTerm) and i.coefficient <= 0) or (isinstance(i,MNumber) and i.val < 0))) and n != 0:
                string += '+'
            if latex:
                string += i.latex()
            else:
                string += str(i)
        if len(string) == 0:
            return ''
        string = string.replace('+', ' + ')
        string = string[0] + string[1:].replace('-',' - ')
        return string
    
    def latex(self):
        return self.__repr__(latex = True)     

    def __add__(self,other):
        if other == 0:
            return self.copy()
        new = self.copy()
        
        if type(other) == Polynomial:
            new.terms += other.copy().terms
            return new
        
        if isinstance(other, MathInterface):
            # for i in range(len(new.terms)):
            #     if other.canaddcombine(new.terms[i]):
            #         new.terms[i] += other
            #         break
            # else:      
            new.terms.append(other)
            return new
        if isinstance(other, Number):
            return self + MathTerm(other)
        return NotImplemented
    
    def oneoverself(self):
        return RationalFunction([MNumber(1),self])

    def equalszero(self):
        return self.terms == []

    def __getitem__(self, index):
        return self.terms[index]

    def pop(self, index):
        return self.terms.pop(index)
    
    def __iter__(self):
        return self.terms.__iter__()
    
    def evaluate(self,var, value):
        a = Polynomial()
        for i in self.terms:
            a += i.evaluate(var,value)
        return a
    
    def derivative(self, respectto):
        suum = Polynomial()
        for i in self.terms:
            suum += i.derivative(respectto)
        return suum

from RationalFunction import RationalFunction
from MathTerm import MathTerm
from numbers import Number
from MNumber import MNumber


