# coding: utf-8
#from nltk.util import ngrams, skipgrams
# from nltk.data import find
import typing
from collections import defaultdict, deque
from copy import deepcopy
from string import punctuation
from re import search, findall
import heapdict
import regex
from chest import Chest
import subprocess
#import chest
#from numpy import *
from math import log10, log
#from _pickle import load, dump
#from functools import reduce
from itertools import groupby

# import functools

# true = "∆x.∆y.x"
# false = "∆x.∆y.y"
# et = "∆p.∆q.((p)q){false}".format(false=false)
# ou = "∆p.∆q.((p){true})q".format(true=true)
# negation = "(∆x.x)(false)true"
# ifthenelse = "∆p.∆a.∆b.((p)a)b"
# jeanmangeunepomme = "€x((P)x & (M)(x)j)"
# jean = "∆P.(P)j"
# mange = "∆x.∆y.(M)(y)x"
# une = "∆P.∆Q.€x(P)Q"
# unepomme = "∆Q.€x.(∆x.(P)x)Q"
# pomme = "∆x.(P)x"
# iszero = "∆n.((n)∆x.{false}){true}".format(true=true, false=false)
# iszero2 = "∆x.x"
# app_func = "({}){}"
# nsegation = "(∆x.x)({false}){true}".format(true=true, false=false)


class Point(object):
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return self.string

    def __str__(self):
        return repr(self)

    def __hash__(self):
        return 1

    def __eq__(self, other):
        return str(self) == str(other)


class OptimString:
    def __init__(self, point: Point, seq: typing.Sequence, pointee=None, control=None):
        self.__point = point
        self.__data = seq
        self.__data_pointe = list(seq) if not pointee else pointee
        self.__control = defaultdict(deque) if not control else control
        if not self.__control:
            self.__remplir_control(seq)
        tmp = list(filter(lambda x: isinstance(x, str), self.__data_pointe))
        self.__first = tmp[0] if tmp else ''

    @property
    def first(self):
        return self.__first

    @property
    def get_point(self):
        return self.__point

    @property
    def data_pointe(self):
        return self.__data_pointe

    @data_pointe.setter
    def data_pointe(self, value):
        pass

    @property
    def data(self):
        return self.__data

    @property
    def control(self):
        return self.__control

    def etendre(self):
        l = list()
        n_p = None
        for x in self.data_pointe:
            if not isinstance(x, Point):
                if n_p is not None:
                    l.append(n_p)
                    n_p = None
                l.append(x)
            else:
                if n_p is None:
                    n_p = x
                else:
                    n_p = Point('.*')
        if n_p is not None:
            l.append(n_p)
        return OptimString(point=Point('.*'), seq=l)

    def __remplir_control(self, seq): list(
        map(lambda x: self.control[x[0]].append(x[1]), self.__inverse_enumerate(seq=seq))
    )

    def trier_control(self): return heapdict.heapdict(self.control)

    @staticmethod
    def __inverse_enumerate(seq):
        """
            On inverse clé,valeur de enumerate(sequence).
        :return:
        """
        return ((t, y) for y, t in enumerate(seq))

    def add_point(self):
        data_pointe = deepcopy(self.data_pointe)
        control = deepcopy(self.control)

        if self.get_point not in control:
            data_pointe[0] = self.get_point
            control[self.get_point].append(0)
        else:
            if isinstance(data_pointe[-1], Point):
                return OptimString(point=self.__point, seq=self.data, pointee=data_pointe, control=control)

            pt = control.get(self.get_point)[-1]
            data_pointe[pt+1] = self.get_point
            control.get(self.get_point).append(pt+1)

        return OptimString(point=self.__point, seq=self.data, pointee=data_pointe, control=control)

    def deplace_point(self):
        data_pointe = deepcopy(self.data_pointe)
        control = deepcopy(self.control)

        if self.get_point not in control:
            return self

        pt = control.get(self.get_point)[-1]
        if pt == len(self.__data)-1:
            return OptimString(point=self.__point, seq=self.data, pointee=data_pointe, control=control)
        else:
            control[self.get_point][-1] += 1
            data_pointe[pt] = self.__data[pt]
            data_pointe[pt+1] = self.get_point
        return OptimString(point=self.__point, seq=self.data, pointee=data_pointe, control=control)

    def __repr__(self):
        return "".join(map(lambda x: escape_char(x), self.data_pointe))

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return self.data_pointe == other.data_pointe

    def __hash__(self):
        return 1


