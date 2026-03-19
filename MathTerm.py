powerchars = '⁰¹²³⁴⁵⁶⁷⁸⁹'
numberchars = '0123456789.'
mischars = '⁻,()\'"=-+'
from MathInterface import MathInterface
from numbers import Number

class TermPower:
    def __init__(self, term:MathInterface, power:Number):
        self.term = term
        self.power = power
    def copy(self):
        return TermPower(self.term.copy(),self.power)


class MathTerm(MathInterface):
    def __init__(self, arg=''):
        if isinstance(arg, Number):
            self.coefficient = arg
            self.terms = []
        elif arg == '':
            self.coefficient, self.terms = 1, []
        elif isinstance(arg, list):
            self.coefficient, self.terms = 1, []
            for i in arg:
                self *= i
        elif isinstance(arg, MathInterface):
            self.coefficient = 1
            self.terms = [TermPower(arg.copy(), 1)]
        else:
            raise TypeError('Cannot pass type '+str(type(arg))+' to MathTerm')
            self.coefficient, self.terms = MathTerm.parse(arg)
    def __repr__(self):
        if self.coefficient == 1 and self.terms == []:
            return '1'
        if self.coefficient == -1 and self.terms == []:
            return '-1'
        string = ''
        for i in self.terms:
            mypower = i.power
            if abs(mypower) >= 1:
                string += str(i.term)
            if mypower <= -1:
                string += '⁻'
                for j in str(mypower)[1:]:
                    string += powerchars[int(j)]

            if mypower >= 2:
                for j in str(mypower):
                    string += powerchars[int(j)]
        if self.coefficient == int(self.coefficient):
            self.coefficient = int(self.coefficient)
        strco = str(self.coefficient)
        if self.coefficient == 1:
            strco = ''
        elif self.coefficient == -1:
            strco = '-'
        return strco+string

    def latex(self):
        if self.coefficient == 1 and not self.terms:
            return '1'
        if self.coefficient == -1 and not self.terms:
            return '-1'
        string = ''
        for i in self.terms:
            mypower = i.power
            if mypower >= 1:
                string += i.term.latex()
                if mypower >= 2:
                    string += '^{'+str(mypower)+'}'
        overs = ''
        for i in self.terms:
            mypower = i.power
            if mypower <= -1:
                overs += i.term.latex()
                if mypower <= -2:
                    overs += '^{'+str(-mypower)+'}'
        if overs:
            if not string:
                string = '1'
            string = '\\frac{'+string+'}{'+overs+'}'

        if self.coefficient == int(self.coefficient):
            self.coefficient = int(self.coefficient)
        strco = str(self.coefficient)
        if self.coefficient == 1:
            strco = ''
        elif self.coefficient == -1:
            strco = '-'
        return strco+string


    def __mul__(self, other):
        if isinstance(other, MathTerm):
            new = self.copy()
            for i in other.terms:
                for j in new.terms:
                    if i.term.canaddcombine(j.term):
                        j.power += i.power
                        break
                else:
                    new.terms.append(i.copy())
            new.coefficient *= other.coefficient
            return new
        elif isinstance(other, MNumber):
            a = self.copy()
            a.coefficient *= other.val
            return a
        elif isinstance(other, RationalFunction) or isinstance(other, Polynomial):
            return NotImplemented
        elif isinstance(other, Variable):
            self = self.copy()
            for i in self.terms:
                if i.term.canaddcombine(other):
                    i.power += 1
                    break
            else:
                self.terms.append(TermPower(other,1))
            return self
        elif isinstance(other, MathInterface):
            new = self.copy()
            new.terms.append(TermPower(other,1)) 
            return new           
        else:
            try:
                new = self.copy()
                new.coefficient *= float(other)
                return new
            except TypeError:
                return NotImplemented
                
    def __pow__(self, number):
        if number == 0:
            return 1
        basemt = self.copy()
        mt = self.copy()
        for i in range(number-1):
            mt *= basemt
        return mt
    
    def oneoverself(self):
        a = self.copy()
        for i in a.terms:
            i.power *= -1
        a.coefficient = 1/a.coefficient
        return a

    def equalszero(self):
        return self.coefficient == 0

    def simplified(self):
        self = self.copy()
        
        for i in range(len(self.terms)):
            self.terms[i].term = self.terms[i].term.simplified()

        tokill = []
        for i in range(len(self.terms)):
            if isinstance(self.terms[i].term, MathTerm) or isinstance(self.terms[i].term,MNumber) or isinstance(self.terms[i].term, Polynomial):
                tokill.append(i)
            
        savedcopy = self.copy()
        for i in range(len(tokill)):
            self.terms.pop(tokill[i]-i)
        for i in range(len(tokill)):
            tp = savedcopy.terms[tokill[i]]
            self = self * (tp.term)**(tp.power)
        tokill = []
        for i in range(len(self.terms)):
            for j in range(len(self.terms)):
                if i == j or i in tokill or j in tokill:
                    continue
                if self.terms[i].term.canaddcombine(self.terms[j].term):
                    self.terms[i].power += self.terms[j].power
                    self.terms[j].power = 0
                    tokill.append(j)

        for i in range(len(tokill)):
            self.terms.pop(tokill[i]-i)

        tokill = []
        for i in range(len(self.terms)):
            if self.terms[i].power == 0:
                tokill.append(i)
        for i in range(len(tokill)):
            self.terms.pop(tokill[i]-i)

        if self.coefficient == 0:
            return MNumber(0)
        if len(self.terms) == 0:
            return MNumber(self.coefficient)
        if len(self.terms) == 1 and self.terms[0].power == 1:
            return self.terms[0].term * self.coefficient
        return self
        

    def copy(self):
        new = MathTerm()
        new.coefficient = self.coefficient
        for i in self.terms:
            new.terms.append(TermPower(i.term.copy(), i.power))
        return new

    def parse(string):
        numbers, variables, powers = getnumbers(string), getvariables(string), getpowers(string)
        coef, varys =  powerify(string,numbers, variables, powers)
        if string[0] == '-':
            coef = -coef
        return coef, varys
    
    def canaddcombine(self,other):
        self = self.simplified()
        if not isinstance(self, MathTerm):
            return self.canaddcombine(other)
        other = other.simplified()
        if isinstance(other,MathTerm):
            for i in self.terms:
                for j in other.terms:
                    if i.term == j.term and i.power == j.power:
                        break
                else:
                    return False
            return True
        elif len(self.terms) == 1 and self.terms[0].power == 1 and isinstance(other,MathInterface):
            return self.terms[0].term.canaddcombine(other)
        return isinstance(other, Polynomial)
    
    def evaluate(self,var, value):
        prod = MathTerm(self.coefficient)
        for i in self.terms:
            prod *= (i.term.evaluate(var,value))**(i.power)
        if isinstance(prod, Number) or isinstance(prod, MNumber):
            return prod
        if len(prod.terms) == 0:
            return prod.coefficient
        return prod

    def __add__(self,other):
        if isinstance(other,MathTerm):
            if self.canaddcombine(other):
                a = self.copy()
                a.coefficient = self.coefficient + other.coefficient
                return a
            else:
                return Polynomial(terms=[self.copy(),other.copy()])
        if isinstance(other, Variable) and self.canaddcombine(other):
            a = self.copy()
            a.coefficient += 1
            return a
        elif isinstance(other, Polynomial) or isinstance(other, RationalFunction):
            return NotImplemented
        elif isinstance(other,MathInterface):
            return Polynomial(terms=[self.copy(),other.copy()])
        elif isinstance(other,Number):
            return Polynomial(terms=[self.copy(),MathTerm(other)])
        return NotImplemented
            
    def derivative(self, respectto):
        result = Polynomial()
        self = self.simplified()
        if type(self) != MathTerm:
            return self.derivative(respectto)
        for i in range(len(self.terms)):
            newterm = self.copy()
            power = newterm.terms[i].power
            term = newterm.terms[i].term
            if power == 1:
                newterm.terms.pop(i)
            else:
                newterm.coefficient *= power
                newterm.terms[i].power -= 1
            newterm *= term.derivative(respectto)
            result += newterm
        if result == 0:
            return MNumber(0)
        return result

        

