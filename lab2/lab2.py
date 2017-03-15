#!/usr/bin/python3.6
from collections import defaultdict
from itertools import product
from functools import reduce
from math import log, ceil
from string import ascii_lowercase
from pprint import pprint, pformat


def to_probabilities(src):
    letters, count = zip(*src)
    probs = list(map(lambda x: float(x)/sum(count), count))
    return zip(letters, probs)


def source(str):
    d = defaultdict(lambda: 0)
    for c in str:
        d[c] += 1
    return list(d.items())


def source_extension(src, k):
    src = dict(to_probabilities(src))

    letters = list(zip(*src))[0]
    words = [''.join(i) for i in list(product(letters, repeat=k))]

    d = {}
    for w in words:
        p = 1
        for c in w:
            p *= src[c]
        d[w] = p

    return list(d.items())


def entropy_source(src):
    src = to_probabilities(src)

    H = 0
    for c, p in src:
        H += p*log(1/p, 2)

    return H


def mean_length(probs,C):
    L = map(lambda x: len(x[1]),C)
    return reduce(lambda x,y: x+y[0]*y[1], zip(probs,L), 0)


def shannon_code(src):
    src = to_probabilities(src)
    src = sorted(src, key=lambda x: x[1], reverse=True)

    letters, probs = map(list,zip(*src))
    L = list(map(lambda x: ceil(log(1/x,2)),probs)) # shannon code

    C = []
    q = ['']
    for n in range(max(L)+1):
        while L and L[0]==n:
            L.pop(0)
            x = q.pop(0)
            a = letters.pop(0)
            C.append((a,x))
        else:
            aux = []
            for x in q:
                aux.append(x+'0')
                aux.append(x+'1')
            q = aux

    return C, mean_length(probs,C)


def balanced_division(src):
    A = []
    B = list(src)
    diff = -sum(map(lambda x:x[1],src)) # diff = sum(A)-sum(B)
    while abs(diff+2*B[0][1]) < abs(diff):
        x = B.pop(0)
        A.append(x)
        diff += 2*x[1] # diff = (sum(A)+x)-(sum(B)-x) = diff + 2*x

    return A,B

def shannon_fano_code1(src,x):
    if len(src)==1:
        return [(src[0][0],x)]
    else:
        A,B = balanced_division(src)

        CA = shannon_fano_code1(A,x+'0')
        CB = shannon_fano_code1(B,x+'1')

        return CA + CB

def shannon_fano_code(src):
    src = to_probabilities(src)
    src = sorted(src, key=lambda x: x[1], reverse=True)

    probs = map(lambda x:x[1],src)
    C = shannon_fano_code1(src,'')

    return C, mean_length(probs,C)


'''
with open('../data/moby_dick.txt') as f:
    txt = f.read()
    txt = filter(lambda c: c in ascii_lowercase+' ',txt.lower())
    src = source(txt)
    #pprint(sorted(src,key=lambda x:x[1],reverse=True))
    #pprint(sorted(source_extension(src, 2),key=lambda x:x[1],reverse=True))
    print('H = ' + str(entropy_source(src)))
    #print('C = ' + pformat(shannon_code(src)))
    #pprint(shannon_fano_code(src))
    pprint(shannon_fano_code([('a1',0.36),('a2',0.18),('a3',0.18),('a4',0.12),('a5',0.09),('a6',0.07)]))
'''

src = [('0',0.9),('1',0.1)]
src_ext = source_extension(src,2)
pprint(shannon_code(src_ext))
pprint(shannon_fano_code(src_ext))
