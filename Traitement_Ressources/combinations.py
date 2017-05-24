# coding: utf-8

from itertools import combinations, chain
from argparse import ArgumentParser
from chest import Chest
from regex import search, match, findall
from math import log, log10
from sys import stdout, stderr
from multiprocessing import Pool


def freq_binaire(t: str, d: str):
    return 1 if search(t, d) else 0


def frequence_brute(t: str, d: str, overlapped=True, len_d=False) -> float:
    return len(findall(t, d, overlapped=overlapped))/pow(2, len(d))


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


def tf_idf(t, d, ds, tf_p: str, overlapped=True):
    """
        Calcul du tf-idf d'un terme pour un document
    :param t: terme appartenant ou pas à d
    :param d: document d appartient à ds
    :param ts: ensembles des termes du document d
    :param ds: corpus de documents
    :param tf_p: flag peremttant de savoir quel type de tf on veut faire
    :param overlapped: booléen indiquant si l'on veut faire de la recherche en overlapping
    :return: retourne le tf-idf d'un terme
    """
    if d not in ds:
        return 0.
    else:
        tf = float()
        idf_ = idf(t, ds)
        print(idf_)
        if tf_p in ('bin', 'freq_brut', 'log_norm', 'norm_0.5'):
            if tf_p == 'bin':
                tf = freq_binaire(t=t, d=d)
            elif tf_p == "freq_brut":
                tf = frequence_brute(t=t, d=d, overlapped=False)
            elif tf_p == "log_norm":
                tf = log_norm(t=t, d=d)
        else:
            raise TypeError("la valeur de tf doit être dans ce tuple: ('bin', 'freq_brut', 'log_norm', 'norm_0.5')")
    return tf * idf_


def replace(seq, points, new):
    seq = list(seq)
    i = 0
    while i < len(points):
        seq[points[i]] = new
        i += 1
    return "".join(seq)


def estime(ba, memoire: Chest):
    """
        L'estimation maximale des paramètre se fait par le calcul du powerset sur un ensemble BA (Base d'Apprentissage).
        On fait donc un tf-idf mais en ayant en vocabulaire les composantes du powerset
    :param BA:
    :return:
    """
    len_ba = sum(pow(2, len(x)) for x in ba)
    with Pool(processes=5) as p:
        for element in ba:
            for x in p.map(lambda i: powerset(element, i), range(len(element))):
                for y in x:
                    if not memoire.get(x):
                        memoire[x] = frequence_brute(y, element, True)
    for x in memoire:
        memoire[x] /= len(memoire)


def powerset(sequence, i, var='.'):
    for x in map(lambda seq: replace(sequence, seq, var), combinations(range(len(sequence)), i)):
        yield x


def main():
    parser = ArgumentParser(
        prog="combinations"
    )

    parser.add_argument(
        "sequence"
    )

    parser.add_argument(
        "-i",
        "--int",
        type=int
    )

    args = parser.parse_args()

    for x in map(lambda seq: replace(args.sequence, seq, "."), combinations(range(len(args.sequence)), args.int)):
        print(x, file=stdout)


def main2():
    seq = "a"*10
    print(len(list(chain(*[x for x in map(lambda i: powerset(seq, i), range(1, len(seq)+1))]))))


if __name__ == '__main__':
    main2()
