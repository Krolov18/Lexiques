# coding: utf-8

import ply.lex as lex
import ply.yacc as yacc
import os
from abc import ABCMeta, abstractmethod


class Parser(metaclass=ABCMeta):
    """
        Classe inspirée de http://www.juanjoconti.com.ar/files/python/ply-examples/classcalc/calc.py

        Classe Abstraite

        Séparation de lex et de yacc afin de pouvoir utiliser l'un et l'autre indépendamment.

        Cette séparation n'est pas obligatoire. Pour une question de lisibilité pour les classes qui héritent
        de cette classe pour ce TP, je les ai mis dans la même classe.
    """
    tokens = ()
    precedence = ()

    @abstractmethod
    def __init__(self, **kwargs):
        """
            Ce constructeur permet de représenter les actions principales d'un parseur,
            qui sont l'action parse() et l'action recognise(). La troisième méthode run_while()
            est une méthode qui permet de rentrer directement des actions succéssives.
            Cette méthodes permet de tester la mise en mémoire de certaines actions (mémoisation).

            Ce constructeur peut soit être hérité d'une seule classe dans laquelle il y a tout. Le lexique et
            la syntaxe.
            Toutefois, on peut vouloir avoir une classe pour le lexique et une autre pour la syntaxe.
            C'est aussi possible.

        :param kw: parametre pour le fichier de debuggage et les exceptions
        """
        self.debug = kwargs.get('debug', 0)
        self.base = kwargs.get('excpetions', None)
        self.names = {}
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "_".join(["parser", self.__class__.__name__])
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"

        # Build the lexer and parser
        self.lexer = lex.lex(
            module=self,
            debug=self.debug
        )
        self.yacc = yacc.yacc(
            module=self,
            debug=self.debug,
            debugfile=self.debugfile,
            tabmodule=self.tabmodule
        )

    def run_while(self):
        """
            Méthode qui simule une boucle infinie permettant de tester la mise en mémoire
            de variables, pour la réutilisation.
        :return: None
        """
        s = ""
        while not s.startswith(':'):
            s = input("Tapez une chaine : ")
            print(self.yacc.parse(s))

    def recognise(self, data):
        """
            Méthode pouvant être réécrite qui sert à prendre une chaine en entrée et tester si celle-ci est conforme
            à un lexique. Elle retourne les LexToken() et/ou un message d'erreur quand il y a non conformité
            avec le lexique.
        :param data: chaine de caractères
        :return: liste des tokens
        """
        self.lexer.input(data)
        print(self.lexer.lextokens_all)
        # return self.lexer.input(data)

    def parse(self, c: str):
        """
            execute la méthode parse(c) de yacc.
        :param c:
        :return:
        """
        return self.yacc.parse(c)


def main():
    x = Parser()

if __name__ == '__main__':
    main()