def escape_char(x):
    return "\\"+x if ((str(x) in punctuation) and isinstance(x, str)) else str(x)


def generate_regex(seq: OptimString, memo: Chest=None):
    file = deque()
    sortie = deque()

    file.appendleft(seq)

    while file:
        current = file.pop()
        if not all(x == '.' for x in str(current)):
            if not memo.get(current):
                yield current
        if not isinstance(current.data_pointe[-1], Point):
            current = current.add_point()
            file.appendleft(current)
            for _ in range(current.control.get(current.get_point)[-1]+1, len(current.data)):
                current = current.deplace_point()
                file.appendleft(current)


def count(regex: OptimString, chaine: str, nb=False):
    if nb:
        return 1 if search(str(regex), chaine) else 0
    i = 0
    rec = search(str(regex), chaine)
    while rec:
        i += 1
        if not regex.first:
            break
        chaine = chaine.replace(regex.first, '', 1)
        rec = search(str(regex), chaine)
    return i


def construire(phrases):
    classes = Chest(path="classes", dump=dump, load=load)
    features = Chest(path="features", dump=dump, load=load)

    for p in phrases:
        vecteur = Chest(path=p, dump=dump, load=load)
        vecteur_log = Chest(path=p, dump=dump, load=load)

        # for skip in generate_regex()


def replace(x, y, z):
    for s in y:
        x = x.replace(x[s], z, 1)
    return x


def g(mot):
    # from re import sub
    from nltk.util import skipgrams
    tmp = [x for x, y in enumerate(mot)]
    for i in range(2, len(mot)+1):
        for skip in skipgrams(tmp, i, len(mot)):
            # yield sub("\.\.+", ".+", replace(mot, skip, '.'))
            yield skip


def dot(wi, x):
    from functools import reduce
    from operator import mul, add
    return reduce(add, map(lambda i: mul(wi[i], x[i]), x))


def argmax(w, x):
    a = str()
    b = float()

    for z, u in w.items():
        calcul = dot(z, x)
        if calcul > b:
            a = u
            b = calcul
    return a, b


def estime(ba):
    classes = chest.Chest(path="classes", dump=dump, load=load)
    features = chest.Chest(path='features', dump=dump, load=load)
    ba_repr = chest.Chest(path='base-d-apprentissage', dump=dump, load=load)
    for p in ba:
        classes[p] = True
        features[p] = True
        for y in generate_regex(OptimString(point=Point('.'), seq=p)):
            features[y] = True
            ba_repr[p][y] = (1+log10(count(y, p)/pow(2, len(p))))/log10(len(ba)/sum(count(y, z, True) for z in ba))
        features.flush()
    classes.flush()
    ba_repr.flush()


def perceptron(classes, features, ba, n):
    w = random.rand(len(classes), len(features))
    for i in range(n):
        for (x, y) in ba:
            y_pred = argmax(w, x)
            if y != y_pred:
                for t, i in x.items():
                    w[y][t] += i
                    w[y_pred][t] += i


def freq_binaire(t: str, d: str):
    return 1 if regex.search(t, d) else 0


def frequence_brute(t: str, d: str, overlapped=True, len_d=False) -> float:
    return len(regex.findall(t, d, overlapped=overlapped))/len(d) if not len_d else pow(2, len(d))


