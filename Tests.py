from Polynomial import Polynomial
from RationalFunction import RationalFunction
from MathTerm import MathTerm
from numbers import Number
from MNumber import MNumber
from Variable import Variable

x = Variable('x')

def asserteq(a,b):
    try:
        assert a == b
    except AssertionError:
        print('Assertion error!')
        print(a,'==',b,'(',type(a),type(b),')')
        try:
            print(a.simplified()== b.simplified())
            print(a-b,'== 0')
        except:
            pass
        exit()
a = (x/(x-1))
b = 1/(x-1)

asserteq(MathTerm(2)*(Variable('x')), 2*x)

asserteq(x-1,x-1)
a = 6/(5*x-2)
b = (5*x-9)/(7*x**2+7)
c = 6*x+1
n = (67*x**2-55*x+60)
d = (5*x-2)*(7*x**2+7)
asserteq(a, 6*(1/(5*x-2)))
asserteq(a/c,6/(30*x**2 - 7*x - 2))
asserteq(a+b, (67*x**2-55*x+60)/((5*x-2)*(7*x**2+7)))
asserteq(a*b, (30*x - 54)/(35*x**3 + 35*x - 14*x**2 - 14))
asserteq(a.derivative('x'),-30/(5*x-2)**2)
asserteq(a.evaluate('x',1),2)
asserteq(a+1, (4+5*x)/(5*x-2))
asserteq(a+MathTerm(1), (4+5*x)/(5*x-2))
asserteq(a*MathTerm(2)*Polynomial(3), 6*a)
asserteq(a.simplified(), 6*(1/(5*x-2)))
asserteq((1/(x**2+1)).derivative('x'),-2*x/(x**4+2*x**2+1))

asserteq(Variable('x')**1,Variable('x'))

rt = x-1
ex = rt**2
rd = rt + 2

asserteq(rd, x + 1)
asserteq(ex , x**2 - 2*x +1)

big = (rt**16+rt**3+rd**3)/(rt**5+rd**22)
asserteq(ex/rt, rt)
asserteq(1/(1/rt),rt)
asserteq(ex/rd, (x**2-2*x+1)/(x+1))
asserteq(a.derivative('x'),-30/(25*x**2-20*x+4))
#print(a,'deriv->',a.derivative('x'))
#print(big,'derivative->',big.derivative('x'))
asserteq(x-x,0)
r = Variable('r')
asserteq(r-r,x-x)

asserteq((2*r)/(2*r**2),1/r)
asserteq((r**2 * (2*r**2)), 2*r**4)
asserteq(r**2 * (2*r)**2, 4*r**4)

asserteq(len((r*r).terms),1)

asserteq((x*r**2).derivative('r').derivative('x').evaluate('r,x',0).evaluate('x,r',0),2*r)

try:
    cookies = int(open('CRITICAL_DATA.txt','r').read())
except:
    cookies = 0
cookies += 1
onedigitmap = ['th','st','nd','rd','th','th','th','th','th','th']
digitmap = onedigitmap + ['th']*10 + onedigitmap+ onedigitmap+ onedigitmap+ onedigitmap+ onedigitmap+ onedigitmap+ onedigitmap+ onedigitmap+ onedigitmap+ onedigitmap
print('\nall tests passed! You earned your '+str(cookies)+digitmap[int(str(cookies)[-2:])]+' cookie\n')
with open('CRITICAL_DATA.txt','w+') as file:
    file.write(str(cookies))