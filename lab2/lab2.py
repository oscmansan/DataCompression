#!/usr/bin/python3.6
from collections import defaultdict
from itertools import product
from math import log


def to_probabilities(src):
    letters, count = zip(*src)
    probs = list(map(lambda x: float(x) / sum(count), count))
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


with open('../data/don_quijote.txt') as f:
    txt = f.read()
    src = source(txt)
    print(src)
    print(source_extension(src, 2))
    print(entropy_source(src))
