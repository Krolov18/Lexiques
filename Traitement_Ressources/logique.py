# coding: utf-8
from nltk.util import ngrams, skipgrams
# from nltk.data import find
from collections import defaultdict, deque
from copy import deepcopy
from string import punctuation
from re import search
import heapdict
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
    def __init__(self, point: Point, seq: str, pointee=None, control=None):
        self.__point = point
        self.__data = seq
        self.__data_pointe = list(seq) if not pointee else pointee
        self.__control = defaultdict(deque) if not control else control
        if not self.__control:
            self.__remplir_control(seq)
        self.__buffer = heapdict.heapdict(self.__control)

    @property
    def buffer(self):
        return self.__buffer

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
                    n_p = Point('.+')
        if n_p is not None:
            l.append(n_p)
        return "".join(map(str, l))

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


def generate_regex(seq: OptimString):
    file = deque()
    sortie = deque()

    file.appendleft(seq)

    while file:
        current = file.pop()
        yield current
        if not isinstance(current.data_pointe[-1], Point):
            current = current.add_point()
            file.appendleft(current)
            for _ in range(current.control.get(current.get_point)[-1]+1, len(current.data)):
                current = current.deplace_point()
                file.appendleft(current)


def count(regex, chaine: str):
    i = 0
    rec = search(str(regex), chaine)
    x = regex.buffer.popitem()[0]
    while rec:
        i += 1
        chaine = chaine.replace(x, '', 1)
        rec = search(str(regex), chaine)
    return i


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


def replace(x, y, z):
    for s in y:
        x = x.replace(x[s], z, 1)
    return x


def g(mot):
    tmp = [x for x, y in enumerate(mot)]
    for i in range(2, len(mot)+1):
        for skip in skipgrams(tmp, i, len(mot)):
            #yield replace(mot, skip, '.')
            yield skip


def main3():
    tmp = OptimString(Point('.'), 'anticonstitution')
    tmp1 = generate_regex(tmp)
    # for t in g('anconstitution'):
        #print(t)
    for t in tmp1:
        print(str(t))


if __name__ == '__main__':
    main3()
