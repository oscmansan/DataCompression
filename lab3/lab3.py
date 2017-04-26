#!/usr/bin/python3.6
from collections import OrderedDict
from decimal import Decimal, Context
from functools import reduce
from math import log, ceil
from random import randrange


def source(str):
    d = OrderedDict()
    for c in str:
        if c not in d:
            d[c] = 0
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
        b = a + d * cumcount[i + 1] // w - 1
        a = a + d * cumcount[i] // w

        _a = binary(a, k)
        _b = binary(b, k)
        # print(x, _a, _b, c)

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
        # print(_a, _b, g, x)

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


txt = open('../data/don_quixote.txt', 'r').read()
src = source(txt)
letters, count = map(list, zip(*src))
probs = [x / sum(count) for x in count]
p = min(probs)
k = ceil(-log(p, 2) + 2)

l = 1000
for _ in range(1000):
    i = min(randrange(len(txt)), len(txt)-l)
    str = txt[i:i+l]

    c = arithmetic_encode(str, src, k)
    print(c)

    ctx = Context()
    d = dict(zip(letters, probs))
    pr = reduce(lambda x, y: ctx.multiply(x, Decimal(d[y])), str, Decimal(1))
    expected_length = ceil(-ctx.divide(pr.ln(ctx), Decimal(2).ln(ctx))) + 1
    actual_length = len(c)
    assert (actual_length <= expected_length)

    dec = arithmetic_decode(c, src, k, len(str))
    print(dec)

    assert (dec == str)
