import Polynomial
Ex = Polynomial.Polynomial
from Variable import Variable
from MathTerm import MathTerm
import matplotlib.pyplot as plt
from numbers import Number
from time import time
tim = time()
coordnames = 'rθ'

substitutes = {'(R+rsin(θ))':'@','sin(θ)':'&','cos(θ)':'#'}
inversesubs = {}
for i in substitutes:
    inversesubs[substitutes[i]] = i
r = Variable('r')
t = Variable('t')
theta = Variable('θ')
#g_ab, not g^ab
# metric = [
  #  [-1, 0, 0, 0],
   # [0, 1, 0, 0],
    #[0, 0, Variable('b')**2, 0],
    #[0, 0, 0, Variable('r')**2]
#]
#[[θ²,0],[0,r²]] -> cool!
#[[-1,0],[0,r²]] -> hyperbolic coords?
metric = [[1,0],
          [0,1+r**2]]
dim = 2
constantcoords = ''

def grderiv(expression, respectto):
    if isinstance(respectto, Number):
        respectto = coordnames[respectto]
    if respectto not in coordnames:
        raise Exception("Derivative with respect to something weird: "+respectto)
    if respectto in constantcoords:
        return 0
    if isinstance(expression, Number):
        return 0
    exp =  expression.derivative(respectto)
    for i in coordnames:
        for j in coordnames:
            if i != j:
                exp = exp.evaluate(i+','+j,0)
    return exp

def expressionify(metric):
    for i in range(dim):
        for j in range(dim):
            m = metric[i][j]
            if type(metric[i][j]) == str:
                for k in substitutes:
                    m = m.replace(k, substitutes[k])
                if m[1:] == '^2':
                    m = Ex(m[0])
                    m = m**2
                elif m[0] == '(' and m[-3:] == ')^2':
                    m = Ex(m[1:-3])
                    m = m**2
                else:
                    m = Ex(m)
            else:
                m = Ex(m)
            metric[i][j] = m
    return metric

#metric=expressionify(metric)


def p(metric, xoffset = 0,yoffset=0, xgap = 1, ygap = 1):
    plt.scatter([-1+xoffset,(dim+1)*xgap+xoffset],[-1+yoffset,(dim+1)*ygap+yoffset])
    for i in range(dim):
        for j in range(dim):
            if isinstance(metric[i][j], Number):
                txt = '$'+str(metric[i][j])+'$'
            else:
                txt = '$'+metric[i][j].latex()+'$'
            for s in inversesubs:
                txt = txt.replace(s, inversesubs[s])
            plt.text(xoffset+xgap*i,yoffset+ygap*(dim-j),txt)

def pf(func,xoffset = 0,yoffset=0, xgap = 1, ygap = 1):
    plt.scatter([-1+xoffset,(dim+1)*xgap+xoffset],[-1+yoffset,(dim+1)*ygap+yoffset])
    for i in range(dim):
        for j in range(dim):
            val = func(i,j)
            if isinstance(val, Number):
                txt = '$'+str(val)+'$'
            else:
                txt = '$'+val.latex()+'$'
            for s in inversesubs:
                txt = txt.replace(s, inversesubs[s])
            plt.text(xoffset+xgap*i,yoffset+ygap*(dim-j),txt)


def mderiv(a,b, u):
    return grderiv(metric[a][b],coordnames[u])

def display(expr):
    txt = '$'+expr.latex()+'$'
    for s in inversesubs:
        txt = txt.replace(s, inversesubs[s])
    plt.text(0,0,txt)
    plt.show()


#p(metric)

christoffels = [[[None for u in range(dim)] for a in range(dim)] for b in range(dim)]

