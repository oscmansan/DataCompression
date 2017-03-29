#!/usr/bin/python3.6
from collections import defaultdict
from string import ascii_lowercase
from math import log, ceil, floor


def source(str):
    d = defaultdict(lambda: 0)
    for c in str:
        d[c] += 1
    return list(d.items())


def cumsum(L):
    r = [0]
    for x in L:
        r.append(r[-1] + x)
    return r


def arithmetic_encode(str, src, k):
    n = sum(map(lambda x: x[1], src))
    letters = {}
    for i, a in enumerate(map(lambda x: x[0], src)):
        letters[a] = i
    count = list(map(lambda x: x[1], src))
    cumcount = cumsum(count)

    a = 0
    b = 2 ** k - 1
    d = b - a + 1

    for i in range(len(src)):
        _a = a + floor(d * cumcount[i] / n)
        _b = a + floor(d * cumcount[i + 1] / n) - 1
        print(_a, _b)


with open('../data/don_quixote.txt', 'r') as f:
    txt = f.read()
    txt = list(filter(lambda c: c in ascii_lowercase + ' ', txt.lower()))
    src = source(txt)
    count = list(map(lambda x: x[1], src))
    probs = list(map(lambda x: float(x) / sum(count), count))
    p = min(probs)
    k = ceil(-log(p, 2) + 2)
    arithmetic_encode(txt, src, k)
