# Process this file with autoconf to produce a configure script.

AC_PREREQ(2.53)
AC_INIT(lefff, 3.4, benoit.sagot@inria.fr)
AM_INIT_AUTOMAKE

# Checks for programs.
AC_PROG_INSTALL
AC_PATH_PROG(PERL, perl)
if test "x$PERL" = x; then
	AC_MSG_ERROR(perl not found)
fi
AC_PATH_PROG(ICONV, iconv)
if test "x$ICONV" = x; then
	AC_MSG_ERROR(iconv not found)
fi

# Looking for alexina tools
AC_PATH_ALEXINATOOLS

PERLCC_OR_CP="cp -p"
PERLCC_OR_CP_INTERARG="" 

AC_ARG_ENABLE(
	perlcc,
	AC_HELP_STRING(
	       --enable-perlcc,
	       generate and use bytecode version of perl morpho scripts using perlcc
	),
	[PERLCC_OR_CP="perlcc -B"
	PERLCC_OR_CP_INTERARG=" -o "]
	,
)

if test "$PERLCC_OR_CP" = "perlcc -B"; then
   AC_PATH_PROG(PERLCC, perlcc)
   if test "x$PERLCC" = x; then
	AC_MSG_ERROR(perlcc not found thus --enable-perlcc can not be used)
   fi
fi


INCLUDE="include"; AC_SUBST(INCLUDE)

AC_SUBST(PERLCC_OR_CP)
AC_SUBST(PERLCC_OR_CP_INTERARG)
AC_CONFIG_FILES(Makefile)
AC_OUTPUT
