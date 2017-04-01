#!/usr/bin/python3.6
from collections import defaultdict
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
    y = bin(x)[2:]
    return '0' * (k - len(y)) + y


def arithmetic_encode(str, src, k):
    letters = dict([(x[0], i) for i, x in enumerate(src)])
    count = [x[1] for x in src]
    w = sum(count)
    cumcount = cumsum(count)

    a = 0
    b = 2 ** k - 1
    d = b - a + 1

    c = ''
    u = 0
    for x in str:
        # update to the next subinterval
        i = letters[x]
        _a = a + d * cumcount[i] // w
        _b = a + d * cumcount[i + 1] // w - 1

        _a = binary(_a, k)
        _b = binary(_b, k)
        print(x, _a, _b, c)

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


def arithmetic_decode(c, src, k, l):
    n = len(src)
    letters, count = map(list, zip(*src))
    w = sum(count)
    cumcount = cumsum(count)

    a = 0
    b = 2 ** k - 1
    d = b - a + 1

    g = c[:k]
    c = c[k:]

    x = ''
    for _ in range(l):
        # find next letter
        _a = a
        _b = b
        for i in range(n):
            _a = a + d * cumcount[i] // w
            _b = a + d * cumcount[i + 1] // w - 1
            if _a <= int(g, 2) <= _b:
                x += letters[i]
                break

        _a = binary(_a, k)
        _b = binary(_b, k)
        print(_a, _b, g, x)

        # rescaling
        while _a[0] == _b[0]:
            _a = _a[1:] + '0'
            _b = _b[1:] + '1'
            g = g[1:] + c[0]
            c = c[1:] + '0'

        # underflow prevent
        while _a[1] == '1' and _b[1] == '0':
            _a = '0' + _a[2:] + '0'
            _b = '1' + _b[2:] + '1'
            g = g[0] + g[2:] + c[0]
            c = c[1:] + '0'

        a = int(_a, 2)
        b = int(_b, 2)
        d = b - a + 1

    return x


'''
txt = '1010000000'
src = [('0', 9), ('1', 1)]
k = 6
'''

txt = 'setzejutgesdunjutjatmengenfetgedunpenjat'
src = source(txt)
counts = [x[1] for x in src]
probs = [x / sum(counts) for x in counts]
p = min(probs)
k = ceil(-log(p, 2) + 2)

c = arithmetic_encode(txt, src, k)
print(c)
txt = arithmetic_decode(c, src, k, len(txt))
print(txt)
