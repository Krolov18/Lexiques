# coding: utf-8

from itertools import combinations
from multiprocessing import Pool, Process
import functools


def ngrams(seq, n, pads=False):
    if not n:
        return list()
    start = list()
    if pads:
        start += [None]*(n-1)
    seq = start + list(seq) + start
    while len(seq) >= n:
        yield tuple(seq[:n])
        seq = seq[1:]


def everygrams(seq, pads=False):
    for i in range(len(seq)+1):
        for x in ngrams(seq, i, pads):
            yield ''.join(x)


def everycombinations(x):
    for i in range(1, len(x)+1):
        for y in combinations(x, i):
            yield "".join(y)


def decompose(x, y):
    h = dict()
    comb_x = everygrams(x)
    comb_y = list(everygrams(y))
    for comb1 in comb_x:
        h[comb1] = set(comb_y)
    return h


def intersecte(x, y):
    for cle, val in y.items():
        if x.get(cle):
            x[cle] &= val
        else:
            x[cle] = val
    return x


def main():
    seq = "ban"
    print(list(everycombinations(seq)))

if __name__ == '__main__':
    main()
