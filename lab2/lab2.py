#!/usr/bin/python3.6
from collections import defaultdict
from itertools import product
from functools import reduce
from math import log, ceil
from string import ascii_lowercase
from pprint import pprint, pformat
import heapq


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


def mean_length(C,probs):
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

    return C, mean_length(C,probs)


def balanced_division(src):
    A = []
    B = list(src)
    diff = -reduce(lambda x,y: x+y[1], src, 0) # diff = sum(A)-sum(B)
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

    C = shannon_fano_code1(src,'')
    probs = map(lambda x:x[1],src)

    return C, mean_length(C,probs)


def build_code(tree,x):
    if len(tree)==1:
        return [(tree[0],x)]
    else:
        CA = build_code(tree[0],x+'0')
        CB = build_code(tree[1],x+'1')
        return CA+CB


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __lt__(self, other):
        if self.key == other.key:
            return True
        else:
            return self.key < other.key

def huffman_code(src):
    src = to_probabilities(src)
    src = sorted(src, key=lambda x: x[1])

    q = list(map(lambda x: Node(x[1],[x[0]]), src))
    heapq.heapify(q)

    while len(q) > 1:
        x = heapq.heappop(q)
        y = heapq.heappop(q)
        heapq.heappush(q, Node(x.key+y.key,[x.value,y.value]))
    tree = heapq.heappop(q).value

    C = build_code(tree,'')

    probs = []
    src = dict(src)
    for x in map(lambda x: x[0], C):
        probs.append(src[x])

    return C, mean_length(C,probs)


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
    #pprint(shannon_fano_code([('a1',0.36),('a2',0.18),('a3',0.18),('a4',0.12),('a5',0.09),('a6',0.07)]))
    pprint(huffman_code(src))
'''

#src = [('0',0.9),('1',0.1)]
#src = source_extension(src,2)
src = source('setzejutgesdunjutjatmengenfetgedunpenjat')
pprint(shannon_code(src))
pprint(shannon_fano_code(src))
pprint(huffman_code(src))
