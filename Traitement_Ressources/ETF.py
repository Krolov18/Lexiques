# coding: utf-8

from abc import ABC, abstractmethod
from Parser import Parser
# from DocStringInheritance import DocInherit


class Lefffinterpreteur(Parser):
    def __init__(self, **kwargs):
        super(Lefffinterpreteur, self).__init__(**kwargs)
    tokens = (
        "VAL",
        "SEP",
        "NUM",
    )

    literals = (
        "(",
        ")",
        "<",
        ">",
        "@",
        ",",
        ":",
        "=",
        "[",
        "]",
        "|"
    )

    def t_VAL(self, t):
        r'["!\"#$%&*+-./;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz~§©«¯°±²µ»½ÀÉÎàâçèéêëîïñôöùûü"]+'
        return t

    def t_SEP(self, t):
        r'__+'
        return t

    def t_NUM(self, t):
        r'\d+'
        return t

    def t_newline(self, t):
        r"""\n+"""
        t.lexer.lineo += len(t.value)
        return t

    t_ignore = " \t'"

    def t_error(self, t):
        print("BUG")

    def p_A(self, p):
        """ A : '[' B ']' """
        p[0] = p
        print(p[0])


    def p_B_1(self, p):
        """ B : C ',' B """
        p[0] = p
        print(p[0])

    def p_B_2(self, p):
        """ B : C """
        p[0] = p
        print(p[0])

    def p_C(self, p):
        """ C : VAL '=' D """
        p[0] = p
        print(p[0])

    def p_D_1(self, p):
        """ D : "'" VAL SEP NUM E "'" """
        p[0] = p
        print(p[0])

    def p_D_2(self, p):
        """ D : VAL """
        p[0] = p
        print(p[0])

    def p_E(self, p):
        """ E : '<' F '>' """
        p[0] = p
        print(p[0])

    def p_F_1(self, p):
        """ F : G ',' F """
        p[0] = p
        print(p[0])

    def p_F_2(self, p):
        """ F : G """
        p[0] = p
        print(p[0])

    def p_G(self, p):
        """ G : VAL ':' H """
        p[0] = p
        print(p[0])

    def p_H_1(self, p):
        """ H : I """
        p[0] = p
        print(p[0])

    def p_H_2(self, p):
        """ H : VAL """
        p[0] = p
        print(p[0])

    def p_I(self, p):
        """ I : '(' J ')' """
        p[0] = p
        print(p[0])

    def p_J_1(self, p):
        """ J : VAL '|' J """
        p[0] = p
        print(p[0])

    def p_J_2(self, p):
        """ J : VAL """
        p[0] = p
        print(p[0])


    def p_error(self, p):
        print(p)
        print("Il y a une erreur")



def main():
    parseur = Lefffinterpreteur()

    ch3 = "[pred='à savoir_____1<arg1,arg2>',cat = coo]"
    ch2 = "[pred='St-Martin-d'Arberoue_____1<suj:(sn),obj:sn>',@loc,@ms]"
    parseur.run_while()
    # parseur.parse(ch3)


if __name__ == '__main__':
    main()
