import sys
from MathTerm import MathTerm
from Polynomial import Polynomial
from RationalFunction import RationalFunction
ot = sys.stdout
numberchars = '0123456789.'
mischars = ',()\'"=-+'
powerchars = '⁰¹²³⁴⁵⁶⁷⁸⁹'
print(powerchars)


a = RationalFunction('2x/y')*MathTerm('y')
b = RationalFunction('2x/y')*MathTerm('y')
print(a,b,a-b)

exit()

while True:
    inp1, inp2 = input("Enter the binomial: "), int(input("What power to raise it to? ").strip())
    sys.stdout = open("log.txt", "a+", encoding='utf-8')
    a = Polynomial(inp1)**inp2
    sys.stdout = ot
    print(str(a))