def increasederivterm(string, respectto):
    if ',' not in string:
        return string +','+respectto
    elif string[-2] == ',':
        l = [string[-1],respectto]
        l.sort()
        return string[0:-2]+',('+''.join(l)+')'
    else:
        splt = string.split(',')
        assert len(splt) == 2
        backterms = list(splt[1][1:-1])
        backterms.append(respectto)
        backterms.sort()
        return splt[0] + ',('+''.join(backterms)+')'

def latexvar(string):
    if ',' not in string:
        return string
    elif string[-2] == ',':
        return string[0:-1]+'_'+string[-1]
    else:
        splt = string.split(',')
        if len(splt) > 2:
            raise ValueError('More than 1 comma per var')
        return splt[0] + ',_{' + splt[1][1:-1] + '}'

def getnumbers(string):
    string += ' '
    currentnumber = ''
    allnumbers = {}
    for i in range(len(string)):
        if string[i] in numberchars:
            currentnumber += string[i]
        else:
            if currentnumber != '':
                allnumbers[i] = float(currentnumber)
                currentnumber = ''
    return allnumbers


def getvariables(string):
    variables = {}
    for i in range(len(string)):
        
        if string[i] not in numberchars+mischars+powerchars and string[i-1] != ',':
            if string[i] in variables:
                variables[string[i]] += 1
            else:
                variables[string[i]] = 1
        elif string[i] == ',' and i != len(string)-1 and i != 0:
            if variables[string[i-1]] == 1:
                variables.pop(string[i-1])
            else:
                variables[string[i-1]] -= 1
            phrase = string[i-1:i+2]
            if phrase in variables:
                variables[phrase] += 1
            else:
                variables[phrase] = 1
    return variables

def getpowers(string):
    string = string + ' '
    currentnumber = ''
    allnumbers = {}
    for i in range(len(string)):
        if string[i] in powerchars+'⁻':
            currentnumber += string[i]
        else:
            if currentnumber != '':
                total = 0

                for j in range(len(currentnumber)):
                    if currentnumber[j] == '⁻':
                        total *= -1
                    else:
                        total += powerchars.index(currentnumber[j])*10**(len(currentnumber)-j-1)
                allnumbers[i-len(currentnumber)] = total
                currentnumber = ''
    return allnumbers

def product(lst):
    base = 1
    for i in lst:
        base *= i
    return base

def powerify(string, numbers, variables, powers):
    for i in powers:
        if i in numbers:
            numbers[i] = numbers[i] ** powers[i]
        else:
            var = string[i-1]
            variables[var] += powers[i]-len(str(powers[i]))
    return product(numbers.values()), variables



from Polynomial import Polynomial
from Variable import Variable
from MNumber import MNumber
from RationalFunction import RationalFunction