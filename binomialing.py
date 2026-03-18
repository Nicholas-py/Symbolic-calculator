


def choose(n,k):
    return int(factorial(n)/(factorial(k)*factorial(n-k)))

def factorial(n):
    product = 1
    for i in range(1,n+1):
        product *= i
    return product



def binomial(ex, power):
    return binomialrecurse(ex, power)

def binomialrecurse(ex, power):
    #print('currentargs',ex,power)
    #print('(')
    if ex.terms == []:
        #print("Emtyp arg return)")
        return None
    if power == 1:
        #print('boop)')
        return ex
    if power == 0:
        #print('NULLL)')
        return None
    print('BINOMIALLLLLLLLLLLLLLLLLL')
    t1 = ex.pop(0)
    if ex.terms == []:
        return Polynomial(str(t1**power))
    answer = None
    for i in range(power+1):
        pascal = choose(power, i)
        part1 = t1**(power-i)
        part2 = binomialrecurse(Polynomial(str(ex)), i)
        factor = pascal*part1
        sub = factor*part2
        if answer == None:
            answer = Polynomial(str(sub))
        else:
            answer= answer + sub
    return answer


from Polynomial import Polynomial
