from Polynomial import Polynomial
from RationalFunction import RationalFunction
from MathTerm import MathTerm
from MathInterface import MathInterface
from MNumber import MNumber
from Variable import Variable
from Function import MFunction



def removerationalsfrom(nterms, dterms):
    for i in range(len(nterms)):
        if isinstance(nterms[i], RationalFunction):
            for j in range(len(nterms)):
                if i != j:
                    nterms[j] *= nterms[i].denominator
            for j in range(len(dterms)):
                dterms[j] *= nterms[i].denominator
            nterms[j] = nterms[j].numerator
            return False
    return True

def removepolynomialsfrom(nterms):
    for i in range(len(nterms)):
        if isinstance(nterms[i], Polynomial):
            for j in nterms[i].terms:
                nterms.append(j)
            nterms.pop(i)
            return False
    return True

def simplifymathterms(nterms):
    for i in range(len(nterms)):
        if isinstance(nterms[i], MathTerm):
            for j in range(len(nterms[i].terms)):
                item = nterms[i].terms[j].term
                if isinstance(item, Polynomial):
                    pol = item ** (nterms[i].terms[j].power)
                    nterms[i].terms.pop(j)
                    nterms[i] = pol * nterms[i]
                    return False
                elif isinstance(item, RationalFunction):
                    tp = nterms[i].terms.pop(j)
                    rat = (tp.term **tp.power)
                    nterms[i] = rat * nterms[i]
                    return False
                elif isinstance(item, MathTerm):
                    nterms[i].terms.pop(j)
                    for i in item.terms:
                        nterms[i].append(i)
                    return False
                elif isinstance(item, MNumber):
                    nterms[i].terms.pop(j)
                    nterms[i].coefficient *= item.val
                    return False
    return True

def combinemathterms(mathterm):
    used = {}
    for i in range(len(mathterm.terms)):
        for j in range(i+1,len(mathterm.terms)):
            if j not in used and i not in used and mathterm.terms[i] == mathterm.terms[j]:
                mathterm.terms[i].power += mathterm.terms[j].power
                used.add(j)
    for i, item in enumerate(used):
        mathterm.terms.pop(item-i)

def simplify(obj):
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
        else:
            break
    assert not isinstance(numerator, RationalFunction)
    assert not isinstance(denominator, RationalFunction)

    if not isinstance(numerator, Polynomial):
        numerator = Polynomial(numerator)
    if not isinstance(denominator, Polynomial):
        denominator = Polynomial(denominator)
    
    #Clear rational functions from the terms
    nterms = numerator.terms
    dterms = denominator.terms
    while True:
        if not removerationalsfrom(nterms,dterms):
            continue
        if not removerationalsfrom(dterms, nterms):
            continue
        if not removepolynomialsfrom(nterms):
            continue
        if not removepolynomialsfrom(dterms):
            continue
        if not simplifymathterms(nterms):
            continue
        if not simplifymathterms(dterms):
            continue
        break


    for i in nterms+dterms:
        if isinstance(i,MFunction):
            i.contents = simplify(i.contents)
    
    for i in nterms+dterms:
        if isinstance(i, MathTerm):
            combinemathterms(i)



    return RationalFunction([Polynomial(nterms),Polynomial(dterms)])




#x/(y/x) = 1/y
cursed = Polynomial(RationalFunction([Polynomial(MathTerm([Variable('x')])),RationalFunction([Polynomial(Variable('y')),Variable('x')])]))
print(cursed)
print(simplify(cursed))
print(cursed.simplified())
print(cursed)
