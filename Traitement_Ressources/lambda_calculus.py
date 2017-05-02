# coding: utf-8

import typing
from string import ascii_lowercase
from Parser import Parser
from collections import deque, defaultdict


class LambdaCalculus(Parser):
    """
        Ce parseur permet de désambiguiser totalement un lambda terme.
        Cette classe prend un paramètre, le symbole qui sera utilisé comme marqueur pour une lambda-abstraction.
    """

    tokens = (
        "var",
    )

    literals = (
        "(",
        ")",
        ".",
        "∆"
    )

    def __init__(self, **kwargs):
        Parser.__init__(self, **kwargs)

    @staticmethod
    def t_var(t):
        r"""[A-Za-z]+"""
        return t

    @staticmethod
    def t_newline(t):
        r"""\n+"""
        t.lexer.lineo += len(t.value)
        return t

    t_ignore = " \t'"

    @staticmethod
    def t_error(t):
        print("Erreur lexicale: ", t)

    @staticmethod
    def p_axiom(p):
        """ axiome : terme """
        p[0] = p[1]

    @staticmethod
    def p_terme_var(p):
        """ terme : var """
        p[0] = Variable(p[1])
        Variable.free.add(p[0])

    @staticmethod
    def p_terme_lambda(p):
        """ terme : '∆' var '.' terme """
        var = Variable(p[2])
        Variable.free -= {var}
        Variable.bound.add(var)
        p[0] = Lambda(
            a=var,
            t=p[4]
        )

    @staticmethod
    def p_terme_app_func(p):
        """ terme : '(' terme ')' terme """
        p[0] = ApplicationFonctionnelle(
            t1=p[2],
            t2=p[4]
        )

    @staticmethod
    def p_error(p):
        print("Erreur syntaxique: ", p)

    def parse(self, c: str):
        return super(LambdaCalculus, self).parse(c)


class Terme(object):
    def __hash__(self):
        return 0


class Variable(Terme):
    bound = set()
    free = set()

    def __init__(self, a):
        self.a = a

    def __repr__(self):
        return self.a

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return self.a == other.a

    def __hash__(self):
        return 1

    @staticmethod
    def get_bound():
        return Variable.bound

    @staticmethod
    def get_free():
        return Variable.free


class ApplicationFonctionnelle(Terme):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2

    def __repr__(self):
        # return "({self.t1}){self.t2}".format(self=self)
        return "['af', {self.t1}, {self.t2}]".format(self=self)

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return (self.t1 == other.t1) and (self.t2 == other.t2)

    def __hash__(self):
        return 1


class Lambda(Terme):
    def __init__(self, a, t):
        self.a = a
        self.t = t

    def __repr__(self):
        # return "∆{self.a}.{self.t}".format(self=self)
        return "['la', {self.a}, {self.t}]".format(self=self)

    def __eq__(self, other):
        return (self.a == other.a) and (self.t == other.t)

    def __hash__(self):
        return 1


def reduce(t: Terme, trace=False) -> Terme:
    """
        Application de la bêta réduction.
        Si le Terme est une Variable, celui-ci est retourné tel quel.
        Sinon si le le Terme est une lambda-abstraction, on renvoie cette même lambda tout en appliquant
        la bêta réduction sur Lambda.terme.
        Enfin, si c'est une ApplicationFonctionnelle, on réduit terme1 et terme2, puis, on effectue
        l'application de terme1 réduit sur terme2 réduit.

    :param t: objet de type Terme ou sous classe de Terme (Variable, Lambda, ApplicationFonctionnelle
    :type t: Terme
    :param trace: mode debug
    :return: Cette fonction retourne un Terme ou une sous classe de Terme.
    """
    # if isinstance(t, Variable):
    if isinstance(t, str):
        return t
    # elif isinstance(t, Lambda):
    elif t[0] == "la":
        return Lambda(t.a, reduce(t.t, trace=trace))
    # elif isinstance(t, ApplicationFonctionnelle):
    elif t[0] == "af":
        return application(reduce(t.t1, trace=trace), reduce(t.t2, trace=trace), trace=trace)


def application(t1: Terme, t2: Terme, trace=False) -> Terme:
    """
        Cette fonction va appliquer la réduction en cas de redex.
        C'est à dire quand t1 est une lambda abstraction.
        Sans quoi on renvoie une ApplicationFonctionnelle de t1 et t2.

        trace permet d'afficher le foncteur, l'argument et le resultat de la beta reduction.
        L'application fonctionnelle de {l'argument} sur {la fonction} donne {le résultat de la bêta-reduction}

    :param t1: objet de type Terme ou sous classe de Terme (Variable, Lambda, ApplicationFonctionnelle
    :param t2: objet de type Terme ou sous classe de Terme (Variable, Lambda, ApplicationFonctionnelle
    :param trace: mode debug
    :return: Cette fonction retourne un Terme ou une sous classe de Terme.
    """
    # if isinstance(t1, Lambda):
    if t1[0] == 'la':
        # tmp = rename(t1.a, t2, t1.t)
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
        return ApplicationFonctionnelle(t1, t2)


def rename(a, t1, t2) -> Terme:
    """
        Cette fonction applique le remplacement des variables liées de x par t2 dans t1.
    :param a: Une Variable
    :param t1: objet de type Terme ou sous classe de Terme (Variable, Lambda, ApplicationFonctionnelle
    :param t2: objet de type Terme ou sous classe de Terme (Variable, Lambda, ApplicationFonctionnelle
    :return: Cette fonction retourne un terme ou une sous classe de Terme.
    """
    def replace(x: Variable):
        if x == a:
            return t1
        return x
    return func_mapping(replace, t2)


