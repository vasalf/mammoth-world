#!/usr/bin/python3

from random import random

curiosity = 0.4 * 400
INF = 179179
const = 3
def test1(sign, claster):
    am = 1
    s_sign = [0]
    s_claster = [0]
    for i in range(len(sign)):
        s_sign.append(s_sign[-1] + sign[i])
        s_claster.append(s_claster[-1] + claster[i])
    for i in range(len(sign)):
        am += max(abs(sign[i] - claster[i]), 1) ** len(claster)
#    am /= len(sign) 
    return abs(am)

def summ(l):
    ans = 0
    for i in range(len(l)):
        ans += l[i] ** len(l)
    return ans

def test2(sign, claster):
    return abs(test1(sign, claster)) < curiosity ** 2

def join(a, b, am):
    res = a[:]
    for i in range(len(a)):
        res[i] = (am * res[i] + b[i]) / (am + 1)
    return res

def clasterize(signes):
    clasters = []
    paint = []
    for i in range(len(signes)):
        arr = []
        for j in range(len(clasters)):
#            print(signes, i, clasters[j])
            arr.append(test1(signes[i], clasters[j]))
        ind = -1
        mx = INF
        for j in range(len(clasters)):
            if arr[j] <= mx:
                if test2(signes[i], clasters[j]):
                    mx = arr[j]
                    ind = j
        if ind == -1:
            clasters.append(signes[i])
            paint.append(len(clasters) - 1)
        else:
            clasters[ind] = join(clasters[ind], signes[i], paint.count(ind))
            paint.append(ind)
        for i1 in range(i):
            arr = []
            for j in range(len(clasters)):
#                print(signes, i, clasters[j])
                arr.append(test1(signes[i1], clasters[j]))
            ind = -1
            mx = INF
            for j in range(len(clasters)):
                if arr[j] <= mx:
                    mx = arr[j]
                    ind = j
#            clasters[ind] = join(clasters[ind], signes[i], paint.count(ind))
            paint[i1] = ind

    return clasters, paint
        

                
fin = open("input.txt")
n = int(fin.readline().rstrip())
signes = [list(map(int, fin.readline().rstrip().split())) for i in range(n)]
#print(signes)
fin.close()
fout = open("input.txt", 'a')
print(file=fout)
print('\n'.join(map(str, clasterize(signes)[0])), file=fout)
print(file=fout)
print(' '.join(map(str, clasterize(signes)[1])), file=fout)
fout.close()
