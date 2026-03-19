
def getnumdenom(obj):
    denominator = MNumber(1)
    if isinstance(obj, RationalFunction):
        numerator = obj.numerator.copy()
        if obj.denominator:
            denominator = obj.denominator.copy()
    else:
        numerator = obj.copy()
    while True:
        if isinstance(numerator, RationalFunction):
            denominator *= numerator.denominator
            numerator = numerator.numerator
        elif isinstance(denominator, RationalFunction):
            numerator *= denominator.denominator
            denominator = denominator.numerator
        else:
            break
    return numerator, denominator

def removerationalsfrom(nterms, dterms):
    for i in range(len(nterms)):
        if isinstance(nterms[i], RationalFunction):
            for j in range(len(nterms)):
                if i != j:
                    nterms[j] *= nterms[i].denominator
            for j in range(len(dterms)):
                dterms[j] *= nterms[i].denominator
            nterms[i] = nterms[i].numerator
            return True
    return False

def removepolynomialsfrom(nterms):
    for i in range(len(nterms)):
        if isinstance(nterms[i], Polynomial):
            for j in nterms[i].terms:
                nterms.append(j)
            nterms.pop(i)
            return True
    return False

def simplifymathterms(nterms):
    for i in range(len(nterms)):
        if isinstance(nterms[i], MathTerm):
            for j in range(len(nterms[i].terms)):
                item = nterms[i].terms[j].term
                if isinstance(item, Polynomial):
                    pol = item ** (nterms[i].terms[j].power)
                    nterms[i].terms.pop(j)
                    nterms[i] = pol * nterms[i]
                    return True
                elif isinstance(item, RationalFunction):
                    tp = nterms[i].terms.pop(j)
                    rat = (tp.term **tp.power)
                    nterms[i] = rat * nterms[i]
                    return True
                elif isinstance(item, MathTerm):
                    pow = nterms[i].terms[j].power
                    nterms[i].terms.pop(j)
                    for trm in item.terms:
                        texpr, tpow = trm.term, trm.power
                        tpow *= pow
                        nterms[i].terms.append(TermPower(texpr, tpow))
                    return True
                elif isinstance(item, MNumber):
                    nterms[i].terms.pop(j)
                    nterms[i].coefficient *= item.val
                    return True
    return False

def combinemathterms(mathterm):
    used = set()
    for i in range(len(mathterm.terms)):
        for j in range(i+1,len(mathterm.terms)):
            if j not in used and i not in used and mathterm.terms[i] == mathterm.terms[j]:
                mathterm.terms[i].power += mathterm.terms[j].power
                used.add(j)
    for i in range(len(mathterm.terms)):
        if mathterm.terms[i].power == 0:
            used.add(i)
    for i, item in enumerate(sorted(used)):
        mathterm.terms.pop(item-i)

def matches(mt1, mt2):
    for i in mt1.terms:
        for j in mt2.terms:
            if i.term == j.term and i.power == j.power:
                break
        else:
            return False
    return True


def combineaddterms(polylist):
    used = set()
    for i in range(len(polylist)):
        if not isinstance(polylist[i], MathTerm):
            polylist[i] = MathTerm(polylist[i])

    for i in range(len(polylist)):
        for j in range(i+1,len(polylist)):
            if i in used or j in used:
                continue
            if matches(polylist[i], polylist[j]) and matches(polylist[j], polylist[i]):
                polylist[i].coefficient += polylist[j].coefficient
                used.add(j)

    for i in range(len(polylist)):
        if polylist[i].coefficient == 0:
            used.add(i)
    print(polylist, used)
    for i, item in enumerate(sorted(used)):
        print(i, item)
        polylist.pop(item-i)
    

    for i in range(len(polylist)):
        if len(polylist[i].terms) == 1 and polylist[i].terms[0].power == 1 and polylist[i].coefficient == 1:
            polylist[i] = polylist[i].terms[0].term
        elif len(polylist[i].terms) == 0:
            polylist[i] = MNumber(polylist[i].coefficient)


def candivide(term, divisor):
    if isinstance(term, MFunction):
        if not isinstance(divisor, MFunction):
            return False
        return term == divisor
    elif isinstance(term,MNumber):
        return isinstance(divisor, MNumber) and (term/divisor).val %1 == 0
    elif isinstance(term, MathTerm):
        for subterm in term.terms:
            if subterm.term == divisor:
                return True
        return False
    else:
        return False

        


def findcommondivisor(nterms, dterms):
    pastchecked = set()
    queue = []
    for term in dterms:
        if isinstance(term, MFunction):
            queue.append(term)
        elif isinstance(term, MathTerm):
            for subterm in term.terms:
                queue.append(subterm.term)
        else:
            return None
    for element in queue:
        if str(element) in pastchecked:
            continue
        else:
            pastchecked.add(str(element))
            for term in nterms+dterms:
                if not candivide(term, element):
                    break
            else:
                return element
    

    

def commondivide(terms, divisor):
    
    for i in range(len(terms)):
        term = terms[i]
        assert candivide(term, divisor)
        if isinstance(term, MFunction):
            terms[i] = 1
        elif isinstance(term, MathTerm):
            for j,subterm in enumerate(term.terms):
                if subterm.term == divisor:
                    subterm.power -= 1
                    if subterm.power == 0:
                        term.terms.pop(j)
                    break
                
            else:
                raise TypeError('Not found')
        elif isinstance(term, MNumber):
            assert isinstance(divisor, MNumber)
            terms[i] = terms[i]/divisor
        else:
            raise TypeError("Incorrect type when dividing")



def simplify(obj):
    numerator, denominator = getnumdenom(obj)
    assert not isinstance(numerator, RationalFunction)
    assert not isinstance(denominator, RationalFunction)

    if not isinstance(numerator, Polynomial):
        numerator = Polynomial(numerator)
    if not isinstance(denominator, Polynomial):
        denominator = Polynomial(denominator)
    

    nterms = numerator.terms
    dterms = denominator.terms
    while True:
        if removerationalsfrom(nterms,dterms):
            continue
        if removerationalsfrom(dterms, nterms):
            continue
        if removepolynomialsfrom(nterms):
            continue
        if removepolynomialsfrom(dterms):
            continue
        if simplifymathterms(nterms):
            continue
        if simplifymathterms(dterms):
            continue
        break

    for i in nterms+dterms:
        if isinstance(i,MFunction):
            i.contents = simplify(i.contents)
    
    for i in nterms+dterms:
        if isinstance(i, MathTerm):
            combinemathterms(i)
    
    combineaddterms(nterms)
    combineaddterms(dterms)

    while True:
        commondiv = findcommondivisor(nterms, dterms)
        if commondiv is not None:
            commondivide(nterms, commondiv)
            commondivide(dterms, commondiv)
        else:
            break

    if len(dterms) == 0:
        raise ZeroDivisionError('Division by 0 after simplifying')
    if len(nterms) == 0:
        return MNumber(0)

    numerator = Polynomial(nterms)
    denominator = Polynomial(dterms)

    if len(denominator.terms) == 1:
        denominator = denominator.terms[0]
    if len(numerator.terms) == 1:
        numerator = numerator.terms[0]

    if denominator == MNumber(1):
        return numerator
    return RationalFunction([numerator, denominator])


from Polynomial import Polynomial
from RationalFunction import RationalFunction
from MathTerm import MathTerm, TermPower
from MathInterface import MathInterface
from MNumber import MNumber
from Variable import Variable
from Function import MFunction

