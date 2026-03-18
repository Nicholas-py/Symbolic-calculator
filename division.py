from Polynomial import Polynomial
from MathTerm import MathTerm

def longdivide(dividend, divisor):

    if len(divisor.terms) == 1:
        new = dividend.copy()
        for i in range(len(new.terms)):
            new.terms[i] /= divisor.terms[0]
        return (new,0)

    raise SyntaxError('This method doesn\'t work anymore. Try again another day')
    dividend, divisor =  sort(dividend), sort(divisor)

    vari = list(dividend.terms[0].variables.keys())[0]
    vari2 = list(divisor.terms[0].variables.keys())[0]
    #assert vari == vari2

    dividenddegree = dividend.terms[0].variables[vari]
    divisordegree = divisor.terms[0].variables[vari]
    #assert divisordegree < dividenddegree

    result = Polynomial()
    for i in range(dividenddegree-divisordegree+1):
        factor0 = dividend.terms[0]/divisor.terms[0]
        result += factor0
        dividend -= divisor * factor0
        dividend.combineterms()
        dividend.clearzeroes()
    result.clearzeroes()
    return result, dividend


def sort(expression):
    sortedterms = {}
    vari = list(expression.terms[0].variables.keys())[0]
    for i in expression.terms:
        if len(i.variables) > 1 or (len(i.variables) == 1 and vari not in i.variables):
            return NotImplemented
        elif len(i.variables) == 0:
            sortedterms[str(i)] = 0
        else:
            new = i.copy()
            sortedterms[str(new)] = new.variables[vari]
    newdict = dict(sorted(sortedterms.items(), key=lambda item: -item[1]))
    ex = Polynomial()
    for i in newdict:
        ex += MathTerm(i)
    return ex
            

if __name__ == '__main__':

    mt = Polynomial('x²-2x+1')
    mt2 = Polynomial('x-3')
    mt3 = Polynomial('2x-6')
    print((mt/mt2))
    print(mt2/mt3)
