# coding: utf-8
from string import punctuation
from heapdict import heapdict
from copy import deepcopy
from typing import Sequence
from collections import defaultdict, deque
from chest import Chest
from combinations import tf_idf, frequence_brute, freq_binaire, idf, powerset
from itertools import chain, product
import sqlite3


def skip_duplicates(iterable, key=lambda x: x):
    """
        http://sametmax.com/saffranchir-des-doublons-dun-iterable-en-python/
    :param iterable:
    :param key:
    :return:
    """
    # on va mettre l’empreinte unique de chaque élément dans ce set
    fingerprints = set()

    for x in iterable:
        # chaque élement voit son emprunte calculée. Par défaut l’empreinte
        # est l'élément lui même, ce qui fait qu'il n'y a pas besoin de
        # spécifier 'key' pour des primitives comme les ints ou les strings.
        fingerprint = key(x)

        # On vérifie que l'empreinte est dans la liste des empreintes  des
        # éléments précédents. Si ce n'est pas le cas, on yield l'élément, et on
        # rajoute sont empreinte ans la liste de ceux trouvés, donc il ne sera
        # pas yieldé si on ne le yieldera pas une seconde fois si on le
        # rencontre à nouveau
        if fingerprint not in fingerprints:
            yield x
            fingerprints.add(fingerprint)


def remove_duplicates(lst, equals=lambda x, y: x == y):
    """
        http://sametmax.com/saffranchir-des-doublons-dun-iterable-en-python/
    :param lst:
    :param equals:
    :return:
    """
    if not isinstance(lst, list):
        raise TypeError('This function works only with lists.')
    i1 = 0
    l = (len(lst) - 1)
    while i1 < l:
        elem = lst[i1]
        i2 = i1 + 1
        while i2 <= l:
            if equals(elem, lst[i2]):
                del lst[i2]
                l -= 1
            i2 += 1
        i1 += 1
    return lst


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
    def __init__(self, seq: Sequence, point: Point, pointee=None, control=None):
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
                    n_p = Point('.+')
        if n_p is not None:
            l.append(n_p)
        return OptimString(point=Point('.+'), seq=l)

    def __remplir_control(self, seq): list(
        map(lambda x: self.control[x[0]].append(x[1]), self.__inverse_enumerate(seq=seq))
    )

    def trier_control(self): return heapdict(self.control)

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


