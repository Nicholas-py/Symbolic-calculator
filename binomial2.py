import sys
from MathTerm import MathTerm
from Polynomial import Polynomial

ot = sys.stdout
numberchars = '0123456789.'
mischars = ',()\'"=-+'
powerchars = '⁰¹²³⁴⁵⁶⁷⁸⁹'
print(powerchars)




def dobinomial():
    while True:
        inp1, inp2 = input("Enter the binomial: "), int(input("What power to raise it to? ").strip())
        sys.stdout = open("log.txt", "a+", encoding='utf-8')
        a = Polynomial(inp1)**inp2
        sys.stdout = ot
        print(str(a))

def dodivision():
    while True:
        inp1 = Polynomial(input("Enter the first polynomial: "))
        inp2 = Polynomial(input("Enter the second polynomial: "))
        print(inp1/inp2)


if 'b' in input("Which command do you want to run? "):
    dobinomial()
else:
    dodivision()