def alpha_reduction(t: Terme, e: set, q: defaultdict(deque), m: set):
    e -= m
    if isinstance(t, Variable):
        return t if t not in q else q.get(t)[-1]
    elif isinstance(t, Lambda):
        x = e.pop()
        m.add(x)
        q[t.a].append(x)
        return Lambda(q.get(t.a)[-1], alpha_reduction(t.t, e, q, m))
    elif isinstance(t, ApplicationFonctionnelle):
        return ApplicationFonctionnelle(alpha_reduction(t.t1, e, q, m), alpha_reduction(t.t2, e, q, m))


def func_mapping(func, t: Terme) -> Terme:
    """
        Cette fonction prend deux paramètres, une fonction et un Terme.
        Si le Terme est une Variable, il suffit de renvoyer l'application de cette fonction sur la Variable.
        Sinon si le Terme est une lamda-abstraction, on renvoie une lambda tout en appliquant récursivement
        fmap sur Lambda.terme avec la même fonction.
        Enfin, si le Terme est une ApplicationFonctionnelle, on applique récursivement fmap sur terme1 et terme2
        puis on renvoie une ApplicationFonctionnelle avec avec le résultat de fmap sur les deux arguments.
    :param func: fonction applicable sur un Terme
    :param t: objet de type Terme ou sous classe de Terme (Variable, Lambda, ApplicationFonctionnelle
    :return: On retourne un Terme ou une sous classe de Terme.
    """
    if isinstance(t, Variable):
        return func(t)
    elif isinstance(t, Lambda):
        return Lambda(t.a, func_mapping(func, t.t))
    elif isinstance(t, ApplicationFonctionnelle):
        return ApplicationFonctionnelle(func_mapping(func, t.t1), func_mapping(func, t.t2))


def encode_number(zero: str, succ: str, parser, n: int) -> Terme:
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
    :param parser: convertisseur de chaine de caractères en lambda terme
    :return: enodage d'un entier en un lambda terme
    """
    app_func = "({}){}"

    j = zero
    for i in range(1, n+1):
        j = reduce(parser.parse(app_func.format(succ, j)))
    return j


def encode_range(zero: str, succ: str, parser, seq: typing.Sequence) -> typing.Dict:
    """
        Généralisation de l'encodage d'un nombre à celui d'une séqeunce de nombres.
        Cette fonction renvoie un dictionnaire avec en clé un entier, en valeur une string encodant l'entier en ∆-calcul
    :param zero: lambda terme rerpésentant 0
    :param succ: lambda terme rerpésentant 0
    :param parser: convertisseur de chaine de caractères en lambda terme
    :param seq: séquence d'entiers
    :return: dictionnaire de lambda termes
    """
    return dict(map(lambda x: (x, encode_number(zero, succ, parser, x)), seq))


def is_free(x: Variable, t: Terme):
    """
        Dire si une variable x dans un terme t est libre.
    :param x: Variable
    :param t: Terme
    :return: Booléen
    """
    if isinstance(t, Variable):
        return x == t
    if isinstance(t, Lambda):
        return (t.a != x) and is_free(x, t.t)
    if isinstance(t, ApplicationFonctionnelle):
        return is_free(x, t.t1) or is_free(x, t.t2)


def is_bound(x: Variable, t: Terme):
    """
        Dire si une variable x dans un terme t est lié.
    :param x: Variable
    :param t: Terme
    :return: Booléen
    """
    if isinstance(t, Lambda):
        return (x == t.a) or is_bound(x, t.t)
    elif isinstance(t, ApplicationFonctionnelle):
        return is_bound(x, t.t1) or is_bound(x, t.t2)


def main():
    # global parseur
    parseur = LambdaCalculus()

    symboles = set(map(Variable, ascii_lowercase))

    succ_list = ['la', 'n', ['la', 'f', ['la', 'x', ['af', 'f', ['af', ['af', 'n', 'f'], 'x']]]]]
    plus_liste = ['la', 'm', ['la', 'n', ['la', 'f', ['la', 'x', ['af', ['af', 'm', 'f'], ['af', ['af', 'n', 'f'], 'x']]]]]]
    succ = "∆n.∆f.∆x.(f)((n)f)x"
    plus = "∆m.∆n.∆f.∆x.((m)f)((n)f)x"

    zero_liste = ['la', 'f', ['la', 'x', 'x']]
    zero = "∆f.∆x.x"
    # génération des nombres de 1 à 20
    numbers = encode_range(zero, succ, parseur, range(21))

    app_func1 = "({}){}"
    app_func2 = "(({}){}){}"

    # succession
    ope = parseur.parse(app_func1.format(succ, numbers[14]))
    print("variables libres: ", Variable.get_free())
    print("variables liées: ", Variable.get_bound())
    print("étape initiale: ", ope)
    print("étape finale: ", reduce(
        alpha_reduction(
            t=ope,
            e=symboles,
            q=defaultdict(deque),
            m=set()
        ), trace=True
    ))
    print()
    # addition avec la fonction addition
    ope = parseur.parse(app_func2.format(plus, numbers[9], numbers[7]))
    print("variables libres: ", Variable.get_free())
    print("variables liées: ", Variable.get_bound())
    print("étape initiale: ", ope)
    print("étape finale: ", reduce(
        alpha_reduction(
            t=ope,
            e=symboles,
            q=defaultdict(deque),
            m=set()
        ), trace=True
    ))
    print()
    # addition avec la fonction succession
    ope = parseur.parse(app_func2.format(numbers[12], succ, numbers[20]))
    print("variables libres: ", Variable.get_free())
    print("variables liées: ", Variable.get_bound())
    print("étape initiale: ", ope)
    print("étape finale: ", reduce(
        alpha_reduction(
            t=ope,
            e=symboles,
            q=defaultdict(deque),
            m=set()
        ), trace=True
    ))


if __name__ == '__main__':
    main()