def generate_regex(seq: OptimString, classes, cursor: sqlite3.Cursor):
    doublon = None

    add_value_cmd = """INSERT INTO Examples(corpus_id,class_id,feature_id,value)
    SELECT Corpus.id,Classes.id, Features.id
    FROM Corpus,Classes,Features
    WHERE Corpus.sequence=?
    AND Classes.classe=?
    AND Features.feature=?;
    """
    add_classes_cmd = "INSERT OR IGNORE INTO Classes(classe) VALUES (?);"
    add_features_cmd = "INSERT OR IGNORE INTO Features(feature) VALUES (?);"
    add_sequence_cmd = "INSERT OR IGNORE INTO Corpus(sequence) VALUES (?);"
    add_genealogie_cmd = "INSERT OR IGNORE INTO Genealogie(pere_id, descendant_id) VALUES (?,?)"
    select_feature = "select id from features where feature=?"

    seq_id = cursor.execute(select_feature, (str(seq),)).fetchone()

    file = deque()

    file.appendleft(seq)

    while file:
        current = file.pop()
        # vérification de la présence de current dans la database
        cursor.execute("select descendant_id from genealogie where pere_id=(select id from features where id=?)")
        descendants = cursor.fetchall()
        if descendants:
            cursor.executemany(add_value_cmd, product((seq,), classes, descendants))
        else:
            if str(seq) != str(current):
                tmp = (seq, current if not all(x == '.' for x in str(current)) else 'NULL')
                if tmp != doublon:
                    if tmp[1] == "NULL":
                        # mettre à jour les exemples
                        cursor.executemany(add_value_cmd, map(lambda x: (seq, x, current), classes))
                        # mettre à jour généalogie
                        cursor.execute(add_genealogie_cmd,
                                       cursor.execute(select_feature, (str(current),)).fetchone() + ('NULL',))
                    # mettre à jour features
                    cursor.execute(add_features_cmd, (str(current),))
                    # mettre à jour les exemples
                    cursor.executemany(add_value_cmd, map(lambda x: (seq, x, current), classes))
                    # mettre à jour généalogie
                    cursor.execute(add_genealogie_cmd,
                                   seq_id + cursor.execute(select_feature,(str(current),)).fetchone()
                                   )

                    doublon = tmp
                if isinstance(current.data_pointe[-1], Point):
                    yield current, 'NULL'
                    # mettre à jour les exemples
                    cursor.executemany(add_value_cmd, map(lambda x: (seq, x, current), classes))
                    # mettre à jour généalogie
                    cursor.execute(add_genealogie_cmd,
                                   cursor.execute(select_feature, (str(current),)).fetchone()+('NULL',)
                                   )
            if not isinstance(current.data_pointe[-1], Point):
                old = current
                current = current.add_point()
                tmp = (old, current if not all(x == '.' for x in str(current)) else 'NULL')
                if tmp != doublon:
                    yield tmp
                    # mettre à jour features
                    cursor.execute(add_features_cmd, (str(current),))
                    # mettre à jour les exemples
                    cursor.executemany(add_value_cmd, map(lambda x: (seq, x, current), classes))
                    # mettre à jour généalogie
                    cursor.execute(add_genealogie_cmd,
                                   seq_id + cursor.execute(select_feature, (str(current),)).fetchone()
                                   )
                    doublon = tmp
                if not all(x == '.' for x in str(current)):
                    file.appendleft(current)
                for _ in range(current.control.get(current.get_point)[-1]+1, len(current.data)):
                    current = current.deplace_point()
                    file.appendleft(current)


def estime(sequence, ba, memoire=None, d=None):
    for x in generate_regex(seq=OptimString(sequence, Point('.')), memo=memoire):
        tmp = str(x.etendre())
        memoire[tmp] = frequence_brute(tmp, sequence)
        d[tmp].add(sequence)


def estimate(sequence, ba, memoire=None, d=None):
    for x in chain(*[x for x in map(lambda i: powerset(sequence, i), range(1, len(sequence)+1))]):
        if not memoire.get(x):
            memoire[x] = frequence_brute(x, sequence) * idf(x, ba)
        d[x].add(sequence)


def etendre(seq):
    l = str()
    n_p = str()
    for i, x in enumerate(seq):
        if (x != '.') or (seq[i-1] == '\\'):
            if n_p:
                l += n_p
                n_p = str()
            l += x
        else:
            if not n_p:
                n_p = x
            else:
                n_p = '.+'
    if n_p is not None:
        l += n_p
    return l


def main():
    dico = Chest(path='francais_tatoeba_5bis-char-max')
    dico2 = defaultdict(set)
    i = 0
    with open("/Users/korantin/Documents/Projects/Lexiques/francais_col123.txt", 'r') as ba:
        tmp = ba.read().splitlines()
        for phrase in tmp:
            (ind, ln, phrase) = phrase.strip().split('\t')
            if len(phrase) <= 10:
                print(phrase)
                print(i, len(tmp))
                estime(phrase, tmp, memoire=dico, d=dico2)
            i += 1
        for x, y in dico2.items():
            dico[x] *= (len(tmp)/len(y))
        dico.flush()
    print(dico.items(), sep='\n')


def main2():
    x = 'bons'
    tmp = OptimString(seq=x, point=Point('.'), pointee=None, control=None)
    for x in enumerate(skip_duplicates(generate_regex(tmp))):
        print(*x)
    print()
    for x in enumerate(generate_regex(tmp)):
        print(*x)


if __name__ == '__main__':
    main2()
