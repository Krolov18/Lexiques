# Process this file with automake to produce Makefile.in

LANGUAGE = fr

LEXFILES = adj.lex \
	       adv.lex \
	       interj.lex \
	       neg.lex \
	       conj.lex \
	       coord.lex \
	       det.lex \
	       nom.lex \
	       nomp.lex \
	       nompred.lex \
	       ponct.lex \
	       pref-suff.lex \
	       prep.lex \
	       pro.lex \
	       v.lex \
	       v-phd.lex \
	       v_new.lex \
	       entnom.lex \
	       uw.lex \
	       avoirC1pC2.lex \
	       avoirN1pC2.lex \
	       vC1pN2.lex \
	       vC1pC2.lex

LEX_ENCODING = L1

DOC = lefff-tagset-0.1.2.pdf

BUILT_SOURCES = alexina-makefile

include $(srcdir)/alexina-makefile

alexina-makefile: $(alexinatoolsdir)/alexina-makefile
	cp $< $@

