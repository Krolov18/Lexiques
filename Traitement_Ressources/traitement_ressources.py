# coding: utf-8
from codecs import open
from copy import deepcopy
from typing import Dict, Sequence
import re
import collections
from _pickle import dump, load

import yaml
import sys


def lefff_codex():
    """
        Structure des étiquettes morphosyntaxiques du Lefff.
    :return: dictionnaire avec en clé les étiquettes et en valeurs des dictionnaires de set
    """
    tmp = {
        "mode": set(),
        "tense": set(),
        "person": set(),
        "gender": set(),
        "number": set()
    }

    codex = {x: deepcopy(tmp) for x in "PFIJTYZSCKGW123spmf"}

    codex["P"]["mode"].add("indicative")
    codex["P"]["tense"].add("present")

    codex["F"]["mode"].add("indicative")
    codex["F"]["tense"].add("future")

    codex["I"]["mode"].add("indicative")
    codex["I"]["tense"].add("imperfect")

    codex["J"]["mode"].add("indicative")
    codex["J"]["tense"].add("past")

    codex["C"]["mode"].add("conditionnal")
    codex["C"]["tense"].add("present")

    codex["Y"]["mode"].add("imperative")
    codex["Y"]["tense"].add("present")

    codex["S"]["mode"].add("subjunctive")
    codex["S"]["tense"].add("present")

    codex["T"]["mode"].add("subjunctive")
    codex["T"]["tense"].add("imperfect")

    codex["K"]["mode"].add("participe")
    codex["K"]["tense"].add("past")

    codex["G"]["mode"].add("participle")
    codex["G"]["tense"].add("present")

    codex["W"]["mode"].add("infinitive")
    codex["W"]["tense"].add("present")

    codex["1"]["person"].add("1")

    codex["2"]["person"].add("2")

    codex["3"]["person"].add("3")

    codex["m"]["gender"].add("masculine")

    codex["f"]["gender"].add("feminine")

    codex["s"]["number"].add("singular")

    codex["p"]["number"].add("plural")

    return codex


def unify_dict(dico1: Dict, dico2: Dict) -> Dict:
    for (key, value) in dico2.items():
        if key in dico1:
            if isinstance(dico1.get(key), dict) and isinstance(value, dict):
                dico1[key] = unify_dict(dico1.get(key), value)
            elif deepcopy(dico1.get(key)) != value:
                raise LookupError(
                    "Erreur d'unification: pour une clé deux valeurs différentes sont attriuées. {0}, {1}".format(
                        value,
                        dico1.get(key)
                    )
                )
        else:
            dico1[key] = value
    return dico1


def unify_dict_add(dico1: Dict, dico2: Dict) -> Dict:
    # print(dico1, dico2)
    for (key, value) in dico2.items():
        if key in dico1:
            if isinstance(dico1.get(key), dict) and isinstance(value, dict):
                dico1[key] = unify_dict(dico1.get(key), value)
            elif isinstance(dico1.get(key), set) and isinstance(value, set):
                dico1[key].update(value)
        else:
            dico1[key] = value
    return dico1


def reduce_unification(list_dict: Sequence[Dict]) -> Dict:
    import functools
    # print(list_dict)
    return functools.reduce(lambda x, y: unify_dict_add(x, y), list_dict) if list_dict else list_dict


def traiter_bdlexique(filename, mode='r', encoding=None, errors='strict', buffering=1):
    with open(filename=filename, mode=mode, encoding=encoding, errors=errors, buffering=buffering) as inStream:
        pass


def traiter_lexique(filename, mode='r', encoding=None, errors='strict', buffering=1):
    formes = dict()
    categories = set()
    lemmes = set()

    with open(filename=filename, mode=mode, encoding=encoding, errors=errors, buffering=buffering) as inStream:
        for entree in inStream:
            if not entree.startswith('#'):
                (forme, number, categorie, features) = entree.strip().split('\t')
                if not any(x in features for x in ("(arg1)", "(arg2)")):
                    yield [forme, number, categorie, g(iter(features), table_lefff)]



