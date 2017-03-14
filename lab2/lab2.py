#!/usr/bin/python3.6
from collections import defaultdict
from itertools import product
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

    return C


with open('../data/moby_dick.txt') as f:
    txt = f.read()
    txt = filter(lambda c: c in ascii_lowercase+' ',txt.lower())
    src = source(txt)
    #pprint(sorted(src,key=lambda x:x[1],reverse=True))
    #pprint(sorted(source_extension(src, 2),key=lambda x:x[1],reverse=True))
    print('H = ' + str(entropy_source(src)))
    print('C = ' + pformat(shannon_code(src)))
