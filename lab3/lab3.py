#!/usr/bin/python3.6
from collections import defaultdict
from string import ascii_lowercase
from math import log, ceil


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


def binary(x, k):
    if x == 0:
        return '0' * k
    else:
        y = bin(x)[2:]
        return '0' * (k - len(y)) + y


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

    c = ''
    u = 0
    for x in str:
        # update to the next subinterval
        i = letters[x]
        _a = a + d * cumcount[i] // n
        _b = a + d * cumcount[i + 1] // n - 1

        _a = binary(_a, k)
        _b = binary(_b, k)

        # rescaling
        while _a[0] == _b[0]:
            z = _a[0]
            _a = _a[1:] + '0'
            _b = _b[1:] + '1'

            c += z
            c += '1' * u if z == '0' else '0' * u
            u = 0

        # underflow prevent
        while _a[1] == '1' and _b[1] == '0':
            _a = '0' + _a[2:] + '0'
            _b = '1' + _b[2:] + '1'
            u += 1

        a = int(_a, 2)
        b = int(_b, 2)
        d = b - a + 1

    return c + '1'


txt = '1010000000'
src = [('0', 9), ('1', 1)]
c = arithmetic_encode(txt, src, 6)
print(c)
