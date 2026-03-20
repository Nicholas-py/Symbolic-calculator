

from Christoffel import *
from MNumber import MNumber
coordnames = 'rθ'

print(coordnames,dim)

v1 = [1,0]
v2 = [0,1]
pos = (1,1)
vecdict = {pos:([pos[0],pos[1]],v1,v2)}
numsteps = 7

xcoords = [0]
ycoords = [0]


errors = []
steps = 1000
delta = 1/steps
#v^a;b = v^a,b + Γ^a_cb v^c
#v^a (t+delta) = v^a(t) -Γ^a_cb v^c * delta
def walk(dir,rtpos):
    if rtpos not in vecdict:
        raise Exception('not in vecdict')
    xypos,v1, v2 = vecdict[rtpos]
    #curpos = [pos[0],pos[1]]
    def ev(val):
        #print(val,curpos)
        for i in range(dim):
            if isinstance(val, Number):
                val = MNumber(val)
            val = val.evaluate(coordnames[i],rtpos[i])
        return float(val)

    for _ in range(steps):
        #print(i, curpos)
        if dir == 1:
            rtpos = [rtpos[0] + delta, rtpos[1]]
            xypos = [xypos[0]+delta*v1[0], xypos[1]+delta*v1[1]]
            dv1r = [delta*ev(christoffel(i,0,0)) for i in range(dim)]
            dv1x = dv1r[0] * v1[0] + dv1r[1] * v2[0]
            dv1y = dv1r[0] * v1[1] + dv1r[1] * v2[1]
            v1 = [v1[0] + dv1x, v1[1] + dv1y]
            dv2r = [ev(christoffel(i,1,0)) for i in range(dim)]
            dv2x = dv2r[0] * v1[0] + dv2r[1] * v2[0]
            dv2y = dv2r[0] * v1[1] + dv2r[1] * v2[1]
            v2 = [v2[0] + delta * dv2x, v2[1] + delta * dv2y]
        if dir == 2:
            rtpos = [rtpos[0], rtpos[1]+delta]
            xypos = [xypos[0]+delta*v2[0], xypos[1]+delta*v2[1]]
            dv1r = [delta*ev(christoffel(i,0,1)) for i in range(dim)]
            dv1x = dv1r[0] * v1[0] + dv1r[1] * v2[0]
            dv1y = dv1r[0] * v1[1] + dv1r[1] * v2[1]
            v1 = [v1[0] + dv1x, v1[1] + dv1y]
            dv2r = [ev(christoffel(i,1,1)) for i in range(dim)]
            dv2x = dv2r[0] * v1[0] + dv2r[1] * v2[0]
            dv2y = dv2r[0] * v1[1] + dv2r[1] * v2[1]
            v2 = [v2[0] + delta * dv2x, v2[1] + delta * dv2y]

        xcoords.append(xypos[0])
        ycoords.append(xypos[1])
    if (round(rtpos[0],5),round(rtpos[1],5)) in vecdict:
        a,b,c = vecdict[(round(rtpos[0],5),round(rtpos[1],5))]
        errors.append(((a[0]-xypos[0])**2+(a[1]-xypos[1])**2)**0.5)
    else:
        vecdict[(round(rtpos[0],5),round(rtpos[1],5))] = (xypos, v1,v2) 

try:
    for i in range(numsteps):
        walk(1,(i+pos[0],pos[1]))
        walk(2,(pos[0],i+pos[1]))
    for i in range(1,numsteps + 1):
        for j in range(numsteps):
            walk(2,(i+pos[0],j+pos[1]))
            walk(1,(j+pos[0],i+pos[1]))
    raise StopIteration('Done!')
except Exception as e:
    print(e)
    print(len(xcoords))
    if errors:
        print('Avg error: ',sum(errors)/len(errors))
    print('Ricci scalar:',ricciscalar)
    plt.scatter(xcoords,ycoords)
    plt.show()
    raise e