#chris^u_ab = 1/2 * g^uc(g_ac,b+g_bc,a-g_ab,c)
def christoffel(u,a,b):
    if christoffels[u][a][b] is not None:
        return christoffels[u][a][b]
    suum = Ex()
    for c in range(dim):
        if metric[c][u] == 0:
            gup = 0
        else:
            gup = 1/metric[c][u]
        base = mderiv(a,c,b)+mderiv(b,c,a)-mderiv(a,b,c)
        suum += gup * base * 0.5
    suum = suum.simplified()
    christoffels[u][a][b] = suum
    return suum

#a= (christoffel(3,1,3))
for u in range(dim):
    for a in range(dim):
        for b in range(dim):
            try:
                assert christoffel(u,a,b) == christoffel(u,b,a)
            except AssertionError:
                print('CHRISTOFFEL FAIL')
                print(u,a,b)
                one = christoffel(u,a,b)
                two = christoffel(u,b,a)
                three = one-two
                print(one,two, three)
                print(three)
                print()
                exit()
#christoffelrivs = [[[[grderiv(christoffel(a,b,u),coordnames[v]) for u in range(dim)] for a in range(dim)] for b in range(dim)] for v in range(dim)]





riemannups = [[[[None for _ in range(dim)] for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
riemanndowns = [[[[None for _ in range(dim)] for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
#Riemann^a_buv = CH^a_bv,u - CH^a_bu,v + CH^a_uc CH^c_bv - CH^a_vc CH^c_bu
def Riemannup(a,b,u,v):
    if riemannups[a][b][u][v] is not None:
        return riemannups[a][b][u][v]
    suum = Ex()
    suum += grderiv(christoffel(a,b,v),u)
    suum -= grderiv(christoffel(a,b,u),v)
    for c in range(dim):
        suum += christoffel(a,u,c)*christoffel(c,b,v)
        suum -= christoffel(a,v,c)*christoffel(c,b,u)
    riemannups[a][b][u][v] = suum.simplified()
    return suum.simplified()

#R_abuv = g_acR^c_buv
def Riemanndown(a,b,u,v):
    if riemanndowns[a][b][u][v] is not None:
        return riemanndowns[a][b][u][v]
    suum = Ex()
    for c in range(dim):
        #print(suum, metric[a][c], Riemannup(c,b,u,v))
        suum += metric[a][c] * Riemannup(c,b,u,v)
    riemanndowns[a][b][u][v] = suum.simplified()
    return suum.simplified()

#print(metric[1][1], type(metric[1][1].terms[0].terms[1].term))
print(Riemanndown(1,0,1,0))
#exit()
for i in range(dim):
    for j in range(dim):
        for k in range(dim):
            for l in range(dim):
                try:
                    assert Riemanndown(i,j,k,l) == Riemanndown(k,l,i,j)
                    assert Riemanndown(i,j,k,l) == -Riemanndown(j,i,k,l)
                    assert Riemanndown(i,j,k,l) == -Riemanndown(i,j,l,k)
                except AssertionError:
                    print('RIEMANN ERROR')
                    a = Riemanndown(i,j,k,l)
                    b = Riemanndown(k,l,i,j)
                    c = -Riemanndown(j,i,k,l)
                    d = -Riemanndown(i,j,l,k)
                    print(i,j,k,l)
                    print((a-b).simplified(),'==',0)
                    print((a-c).simplified(),'==',0)
                    print(a,'-',c)
                    print((a-d).simplified(),'==',0)
                    exit()
#print(time()-tim)

def Riccidown(a,b):
    suum = Ex()
    for c in range(dim):
        suum += Riemannup(c,a,c,b)
    return suum.simplified()

ricciscalar = 0
for i in range(dim):
    for j in range(dim):
        ricciscalar += Riccidown(i,j) * metric[i][j]
ricciscalar = ricciscalar.simplified()

if __name__ == '__main__':
    for i in range(dim):
        p(christoffels[i],10*i,0,1.5)

    plt.show()

    pf(lambda x,y:Riemanndown(0,1,x,y))
    pf(Riccidown, xoffset=10)
    print('R =',ricciscalar)
    plt.show()
    print('done"')