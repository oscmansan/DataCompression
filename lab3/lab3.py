#!/usr/bin/python3.6
from collections import defaultdict


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
    l = sum(map(lambda x: x[1], src))
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
        _a = a + d * cumcount[i] // l
        _b = a + d * cumcount[i + 1] // l - 1

        _a = binary(_a, k)
        _b = binary(_b, k)
        print(x, _a, _b)

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


def arithmetic_decode(c,src,k,L):
    n = len(src)
    count = list(map(lambda x: x[1], src))
    cumcount = cumsum(count)
    l = sum(count)
    letters = list(map(lambda x: x[0], src))

    a = 0
    b = 2 ** k - 1
    d = b - a + 1

    g = c[:k]
    c = c[k:]

    str = ''
    for _ in range(L):
        _g = int(g, 2)

        # find next letter
        for i in range(n):
            _a = a + d * cumcount[i] // l
            _b = a + d * cumcount[i + 1] // l - 1
            if _a <= _g <= _b:
                str += letters[i]
                break

        _a = binary(_a, k)
        _b = binary(_b, k)
        print(_a, _b, g, str)

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

    return str


txt = '1010000000'
src = [('0', 9), ('1', 1)]
k = 6
c = arithmetic_encode(txt, src, k)
print(c)
txt = arithmetic_decode(c,src,k,len(txt))
print(txt)
