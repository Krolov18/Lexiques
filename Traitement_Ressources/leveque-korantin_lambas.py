# coding: utf-8

from string import ascii_lowercase
from collections import deque, defaultdict


def reduce(t, trace=False):
    """
        Fonction qui appelle la béta réduction
    :param t: terme (soit une lambda abstraction, une variable ou une application fonctionnelle)
    :param trace: en mode debug, cela permet de voir les étapes de réductions intermédiaires
    :return: un lambda terme
    """
    if isinstance(t, str):
        return t
    elif t[0] == "la":
        return ["la", t[1], reduce(t[2], trace=trace)]
    elif t[0] == "af":
        return application(reduce(t[1], trace=trace), reduce(t[2], trace=trace), trace=trace)


def application(t1, t2, trace=False):
    """
        Fonction qui applique la bétâ réduction.
    :param t1: terme (soit une lambda abstraction, une variable ou une application fonctionnelle)
    :param t2: terme (soit une lambda abstraction, une variable ou une application fonctionnelle)
    :param trace: en mode debug, cela permet de voir les étapes de réductions intermédiaires
    :return: un lambda terme
    """
    if t1[0] == 'la':
        tmp = rename(t1[1], t2, t1[2])
        if trace:
            print(
                "étape intermédiaire: l'application fonctionnelle de ({}){} ≡ {}".format(
                    t1,
                    t2,
                    tmp
                )
            )
        tmp = reduce(tmp, trace=trace)
        return tmp
    else:
        return ['af', t1, t2]


def rename(a, t1, t2):
    """
        fonction de renommage de variable. Fonction utilisée lors de l'alpha reduction
    :param a: variable
    :param t1: lambda terme
    :param t2: lambda terme
    :return: lambda terme
    """
    def replace(x):
        if x == a:
            return t1
        return x
    return func_mapping(replace, t2)


def alpha_reduction(t, e: set, q: defaultdict(deque), m: set):
    """
        Application de l'lpha réduction.
    :param t: lambda terme
    :param e: ensemble
    :param q: dictionnaire de listes
    :param m: ensemble
    :return: lambda terme
    """
    e -= m
    if isinstance(t, str):
        return t if t not in q else q.get(t)[-1]
    elif t[0] == 'la':
        x = e.pop()
        m.add(x)
        q[t[1]].append(x)
        return ['la', q.get(t[1])[-1], alpha_reduction(t[2], e, q, m)]
    elif t[0] == 'af':
        return ['af', alpha_reduction(t[1], e, q, m), alpha_reduction(t[2], e, q, m)]


def func_mapping(func, t):
    """
        equivalent de la fonction "map", soit l'application de func sur t,
        suivant des conditions.
    :param func: fonction
    :param t: lambda terme
    :return: lambda terme
    """
    if isinstance(t, str):
        return func(t)
    elif t[0] == 'la':
        return ['la', t[1], func_mapping(func, t[2])]
    elif t[0] == "af":
        return ["af", func_mapping(func, t[1]), func_mapping(func, t[2])]


def encode_number(zero, succ, n):
    """
        Cette fonction prend trois paramètre:
            chaine de caractères représentant 0,
            chaine de caractère représentant la fonction successeur,
            un parser convertissant une string en lambda terme,
            un entier
            On va donc à partir de zéro itérer jusqu'à n et retourner la dernière itération qui sera n encodé.
        algo:
            j: Terme; i: entier
            pour i de 1 à n faire
                j = BETA_REDUCTION(APPLICATION_FONCTIONNELLE(succ, j))
            retourne j
    :param succ: fonction successeur qui permettra d'encoder n en un lambda terme
    :param zero: lambda terme rerpésentant 0
    :param n: entier
    :return: enodage d'un entier en un lambda terme
    """
    def app_simple(x, y): return ['af', x, y]

    j = zero
    for i in range(1, n + 1):
        j = reduce(app_simple(succ, j))
    return j


def encode_range(zero, succ, seq):
    """
        Généralisation de l'encodage d'un nombre à une collection de nombres
    :param zero: lambda terme de zéro
    :param succ: fonction successeur encodé en lambda abstraction
    :param seq: une collection de nombres (ordonnée ou pas)
    :return: dictionnaire (clé=entier, valeur=lambda-expression)
    """
    return dict(map(lambda x: (x, encode_number(zero, succ, x)), seq))


def is_free(x, t):
    """
        Dire si une variable x dans un terme t est libre.
    :param x: Variable
    :param t: Terme
    :return: Booléen
    """
    if isinstance(t, str):
        return x == t
    if t[0] == "la":
        return (t[1] != x) and is_free(x, t[2])
    if t[0] == 'af':
        return is_free(x, t[1]) or is_free(x, t[2])


def is_bound(x, t):
    """
        Dire si une variable x dans un terme t est lié.
    :param x: Variable
    :param t: Terme
    :return: Booléen
    """
    if t[0] == "la":
        return (x == t[1]) or is_bound(x, t[2])
    elif t[0] == "af":
        return is_bound(x, t[1]) or is_bound(x, t[2])


def get_variables(t):
    """
        Récupérer les variables libres et liées d'une expression
    :param t: lambda terme
    :return: (variables_libres, variables_liées)
    """
    vars = set()
    liees = set()

    def ff(u): vars.add(u) if isinstance(u, str) else list(map(ff, u[1:]))

    ff(t)

    for x in vars:
        if is_bound(x, t):
            liees.add(x)
    libres = vars - liees

    return libres, liees


def main():
    succ_list = ['la', 'n', ['la', 'f', ['la', 'x', ['af', 'f', ['af', ['af', 'n', 'f'], 'x']]]]]
    plus_liste = ['la', 'm', ['la', 'n', ['la', 'f', ['la', 'x', ['af', ['af', 'm', 'f'], ['af', ['af', 'n', 'f'], 'x']]
                                                      ]]]]
    zero_liste = ['la', 'f', ['la', 'x', 'x']]

    def app_simple(x, y): return ['af', x, y]

    def app_double(x, y, z): return ['af', app_simple(x, y), z]

    symboles = set(ascii_lowercase)

    # génération des nombres de 1 à 20
    numbers = encode_range(zero_liste, succ_list, range(100))

    # succession
    ope = app_simple(succ_list, numbers[14])
    print("étape initiale: ", ope)
    ope = reduce(
        alpha_reduction(
            t=ope,
            e=symboles,
            q=defaultdict(deque),
            m=set()
        ), trace=True
    )
    print("étape finale: ", ope)
    (libres, liees) = get_variables(ope)
    print("variables libres: ", libres)
    print("variables liées: ", liees)
    print()
    # addition avec la fonction addition
    ope = app_double(plus_liste, numbers[9], numbers[7])
    print("étape initiale: ", ope)
    ope = reduce(
        alpha_reduction(
            t=ope,
            e=symboles,
            q=defaultdict(deque),
            m=set()
        ), trace=True
    )
    print("étape finale: ", ope)
    (libres, liees) = get_variables(ope)
    print("variables libres: ", libres)
    print("variables liées: ", liees)
    print()
    # addition avec la fonction succession
    ope = app_double(numbers[12], succ_list, numbers[20])
    print("étape initiale: ", ope)
    ope = reduce(
        alpha_reduction(
            t=ope,
            e=symboles,
            q=defaultdict(deque),
            m=set()
        ), trace=True
    )
    print("étape finale: ", ope)
    (libres, liees) = get_variables(ope)
    print("variables libres: ", libres)
    print("variables liées: ", liees)


if __name__ == '__main__':
    main()
