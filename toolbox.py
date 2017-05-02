# coding: utf-8

import collections
import itertools
import difflib
import heapq
import pickle

def trier_levenshtein(X):
    F = collections.deque()
    j = 0
    for ((i, x),(j, y)) in itertools.combinations(X, 2):
        if not (j % 100):
            print(j, len(X), file=stderr)
        tmp = difflib.SequenceMatcher(None, x, y)
        F.append((tmp.ratio, i, j))
        j += 1
    return heapq.heapify(F)


def main():
    tmp = list(filter(lambda x: x, map(lambda x: x.strip().split('\t')[::2], open('francais_col123.txt', 'r'))))
    print(trier_levenshtein(tmp[:len(tmp)//100]), file=pickle.load(open('distances.pickle','r')))


if __name__ == "__main__":
    main()