def g(stream, table):
    """
        A partir d'un générteur et d'une table d'opérations sensibles
        aux structures définies ci-dessous, on va retourner une
        structure complexe représentant le contenu du générateur.
    :param stream: générateur
    :param table: dictionnaire de lambdas
    :return: un dictionnaire représentant le générateur
    """
    global morpho, rel, fac, f_cles, r_cles, obligatoire, facultatif, features, relations, buffer, lemme, number, morphologie
    current = next(stream, False)
    morpho = rel = fac = False
    f_cles, r_cles = (list(), list())
    obligatoire, facultatif, morphologie = (set(), set(), set())
    lemme, number = [str(), str()]
    features, relations = (dict(), dict())
    buffer = str()

    while current:
        table[current](current)
        # print(f_cles, buffer)
        # print(features or relations or obligatoire or facultatif or morphologie or lemme or number or morpho or rel or fac)
        current = next(stream, False)
    return features

def raise_error(buffer):
    raise BufferError('est-ce normal d\'avoir cela sur le buffer', buffer)

table_lefff = {
    "[": lambda x: None,

    "(": lambda x: globals().__setitem__('fac', True),
    ")": lambda x: [globals().__setitem__('fac', False),
                    facultatif.add(buffer),
                    relations.__setitem__(r_cles.pop(), {'facultatif': facultatif}),
                    globals().__setitem__('buffer', str())],
    "]": lambda x: [
        (morphologie.add(buffer.strip()) if morpho else features.__setitem__(f_cles.pop(), buffer.strip(' ')),
        features.__setitem__('morphologie', morphologie)) if (features or f_cles or relations or obligatoire or facultatif or morphologie or lemme or number or morpho or rel or fac) else 0
    ],
    "|": lambda x: [facultatif.add(buffer) if fac else obligatoire.add(buffer), globals().__setitem__('buffer', str())],
    "=": lambda x: [f_cles.append(buffer.strip(' ')), globals().__setitem__('buffer', str())],
    ":": lambda x: [r_cles.append(buffer), globals().__setitem__('buffer', str())],
    ",": lambda x: [((obligatoire.add(buffer) if rel else (morphologie.add(buffer) if morpho else features.__setitem__(f_cles.pop(), {'lemme': lemme, 'number': number if number else None, 'relations': relations}))) if buffer else 0), globals().__setitem__('buffer', str())],
    "<": lambda x: [[globals().__setitem__(x, y.lstrip("'")) for (x, y) in zip(('lemme', 'number'), re.split(r'__+', buffer))], globals().__setitem__('rel', True), globals().__setitem__('buffer', str())],
    ">": lambda x: [globals().__setitem__('rel', False), obligatoire.add(buffer) if buffer else 0, (relations.__setitem__(r_cles.pop(), {'obligatoire': obligatoire}) if r_cles else relations.__setitem__('obligatoire', obligatoire))],
    "@": lambda x: globals().__setitem__('morpho', True),

    '!': lambda x: globals().__setitem__("buffer", buffer+x),
    '"': lambda x: globals().__setitem__("buffer", buffer+x),
    '#': lambda x: globals().__setitem__("buffer", buffer+x),
    '$': lambda x: globals().__setitem__("buffer", buffer+x),
    '%': lambda x: globals().__setitem__("buffer", buffer+x),
    '&': lambda x: globals().__setitem__("buffer", buffer+x),
    "'": lambda x: globals().__setitem__("buffer", buffer+x),
    '*': lambda x: globals().__setitem__("buffer", buffer+x),
    "+": lambda x: globals().__setitem__("buffer", buffer+x),
    '-': lambda x: globals().__setitem__("buffer", buffer+x),
    ".": lambda x: globals().__setitem__("buffer", buffer+x),
    "/": lambda x: globals().__setitem__("buffer", buffer+x),
    '0': lambda x: globals().__setitem__("buffer", buffer+x),
    '1': lambda x: globals().__setitem__("buffer", buffer+x),
    '2': lambda x: globals().__setitem__("buffer", buffer+x),
    '3': lambda x: globals().__setitem__("buffer", buffer+x),
    '4': lambda x: globals().__setitem__("buffer", buffer+x),
    '5': lambda x: globals().__setitem__("buffer", buffer+x),
    '6': lambda x: globals().__setitem__("buffer", buffer+x),
    '7': lambda x: globals().__setitem__("buffer", buffer+x),
    '8': lambda x: globals().__setitem__("buffer", buffer+x),
    '9': lambda x: globals().__setitem__("buffer", buffer+x),
    ";": lambda x: globals().__setitem__("buffer", buffer+x),
    '?': lambda x: globals().__setitem__("buffer", buffer+x),
    "A": lambda x: globals().__setitem__("buffer", buffer+x),
    "B": lambda x: globals().__setitem__("buffer", buffer+x),
    "C": lambda x: globals().__setitem__("buffer", buffer+x),
    "D": lambda x: globals().__setitem__("buffer", buffer+x),
    "E": lambda x: globals().__setitem__("buffer", buffer+x),
    "F": lambda x: globals().__setitem__("buffer", buffer+x),
    "G": lambda x: globals().__setitem__("buffer", buffer+x),
    "H": lambda x: globals().__setitem__("buffer", buffer+x),
    "I": lambda x: globals().__setitem__("buffer", buffer+x),
    "J": lambda x: globals().__setitem__("buffer", buffer+x),
    "K": lambda x: globals().__setitem__("buffer", buffer+x),
    "L": lambda x: globals().__setitem__("buffer", buffer+x),
    "M": lambda x: globals().__setitem__("buffer", buffer+x),
    "N": lambda x: globals().__setitem__("buffer", buffer+x),
    "O": lambda x: globals().__setitem__("buffer", buffer+x),
    "P": lambda x: globals().__setitem__("buffer", buffer+x),
    "Q": lambda x: globals().__setitem__("buffer", buffer+x),
    "R": lambda x: globals().__setitem__("buffer", buffer+x),
    "S": lambda x: globals().__setitem__("buffer", buffer+x),
    "T": lambda x: globals().__setitem__("buffer", buffer+x),
    "U": lambda x: globals().__setitem__("buffer", buffer+x),
    "V": lambda x: globals().__setitem__("buffer", buffer+x),
    "W": lambda x: globals().__setitem__("buffer", buffer+x),
    "X": lambda x: globals().__setitem__("buffer", buffer+x),
    "Y": lambda x: globals().__setitem__("buffer", buffer+x),
    "Z": lambda x: globals().__setitem__("buffer", buffer+x),
    "_": lambda x: globals().__setitem__("buffer", buffer+x),
    "a": lambda x: globals().__setitem__("buffer", buffer+x),
    "b": lambda x: globals().__setitem__("buffer", buffer+x),
    "c": lambda x: globals().__setitem__("buffer", buffer+x),
    "d": lambda x: globals().__setitem__("buffer", buffer+x),
    "e": lambda x: globals().__setitem__("buffer", buffer+x),
    "f": lambda x: globals().__setitem__("buffer", buffer+x),
    "g": lambda x: globals().__setitem__("buffer", buffer+x),
    "h": lambda x: globals().__setitem__("buffer", buffer+x),
    "i": lambda x: globals().__setitem__("buffer", buffer+x),
    "j": lambda x: globals().__setitem__("buffer", buffer+x),
    "k": lambda x: globals().__setitem__("buffer", buffer+x),
    "l": lambda x: globals().__setitem__("buffer", buffer+x),
    "m": lambda x: globals().__setitem__("buffer", buffer+x),
    "n": lambda x: globals().__setitem__("buffer", buffer+x),
    "o": lambda x: globals().__setitem__("buffer", buffer+x),
    "p": lambda x: globals().__setitem__("buffer", buffer+x),
    "q": lambda x: globals().__setitem__("buffer", buffer+x),
    "r": lambda x: globals().__setitem__("buffer", buffer+x),
    "s": lambda x: globals().__setitem__("buffer", buffer+x),
    "t": lambda x: globals().__setitem__("buffer", buffer+x),
    "u": lambda x: globals().__setitem__("buffer", buffer+x),
    "v": lambda x: globals().__setitem__("buffer", buffer+x),
    "w": lambda x: globals().__setitem__("buffer", buffer+x),
    "x": lambda x: globals().__setitem__("buffer", buffer+x),
    "y": lambda x: globals().__setitem__("buffer", buffer+x),
    "z": lambda x: globals().__setitem__("buffer", buffer+x),
    '~': lambda x: globals().__setitem__("buffer", buffer+x),
    "§": lambda x: globals().__setitem__("buffer", buffer+x),
    "©": lambda x: globals().__setitem__("buffer", buffer+x),
    "«": lambda x: globals().__setitem__("buffer", buffer+x),
    "¯": lambda x: globals().__setitem__("buffer", buffer+x),
    "°": lambda x: globals().__setitem__("buffer", buffer+x),
    "±": lambda x: globals().__setitem__("buffer", buffer+x),
    "²": lambda x: globals().__setitem__("buffer", buffer+x),
    "µ": lambda x: globals().__setitem__("buffer", buffer+x),
    "»": lambda x: globals().__setitem__("buffer", buffer+x),
    "½": lambda x: globals().__setitem__("buffer", buffer+x),
    "À": lambda x: globals().__setitem__("buffer", buffer+x),
    "É": lambda x: globals().__setitem__("buffer", buffer+x),
    "Î": lambda x: globals().__setitem__("buffer", buffer+x),
    "à": lambda x: globals().__setitem__("buffer", buffer+x),
    "â": lambda x: globals().__setitem__("buffer", buffer+x),
    "ç": lambda x: globals().__setitem__("buffer", buffer+x),
    "è": lambda x: globals().__setitem__("buffer", buffer+x),
    "é": lambda x: globals().__setitem__("buffer", buffer+x),
    "ê": lambda x: globals().__setitem__("buffer", buffer+x),
    "ë": lambda x: globals().__setitem__("buffer", buffer+x),
    "î": lambda x: globals().__setitem__("buffer", buffer+x),
    "ï": lambda x: globals().__setitem__("buffer", buffer+x),
    "ñ": lambda x: globals().__setitem__("buffer", buffer+x),
    "ô": lambda x: globals().__setitem__("buffer", buffer+x),
    "ö": lambda x: globals().__setitem__("buffer", buffer+x),
    "ù": lambda x: globals().__setitem__("buffer", buffer+x),
    "û": lambda x: globals().__setitem__("buffer", buffer+x),
    "ü": lambda x: globals().__setitem__("buffer", buffer+x),
    " ": lambda x: globals().__setitem__("buffer", buffer+x)
}


def calculer_morpho(chaine):
    return chaine

def main():
    # filename = "../LEFFF/lefff-2.1_utf8.txt"
    # traiter_lefff(filename=filename, encoding='utf-8', buffering=53213)
    tmp = traiter_lexique(
        filename="../LEFFF/lefff-2.1_utf8.txt",
        mode='r',
        encoding='utf-8',
        errors='strict',
        buffering=1
    )
    cur = next(tmp, False)
    i = 0
    liste = collections.deque()
    while cur:
        liste.append(cur)
        cur = next(tmp, False)
    dump(liste, open("lexique_lefff.pickle", "wb"))

clear_buffer = lambda : globals().__setitem__('buffer', '')

def test():
    from nltk.featstruct import unify
    from pprint import pprint
    from _functools import reduce
    from yaml import dump

    sf = 'fs'

    # print(dump(lefff_codex(), default_flow_style=False))

    reduire = lambda x, y: dico_add(x, y)
    print(reduce(reduire, [lefff_codex()[x] for x in ('1', '2', '3')]))


def dico_add(dico1, dico2):
    for k, v in dico2.items():
        print(k, v)
        dico1[k]|=(v)
    return dico1





if __name__ == '__main__':
    test()
