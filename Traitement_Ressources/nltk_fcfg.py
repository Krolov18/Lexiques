# coding: utf-8

from nltk.parse.featurechart import InstantiateVarsChart
from nltk import parse


def main():
    cp = parse.load_parser(
        'grammar.fcfg',
        trace=1,
        chart_class=InstantiateVarsChart
    )
    print(cp.grammar())
    exit(1)
    for (i, phrase) in enumerate(phrases):
        default = "N.A."
        for (tree, formula) in analyses[i]:
            default = str(formula)
        print("Phrase: {}\nTraduction: {}".format(phrase, default))


def main2():
    import nltk
    nltk.download_gui()
    # cp = parse.load_parser('grammars/sample_grammar/bindop.fcfg',trace=1,chart_class=InstantiateVarsChart)


if __name__ == '__main__':
    main2()