def log_norm(t: str, d: str) -> float:
    return 1 + log(frequence_brute(t, d))


def normal_05_max(t: str, d: str, ts, overlapped=False, len_d=False):
    max_fr_b = float()
    for q in ts:
        calcul = frequence_brute(q, d, overlapped=overlapped, len_d=len_d)
        if calcul > max_fr_b:
            max_fr_b = calcul
    return 0.5 + 0.5 * (frequence_brute(t, d) / max(frequence_brute(q, d) for q in ts))


def idf(t, ds):
    i = 0
    for d in ds:
        i += freq_binaire(t, d)
    return len(ds) / i


def tf_idf(t, d, ts, ds, tf_p: str, overlapped=True):
    """
        Calcul du tf-idf d'un terme pour un document
    :param t: terme appartenant ou pas à d
    :param d: document d appartient à ds
    :param ts: ensembles des termes du document d
    :param ds: corpus de documents
    :param tf: flag peremttant de savoir quel type de tf on veut faire
    :return: retourne le tf-idf d'un terme
    """
    if d not in ds:
        return 0
    else:
        tf = float()
        idf_ = idf(t, ds)
        if tf_p in ('bin', 'freq_brut', 'log_norm', 'norm_0.5'):
            if tf_p == 'bin':
                tf = freq_binaire(t=t, d=d)
            elif tf_p == "freq_brut":
                tf = frequence_brute(t=t, d=d, overlapped=False)
            elif tf_p == "log_norm":
                tf = log_norm(t=t, d=d)
            elif tf_p == "norm_0.5":
                tf = normal_05_max(t=t, d=d, ts=ts)
        else:
            raise TypeError("la valeur de tf doit être dans ce tuple: ('bin', 'freq_brut', 'log_norm', 'norm_0.5')")
    return tf * idf_


def main():
    import argparse
    import sys
    import re

    parseur = argparse.ArgumentParser()
    parseur.add_argument("texte", type=argparse.FileType(mode='r', encoding='latin-1'))
    args = parseur.parse_args()
    tmp = OptimString(point=Point('.'))

    first = next(args.texte, None)

    tmp.initialise('les')
    print(list(generate_regex(tmp)))

    #while first is not None:
    #    print(first.strip())
    #    for mot in re.split(pattern="\W+", string=first.strip()):
    #        tmp.initialise(mot)
    #        strings = generate_regex(tmp)
    #        print(list(strings))
#   #         for f in strings:
#   #             print(f)
    #        tmp.clear()
    #    first = next(args.texte, None)


    # t = next(strings, None)
    # i = 0
    # while t is not None:
    #     print(t, file=sys.stdout)
    #     i += 1
    #     t = next(strings, None)

def main2():
    from nltk.corpus import gutenberg
    from chest import Chest
    from heapdict import heapdict
    struc = Chest()
    texte = gutenberg.raw('carroll-alice.txt')
    phrases = iter(texte.split('\n'))
    # print(list(map(lambda x: list(generate_regex(OptimString(point=Point('.'), seq="".join(x)))), everygrams(next(phrases)))))

    for element in ngrams(next(phrases), 10):
        chaine = OptimString(point=Point('.'), seq="".join(element))
        for x in generate_regex(chaine):
            # print(str(x))
            struc[x] = True
    print(len(list(struc.keys())))

    # for phrase in phrases:
        # x = OptimString(point=Point('.'), seq=phrase)
        # ttt = heapdict(x.control)
        # regexes = generate_regex(x)
        # first = next(regexes, False)
        # while regexes:
        #     i = count(first, texte)
        #     struc[first] = i
        #     first = next(regexes, False)
        # print(len(struc))


def main3():
    chaine = "le chat dort"
    tmp = OptimString(Point('.'), chaine)
    tmp1 = generate_regex(tmp)

    for t in tmp1:
        print(t.etendre())


if __name__ == '__main__':
    main3()
