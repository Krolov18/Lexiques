# generated automatically by aclocal 1.11.1 -*- Autoconf -*-

# Copyright (C) 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004,
# 2005, 2006, 2007, 2008, 2009  Free Software Foundation, Inc.
# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, to the extent permitted by law; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.

m4_ifndef([AC_AUTOCONF_VERSION],
  [m4_copy([m4_PACKAGE_VERSION], [AC_AUTOCONF_VERSION])])dnl
m4_if(m4_defn([AC_AUTOCONF_VERSION]), [2.68],,
[m4_warning([this file was generated for autoconf 2.68.
You have another version of autoconf.  It may work, but is not guaranteed to.
If you have problems, you may need to regenerate the build system entirely.
To do so, use the procedure documented by the package, typically `autoreconf'.])])

# Copyright (C) 2002, 2003, 2005, 2006, 2007, 2008  Free Software Foundation, Inc.
#
# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# AM_AUTOMAKE_VERSION(VERSION)
# ----------------------------
# Automake X.Y traces this macro to ensure aclocal.m4 has been
# generated from the m4 files accompanying Automake X.Y.
# (This private macro should not be called outside this file.)
AC_DEFUN([AM_AUTOMAKE_VERSION],
[am__api_version='1.11'
dnl Some users find AM_AUTOMAKE_VERSION and mistake it for a way to
dnl require some minimum version.  Point them to the right macro.
m4_if([$1], [1.11.1], [],
      [AC_FATAL([Do not call $0, use AM_INIT_AUTOMAKE([$1]).])])dnl
])

# _AM_AUTOCONF_VERSION(VERSION)
# -----------------------------
# aclocal traces this macro to find the Autoconf version.
# This is a private macro too.  Using m4_define simplifies
# the logic in aclocal, which can simply ignore this definition.
m4_define([_AM_AUTOCONF_VERSION], [])

# AM_SET_CURRENT_AUTOMAKE_VERSION
# -------------------------------
# Call AM_AUTOMAKE_VERSION and AM_AUTOMAKE_VERSION so they can be traced.
# This function is AC_REQUIREd by AM_INIT_AUTOMAKE.
AC_DEFUN([AM_SET_CURRENT_AUTOMAKE_VERSION],
[AM_AUTOMAKE_VERSION([1.11.1])dnl
m4_ifndef([AC_AUTOCONF_VERSION],
  [m4_copy([m4_PACKAGE_VERSION], [AC_AUTOCONF_VERSION])])dnl
_AM_AUTOCONF_VERSION(m4_defn([AC_AUTOCONF_VERSION]))])

# AM_AUX_DIR_EXPAND                                         -*- Autoconf -*-

# Copyright (C) 2001, 2003, 2005  Free Software Foundation, Inc.
#
# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# For projects using AC_CONFIG_AUX_DIR([foo]), Autoconf sets
# $ac_aux_dir to `$srcdir/foo'.  In other projects, it is set to
# `$srcdir', `$srcdir/..', or `$srcdir/../..'.
#
# Of course, Automake must honor this variable whenever it calls a
# tool from the auxiliary directory.  The problem is that $srcdir (and
# therefore $ac_aux_dir as well) can be either absolute or relative,
# depending on how configure is run.  This is pretty annoying, since
# it makes $ac_aux_dir quite unusable in subdirectories: in the top
# source directory, any form will work fine, but in subdirectories a
# relative path needs to be adjusted first.
#
# $ac_aux_dir/missing
#    fails when called from a subdirectory if $ac_aux_dir is relative
# $top_srcdir/$ac_aux_dir/missing
#    fails if $ac_aux_dir is absolute,
#    fails when called from a subdirectory in a VPATH build with
#          a relative $ac_aux_dir
#
# The reason of the latter failure is that $top_srcdir and $ac_aux_dir
# are both prefixed by $srcdir.  In an in-source build this is usually
# harmless because $srcdir is `.', but things will broke when you
# start a VPATH build or use an absolute $srcdir.
#
# So we could use something similar to $top_srcdir/$ac_aux_dir/missing,
# iff we strip the leading $srcdir from $ac_aux_dir.  That would be:
#   am_aux_dir='\$(top_srcdir)/'`expr "$ac_aux_dir" : "$srcdir//*\(.*\)"`
# and then we would define $MISSING as
#   MISSING="\${SHELL} $am_aux_dir/missing"
# This will work as long as MISSING is not called from configure, because
# unfortunately $(top_srcdir) has no meaning in configure.
# However there are other variables, like CC, which are often used in
# configure, and could therefore not use this "fixed" $ac_aux_dir.
#
# Another solution, used here, is to always expand $ac_aux_dir to an
# absolute PATH.  The drawback is that using absolute paths prevent a
# configured tree to be moved without reconfiguration.

AC_DEFUN([AM_AUX_DIR_EXPAND],
[dnl Rely on autoconf to set up CDPATH properly.
AC_PREREQ([2.50])dnl
# expand $ac_aux_dir to an absolute path
am_aux_dir=`cd $ac_aux_dir && pwd`
])

# Do all the work for Automake.                             -*- Autoconf -*-

# Copyright (C) 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004,
# 2005, 2006, 2008, 2009 Free Software Foundation, Inc.
#
# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# serial 16

# This macro actually does too much.  Some checks are only needed if
# your package does certain things.  But this isn't really a big deal.

# AM_INIT_AUTOMAKE(PACKAGE, VERSION, [NO-DEFINE])
# AM_INIT_AUTOMAKE([OPTIONS])
# -----------------------------------------------
# The call with PACKAGE and VERSION arguments is the old style
# call (pre autoconf-2.50), which is being phased out.  PACKAGE
# and VERSION should now be passed to AC_INIT and removed from
# the call to AM_INIT_AUTOMAKE.
# We support both call styles for the transition.  After
# the next Automake release, Autoconf can make the AC_INIT
# arguments mandatory, and then we can depend on a new Autoconf
# release and drop the old call support.
AC_DEFUN([AM_INIT_AUTOMAKE],
[AC_PREREQ([2.62])dnl
dnl Autoconf wants to disallow AM_ names.  We explicitly allow
dnl the ones we care about.
m4_pattern_allow([^AM_[A-Z]+FLAGS$])dnl
AC_REQUIRE([AM_SET_CURRENT_AUTOMAKE_VERSION])dnl
AC_REQUIRE([AC_PROG_INSTALL])dnl
if test "`cd $srcdir && pwd`" != "`pwd`"; then
  # Use -I$(srcdir) only when $(srcdir) != ., so that make's output
  # is not polluted with repeated "-I."
  AC_SUBST([am__isrc], [' -I$(srcdir)'])_AM_SUBST_NOTMAKE([am__isrc])dnl
  # test to see if srcdir already configured
  if test -f $srcdir/config.status; then
    AC_MSG_ERROR([source directory already configured; run "make distclean" there first])
  fi
fi

# test whether we have cygpath
if test -z "$CYGPATH_W"; then
  if (cygpath --version) >/dev/null 2>/dev/null; then
    CYGPATH_W='cygpath -w'
  else
    CYGPATH_W=echo
  fi
fi
AC_SUBST([CYGPATH_W])

# Define the identity of the package.
dnl Distinguish between old-style and new-style calls.
m4_ifval([$2],
[m4_ifval([$3], [_AM_SET_OPTION([no-define])])dnl
 AC_SUBST([PACKAGE], [$1])dnl
 AC_SUBST([VERSION], [$2])],
[_AM_SET_OPTIONS([$1])dnl
dnl Diagnose old-style AC_INIT with new-style AM_AUTOMAKE_INIT.
m4_if(m4_ifdef([AC_PACKAGE_NAME], 1)m4_ifdef([AC_PACKAGE_VERSION], 1), 11,,
  [m4_fatal([AC_INIT should be called with package and version arguments])])dnl
 AC_SUBST([PACKAGE], ['AC_PACKAGE_TARNAME'])dnl
 AC_SUBST([VERSION], ['AC_PACKAGE_VERSION'])])dnl

_AM_IF_OPTION([no-define],,
[AC_DEFINE_UNQUOTED(PACKAGE, "$PACKAGE", [Name of package])
 AC_DEFINE_UNQUOTED(VERSION, "$VERSION", [Version number of package])])dnl

# Some tools Automake needs.
AC_REQUIRE([AM_SANITY_CHECK])dnl
AC_REQUIRE([AC_ARG_PROGRAM])dnl
AM_MISSING_PROG(ACLOCAL, aclocal-${am__api_version})
AM_MISSING_PROG(AUTOCONF, autoconf)
AM_MISSING_PROG(AUTOMAKE, automake-${am__api_version})
AM_MISSING_PROG(AUTOHEADER, autoheader)
AM_MISSING_PROG(MAKEINFO, makeinfo)
AC_REQUIRE([AM_PROG_INSTALL_SH])dnl
AC_REQUIRE([AM_PROG_INSTALL_STRIP])dnl
AC_REQUIRE([AM_PROG_MKDIR_P])dnl
# We need awk for the "check" target.  The system "awk" is bad on
# some platforms.
AC_REQUIRE([AC_PROG_AWK])dnl
AC_REQUIRE([AC_PROG_MAKE_SET])dnl
AC_REQUIRE([AM_SET_LEADING_DOT])dnl
_AM_IF_OPTION([tar-ustar], [_AM_PROG_TAR([ustar])],
	      [_AM_IF_OPTION([tar-pax], [_AM_PROG_TAR([pax])],
			     [_AM_PROG_TAR([v7])])])
_AM_IF_OPTION([no-dependencies],,
[AC_PROVIDE_IFELSE([AC_PROG_CC],
		  [_AM_DEPENDENCIES(CC)],
		  [define([AC_PROG_CC],
			  defn([AC_PROG_CC])[_AM_DEPENDENCIES(CC)])])dnl
AC_PROVIDE_IFELSE([AC_PROG_CXX],
		  [_AM_DEPENDENCIES(CXX)],
		  [define([AC_PROG_CXX],
			  defn([AC_PROG_CXX])[_AM_DEPENDENCIES(CXX)])])dnl
AC_PROVIDE_IFELSE([AC_PROG_OBJC],
		  [_AM_DEPENDENCIES(OBJC)],
		  [define([AC_PROG_OBJC],
			  defn([AC_PROG_OBJC])[_AM_DEPENDENCIES(OBJC)])])dnl
])
_AM_IF_OPTION([silent-rules], [AC_REQUIRE([AM_SILENT_RULES])])dnl
dnl The `parallel-tests' driver may need to know about EXEEXT, so add the
dnl `am__EXEEXT' conditional if _AM_COMPILER_EXEEXT was seen.  This macro
dnl is hooked onto _AC_COMPILER_EXEEXT early, see below.
AC_CONFIG_COMMANDS_PRE(dnl
[m4_provide_if([_AM_COMPILER_EXEEXT],
  [AM_CONDITIONAL([am__EXEEXT], [test -n "$EXEEXT"])])])dnl
])

dnl Hook into `_AC_COMPILER_EXEEXT' early to learn its expansion.  Do not
dnl add the conditional right here, as _AC_COMPILER_EXEEXT may be further
dnl mangled by Autoconf and run in a shell conditional statement.
m4_define([_AC_COMPILER_EXEEXT],
m4_defn([_AC_COMPILER_EXEEXT])[m4_provide([_AM_COMPILER_EXEEXT])])


# When config.status generates a header, we must update the stamp-h file.
# This file resides in the same directory as the config header
# that is generated.  The stamp files are numbered to have different names.

# Autoconf calls _AC_AM_CONFIG_HEADER_HOOK (when defined) in the
# loop where config.status creates the headers, so we can generate
# our stamp files there.
AC_DEFUN([_AC_AM_CONFIG_HEADER_HOOK],
[# Compute $1's index in $config_headers.
_am_arg=$1
_am_stamp_count=1
for _am_header in $config_headers :; do
  case $_am_header in
    $_am_arg | $_am_arg:* )
      break ;;
    * )
      _am_stamp_count=`expr $_am_stamp_count + 1` ;;
  esac
done
echo "timestamp for $_am_arg" >`AS_DIRNAME(["$_am_arg"])`/stamp-h[]$_am_stamp_count])

# Copyright (C) 2001, 2003, 2005, 2008  Free Software Foundation, Inc.
#
# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# AM_PROG_INSTALL_SH
# ------------------
# Define $install_sh.
AC_DEFUN([AM_PROG_INSTALL_SH],
[AC_REQUIRE([AM_AUX_DIR_EXPAND])dnl
if test x"${install_sh}" != xset; then
  case $am_aux_dir in
  *\ * | *\	*)
    install_sh="\${SHELL} '$am_aux_dir/install-sh'" ;;
  *)
    install_sh="\${SHELL} $am_aux_dir/install-sh"
  esac
fi
AC_SUBST(install_sh)])

# Copyright (C) 2003, 2005  Free Software Foundation, Inc.
#
# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# serial 2

# Check whether the underlying file-system supports filenames
# with a leading dot.  For instance MS-DOS doesn't.
AC_DEFUN([AM_SET_LEADING_DOT],
[rm -rf .tst 2>/dev/null
mkdir .tst 2>/dev/null
if test -d .tst; then
  am__leading_dot=.
else
  am__leading_dot=_
fi
rmdir .tst 2>/dev/null
AC_SUBST([am__leading_dot])])

# Fake the existence of programs that GNU maintainers use.  -*- Autoconf -*-

# Copyright (C) 1997, 1999, 2000, 2001, 2003, 2004, 2005, 2008
# Free Software Foundation, Inc.
#
# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# serial 6

# AM_MISSING_PROG(NAME, PROGRAM)
# ------------------------------
AC_DEFUN([AM_MISSING_PROG],
[AC_REQUIRE([AM_MISSING_HAS_RUN])
$1=${$1-"${am_missing_run}$2"}
AC_SUBST($1)])


# AM_MISSING_HAS_RUN
# ------------------
# Define MISSING if not defined so far and test if it supports --run.
# If it does, set am_missing_run to use it, otherwise, to nothing.
AC_DEFUN([AM_MISSING_HAS_RUN],
[AC_REQUIRE([AM_AUX_DIR_EXPAND])dnl
AC_REQUIRE_AUX_FILE([missing])dnl
if test x"${MISSING+set}" != xset; then
  case $am_aux_dir in
  *\ * | *\	*)
    MISSING="\${SHELL} \"$am_aux_dir/missing\"" ;;
  *)
    MISSING="\${SHELL} $am_aux_dir/missing" ;;
  esac
fi
# Use eval to expand $SHELL
if eval "$MISSING --run true"; then
  am_missing_run="$MISSING --run "
else
  am_missing_run=
  AC_MSG_WARN([`missing' script is too old or missing])
fi
])

# Copyright (C) 2003, 2004, 2005, 2006  Free Software Foundation, Inc.
#
# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# AM_PROG_MKDIR_P
# ---------------
# Check for `mkdir -p'.
AC_DEFUN([AM_PROG_MKDIR_P],
[AC_PREREQ([2.60])dnl
AC_REQUIRE([AC_PROG_MKDIR_P])dnl
dnl Automake 1.8 to 1.9.6 used to define mkdir_p.  We now use MKDIR_P,
dnl while keeping a definition of mkdir_p for backward compatibility.
dnl @MKDIR_P@ is magic: AC_OUTPUT adjusts its value for each Makefile.
dnl However we cannot define mkdir_p as $(MKDIR_P) for the sake of
dnl Makefile.ins that do not define MKDIR_P, so we do our own
dnl adjustment using top_builddir (which is defined more often than
dnl MKDIR_P).
AC_SUBST([mkdir_p], ["$MKDIR_P"])dnl
case $mkdir_p in
  [[\\/$]]* | ?:[[\\/]]*) ;;
  */*) mkdir_p="\$(top_builddir)/$mkdir_p" ;;
esac
])

# Helper functions for option handling.                     -*- Autoconf -*-

# Copyright (C) 2001, 2002, 2003, 2005, 2008  Free Software Foundation, Inc.
#
# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# serial 4

# _AM_MANGLE_OPTION(NAME)
# -----------------------
AC_DEFUN([_AM_MANGLE_OPTION],
[[_AM_OPTION_]m4_bpatsubst($1, [[^a-zA-Z0-9_]], [_])])

# _AM_SET_OPTION(NAME)
# ------------------------------
# Set option NAME.  Presently that only means defining a flag for this option.
AC_DEFUN([_AM_SET_OPTION],
[m4_define(_AM_MANGLE_OPTION([$1]), 1)])

# _AM_SET_OPTIONS(OPTIONS)
# ----------------------------------
# OPTIONS is a space-separated list of Automake options.
AC_DEFUN([_AM_SET_OPTIONS],
[m4_foreach_w([_AM_Option], [$1], [_AM_SET_OPTION(_AM_Option)])])

# _AM_IF_OPTION(OPTION, IF-SET, [IF-NOT-SET])
# -------------------------------------------
# Execute IF-SET if OPTION is set, IF-NOT-SET otherwise.
AC_DEFUN([_AM_IF_OPTION],
[m4_ifset(_AM_MANGLE_OPTION([$1]), [$2], [$3])])

# Check to make sure that the build environment is sane.    -*- Autoconf -*-

# Copyright (C) 1996, 1997, 2000, 2001, 2003, 2005, 2008
# Free Software Foundation, Inc.
#
# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# serial 5

# AM_SANITY_CHECK
# ---------------
AC_DEFUN([AM_SANITY_CHECK],
[AC_MSG_CHECKING([whether build environment is sane])
# Just in case
sleep 1
echo timestamp > conftest.file
# Reject unsafe characters in $srcdir or the absolute working directory
# name.  Accept space and tab only in the latter.
am_lf='
'
case `pwd` in
  *[[\\\"\#\$\&\'\`$am_lf]]*)
    AC_MSG_ERROR([unsafe absolute working directory name]);;
esac
case $srcdir in
  *[[\\\"\#\$\&\'\`$am_lf\ \	]]*)
    AC_MSG_ERROR([unsafe srcdir value: `$srcdir']);;
esac

# Do `set' in a subshell so we don't clobber the current shell's
# arguments.  Must try -L first in case configure is actually a
# symlink; some systems play weird games with the mod time of symlinks
# (eg FreeBSD returns the mod time of the symlink's containing
# directory).
if (
   set X `ls -Lt "$srcdir/configure" conftest.file 2> /dev/null`
   if test "$[*]" = "X"; then
      # -L didn't work.
      set X `ls -t "$srcdir/configure" conftest.file`
   fi
   rm -f conftest.file
   if test "$[*]" != "X $srcdir/configure conftest.file" \
      && test "$[*]" != "X conftest.file $srcdir/configure"; then

      # If neither matched, then we have a broken ls.  This can happen
      # if, for instance, CONFIG_SHELL is bash and it inherits a
      # broken ls alias from the environment.  This has actually
      # happened.  Such a system could not be considered "sane".
      AC_MSG_ERROR([ls -t appears to fail.  Make sure there is not a broken
alias in your environment])
   fi

   test "$[2]" = conftest.file
   )
then
   # Ok.
   :
else
   AC_MSG_ERROR([newly created file is older than distributed files!
Check your system clock])
fi
AC_MSG_RESULT(yes)])

# Copyright (C) 2001, 2003, 2005  Free Software Foundation, Inc.
#
# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# AM_PROG_INSTALL_STRIP
# ---------------------
# One issue with vendor `install' (even GNU) is that you can't
# specify the program used to strip binaries.  This is especially
# annoying in cross-compiling environments, where the build's strip
# is unlikely to handle the host's binaries.
# Fortunately install-sh will honor a STRIPPROG variable, so we
# always use install-sh in `make install-strip', and initialize
# STRIPPROG with the value of the STRIP variable (set by the user).
AC_DEFUN([AM_PROG_INSTALL_STRIP],
[AC_REQUIRE([AM_PROG_INSTALL_SH])dnl
# Installed binaries are usually stripped using `strip' when the user
# run `make install-strip'.  However `strip' might not be the right
# tool to use in cross-compilation environments, therefore Automake
# will honor the `STRIP' environment variable to overrule this program.
dnl Don't test for $cross_compiling = yes, because it might be `maybe'.
if test "$cross_compiling" != no; then
  AC_CHECK_TOOL([STRIP], [strip], :)
fi
INSTALL_STRIP_PROGRAM="\$(install_sh) -c -s"
AC_SUBST([INSTALL_STRIP_PROGRAM])])

# Copyright (C) 2006, 2008  Free Software Foundation, Inc.
#
# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# serial 2

# _AM_SUBST_NOTMAKE(VARIABLE)
# ---------------------------
# Prevent Automake from outputting VARIABLE = @VARIABLE@ in Makefile.in.
# This macro is traced by Automake.
AC_DEFUN([_AM_SUBST_NOTMAKE])

# AM_SUBST_NOTMAKE(VARIABLE)
# ---------------------------
# Public sister of _AM_SUBST_NOTMAKE.
AC_DEFUN([AM_SUBST_NOTMAKE], [_AM_SUBST_NOTMAKE($@)])

# Check how to create a tarball.                            -*- Autoconf -*-

# Copyright (C) 2004, 2005  Free Software Foundation, Inc.
#
# This file is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# serial 2

# _AM_PROG_TAR(FORMAT)
# --------------------
# Check how to create a tarball in format FORMAT.
# FORMAT should be one of `v7', `ustar', or `pax'.
#
# Substitute a variable $(am__tar) that is a command
# writing to stdout a FORMAT-tarball containing the directory
# $tardir.
#     tardir=directory && $(am__tar) > result.tar
#
# Substitute a variable $(am__untar) that extract such
# a tarball read from stdin.
#     $(am__untar) < result.tar
AC_DEFUN([_AM_PROG_TAR],
[# Always define AMTAR for backward compatibility.
AM_MISSING_PROG([AMTAR], [tar])
m4_if([$1], [v7],
     [am__tar='${AMTAR} chof - "$$tardir"'; am__untar='${AMTAR} xf -'],
     [m4_case([$1], [ustar],, [pax],,
              [m4_fatal([Unknown tar format])])
AC_MSG_CHECKING([how to create a $1 tar archive])
# Loop over all known methods to create a tar archive until one works.
_am_tools='gnutar m4_if([$1], [ustar], [plaintar]) pax cpio none'
_am_tools=${am_cv_prog_tar_$1-$_am_tools}
# Do not fold the above two line into one, because Tru64 sh and
# Solaris sh will not grok spaces in the rhs of `-'.
for _am_tool in $_am_tools
do
  case $_am_tool in
  gnutar)
    for _am_tar in tar gnutar gtar;
    do
      AM_RUN_LOG([$_am_tar --version]) && break
    done
    am__tar="$_am_tar --format=m4_if([$1], [pax], [posix], [$1]) -chf - "'"$$tardir"'
    am__tar_="$_am_tar --format=m4_if([$1], [pax], [posix], [$1]) -chf - "'"$tardir"'
    am__untar="$_am_tar -xf -"
    ;;
  plaintar)
    # Must skip GNU tar: if it does not support --format= it doesn't create
    # ustar tarball either.
    (tar --version) >/dev/null 2>&1 && continue
    am__tar='tar chf - "$$tardir"'
    am__tar_='tar chf - "$tardir"'
    am__untar='tar xf -'
    ;;
  pax)
    am__tar='pax -L -x $1 -w "$$tardir"'
    am__tar_='pax -L -x $1 -w "$tardir"'
    am__untar='pax -r'
    ;;
  cpio)
    am__tar='find "$$tardir" -print | cpio -o -H $1 -L'
    am__tar_='find "$tardir" -print | cpio -o -H $1 -L'
    am__untar='cpio -i -H $1 -d'
    ;;
  none)
    am__tar=false
    am__tar_=false
    am__untar=false
    ;;
  esac

  # If the value was cached, stop now.  We just wanted to have am__tar
  # and am__untar set.
  test -n "${am_cv_prog_tar_$1}" && break

  # tar/untar a dummy directory, and stop if the command works
  rm -rf conftest.dir
  mkdir conftest.dir
  echo GrepMe > conftest.dir/file
  AM_RUN_LOG([tardir=conftest.dir && eval $am__tar_ >conftest.tar])
  rm -rf conftest.dir
  if test -s conftest.tar; then
    AM_RUN_LOG([$am__untar <conftest.tar])
    grep GrepMe conftest.dir/file >/dev/null 2>&1 && break
  fi
done
rm -rf conftest.dir

AC_CACHE_VAL([am_cv_prog_tar_$1], [am_cv_prog_tar_$1=$_am_tool])
AC_MSG_RESULT([$am_cv_prog_tar_$1])])
AC_SUBST([am__tar])
AC_SUBST([am__untar])
]) # _AM_PROG_TAR

dnl Autoconf macros for alexina-tools, including lexed
dnl $Id: lexed.m4 1116 2007-03-09 09:40:04Z icabrera $

dnl AM_PATH_LEXED: macro for lexed (inspired from gpme package)
AC_DEFUN([AM_PATH_LEXED],
[ AC_PREREQ(2.57)dnl
  AC_ARG_WITH(lexed-prefix,
            AC_HELP_STRING([--with-lexed-prefix=PFX],
                           [prefix where LEXED is installed (optional)]),
     lexed_config_prefix="$withval", lexed_config_prefix="")
  if test x$lexed_config_prefix != x ; then
     lexed_config_args="$lexed_config_args --prefix=$lexed_config_prefix"
     if test x${LEXED_CONFIG+set} != xset ; then
        LEXED_CONFIG=$lexed_config_prefix/bin/lexed-config
     fi
  fi

  AC_PATH_PROG(LEXED_CONFIG, lexed-config, no)
  min_lexed_version=ifelse([$1], ,0.3.9,$1)
  AC_MSG_CHECKING(for LEXED - version >= $min_lexed_version)
  ok=no
  if test "$LEXED_CONFIG" != "no" ; then
    req_major=`echo $min_lexed_version | \
               sed 's/\([[0-9]]*\)\.\([[0-9]]*\)\.\([[0-9]]*\)/\1/'`
    req_minor=`echo $min_lexed_version | \
               sed 's/\([[0-9]]*\)\.\([[0-9]]*\)\.\([[0-9]]*\)/\2/'`
    req_micro=`echo $min_lexed_version | \
               sed 's/\([[0-9]]*\)\.\([[0-9]]*\)\.\([[0-9]]*\)/\3/'`
    lexed_config_version=`$LEXED_CONFIG $lexed_config_args --version`
    major=`echo $lexed_config_version | \
               sed 's/\([[0-9]]*\)\.\([[0-9]]*\)\.\([[0-9]]*\).*/\1/'`
    minor=`echo $lexed_config_version | \
               sed 's/\([[0-9]]*\)\.\([[0-9]]*\)\.\([[0-9]]*\).*/\2/'`
    micro=`echo $lexed_config_version | \
               sed 's/\([[0-9]]*\)\.\([[0-9]]*\)\.\([[0-9]]*\).*/\3/'`
    if test "$major" -gt "$req_major"; then
        ok=yes
    else 
        if test "$major" -eq "$req_major"; then
            if test "$minor" -gt "$req_minor"; then
               ok=yes
            else
               if test "$minor" -eq "$req_minor"; then
                   if test "$micro" -ge "$req_micro"; then
                     ok=yes
                   fi
               fi
            fi
        fi
    fi
  fi
  if test $ok = yes; then
    LEXED_CFLAGS=`$LEXED_CONFIG $lexed_config_args --cflags`
    LEXED_LIBS=`$LEXED_CONFIG $lexed_config_args --libs`
    AC_MSG_RESULT(yes)
    ifelse([$2], , :, [$2])
  else
    LEXED_CFLAGS=""
    LEXED_LIBS=""
    AC_MSG_RESULT(no)
    ifelse([$3], , :, [$3])
  fi
  AC_SUBST(LEXED_CFLAGS)
  AC_SUBST(LEXED_LIBS)
])

# AC_PATH_ALEXINA
# Test for alexina installation (i.e., at least one alexina lexicon)
# defines alexinadir
AC_DEFUN([AC_PATH_ALEXINA], [
	AC_ARG_WITH(
		alexinadir,
		AC_HELP_STRING(
		       --with-alexinadir=DIR,
		       path where alexina (lexicons) directory is installed
		),
		alexinadir=$withval,
		if test -d $datadir/alexina; then
			alexinadir=$datadir/alexina
		else
			if test -d $prefix/share/alexina; then
				alexinadir=$prefix/share/alexina
			else
				if test -d /usr/local/share/alexina; then
					alexinadir=/usr/local/share/alexina
				else
					if test -d /usr/share/alexina; then
						alexinadir=/usr/share/alexina
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for Alexina lexicons hierarchy)

	# check validity
	if test -d "$alexinadir"; then
		# expand to an absolute path
		alexinadir=`cd $alexinadir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	AC_SUBST(alexinadir)

])

# AC_PATH_ALEDA
# Test for aleda, the alexina named entity database
# defines aledalibdir
AC_DEFUN([AC_PATH_ALEDA], [
	AC_ARG_WITH(
		aledalibdir,
		AC_HELP_STRING(
		       --with-aledalibdir=DIR,
		       path where the aleda databases are installed
		),
		aledalibdir=$withval,
		if test -d $datadir/aleda; then
			aledalibdir=$datadir/aleda
		else
			if test -d $prefix/share/aleda; then
				aledalibdir=$prefix/share/aleda
			else
				if test -d /usr/local/share/aleda; then
					aledalibdir=/usr/local/share/aleda
				else
					if test -d /usr/share/aleda; then
						aledalibdir=/usr/share/aleda
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for the Aleda database)

	# check validity
	if test -d "$aledalibdir"; then
		# expand to an absolute path
		aledalibdir=`cd $aledalibdir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	AC_SUBST(aledalibdir)

])

AC_DEFUN([AC_PATH_ALEXINATOOLS], [
	AC_ARG_WITH(
		alexinatoolsdir,
		AC_HELP_STRING(
		       --with-alexinatoolsdir=DIR,
		       path where alexina-tools directory is installed
		),
		alexinatoolsdir=$withval,
		if test -d $datadir/alexina-tools; then
			alexinatoolsdir=$datadir/alexina-tools
		else
			if test -d $prefix/share/alexina-tools; then
				alexinatoolsdir=$prefix/share/alexina-tools
			else
				if test -d /usr/local/share/alexina-tools; then
					alexinatoolsdir=/usr/local/share/alexina-tools
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for Alexina tools)

	# check validity
	if test -d "$alexinatoolsdir"; then
		# expand to an absolute path
		alexinatoolsdir=`cd $alexinatoolsdir && pwd`
		AC_MSG_RESULT(yes (alexinatoolsdir=$alexinatoolsdir))
	else
		AC_MSG_RESULT(no)
	fi

	AC_SUBST(alexinatoolsdir)

])


# AC_PATH_SKLEX
# Test for SkLex installation
# defines sklexdir
AC_DEFUN([AC_PATH_SKLEX], [
	AC_ARG_WITH(
		sklexdir,
		AC_HELP_STRING(
		       --with-sklexdir=DIR,
		       path where sklex is installed
		),
		sklexdir=,
		if test -d $datadir/sklex; then
			sklexdir=$datadir/sklex
		else
			if test -d $prefix/share/sklex; then
				sklexdir=$prefix/share/sklex
			else
				if test -d /usr/local/share/sklex; then
					sklexdir=/usr/local/share/sklex
				else
					if test -d /usr/share/sklex; then
						sklexdir=/usr/share/sklex
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for SkLex)

	# check validity
	if test -d "$sklexdir"; then
		# expand to an absolute path
		sklexdir=`cd $sklexdir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	sklexdir=$sklexdir
	AC_SUBST(sklexdir)
	AC_SUBST(sklexdir)
])


# AC_PATH_LEFFF
# Test for Lefff installation
# defines lefffdir
AC_DEFUN([AC_PATH_LEFFF], [
	AC_ARG_WITH(
		lefffdir,
		AC_HELP_STRING(
		       --with-lefffdir=DIR,
		       path where lefff is installed
		),
		lefffdir=,
		if test -d $datadir/lefff; then
			lefffdir=$datadir/lefff
		else
			if test -d $prefix/share/lefff; then
				lefffdir=$prefix/share/lefff
			else
				if test -d /usr/local/share/lefff; then
					lefffdir=/usr/local/share/lefff
				else
					if test -d /usr/share/lefff; then
						lefffdir=/usr/share/lefff
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for Lefff)

	# check validity
	if test -d "$lefffdir"; then
		# expand to an absolute path
		lefffdir=`cd $lefffdir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	frlexdir=$lefffdir
	AC_SUBST(lefffdir)
	AC_SUBST(frlexdir)
])


# AC_PATH_RULEX
# Test for RuLex installation
# defines rulexdir
AC_DEFUN([AC_PATH_RULEX], [
	AC_ARG_WITH(
		rulexdir,
		AC_HELP_STRING(
		       --with-rulexdir=DIR,
		       path where rulex is installed
		),
		rulexdir=,
		if test -d $datadir/rulex; then
			rulexdir=$datadir/rulex
		else
			if test -d $prefix/share/rulex; then
				rulexdir=$prefix/share/rulex
			else
				if test -d /usr/local/share/rulex; then
					rulexdir=/usr/local/share/rulex
				else
					if test -d /usr/share/rulex; then
						rulexdir=/usr/share/rulex
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for RuLex)

	# check validity
	if test -d "$rulexdir"; then
		# expand to an absolute path
		rulexdir=`cd $rulexdir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	rulexdir=$rulexdir
	AC_SUBST(rulexdir)
	AC_SUBST(rulexdir)
])


# AC_PATH_SALDO
# Test for Saldo installation
# defines saldodir
AC_DEFUN([AC_PATH_SALDO], [
	AC_ARG_WITH(
		saldodir,
		AC_HELP_STRING(
		       --with-saldodir=DIR,
		       path where saldo is installed
		),
		saldodir=,
		if test -d $datadir/saldo; then
			saldodir=$datadir/saldo
		else
			if test -d $prefix/share/saldo; then
				saldodir=$prefix/share/saldo
			else
				if test -d /usr/local/share/saldo; then
					saldodir=/usr/local/share/saldo
				else
					if test -d /usr/share/saldo; then
						saldodir=/usr/share/saldo
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for Saldo)

	# check validity
	if test -d "$saldodir"; then
		# expand to an absolute path
		saldodir=`cd $saldodir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	svlexdir=$saldodir
	AC_SUBST(saldodir)
	AC_SUBST(svlexdir)
])


# AC_PATH_FRWIKTIONARY_ALEXINA
# Test for frwiktionary_alexina installation
# defines frwiktionary_alexinadir
AC_DEFUN([AC_PATH_FRWIKTIONARY_ALEXINA], [
	AC_ARG_WITH(
		frwiktionary_alexinadir,
		AC_HELP_STRING(
		       --with-frwiktionary_alexinadir=DIR,
		       path where frwiktionary_alexina is installed
		),
		frwiktionary_alexinadir=,
		if test -d $datadir/frwiktionary_alexina; then
			frwiktionary_alexinadir=$datadir/frwiktionary_alexina
		else
			if test -d $prefix/share/frwiktionary_alexina; then
				frwiktionary_alexinadir=$prefix/share/frwiktionary_alexina
			else
				if test -d /usr/local/share/frwiktionary_alexina; then
					frwiktionary_alexinadir=/usr/local/share/frwiktionary_alexina
				else
					if test -d /usr/share/frwiktionary_alexina; then
						frwiktionary_alexinadir=/usr/share/frwiktionary_alexina
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for frwiktionary_alexina)

	# check validity
	if test -d "$frwiktionary_alexinadir"; then
		# expand to an absolute path
		frwiktionary_alexinadir=`cd $frwiktionary_alexinadir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	frWlexdir=$frwiktionary_alexinadir
	AC_SUBST(frwiktionary_alexinadir)
	AC_SUBST(frWlexdir)
])


# AC_PATH_PERLEX
# Test for PerLex installation
# defines perlexdir
AC_DEFUN([AC_PATH_PERLEX], [
	AC_ARG_WITH(
		perlexdir,
		AC_HELP_STRING(
		       --with-perlexdir=DIR,
		       path where perlex is installed
		),
		perlexdir=,
		if test -d $datadir/perlex; then
			perlexdir=$datadir/perlex
		else
			if test -d $prefix/share/perlex; then
				perlexdir=$prefix/share/perlex
			else
				if test -d /usr/local/share/perlex; then
					perlexdir=/usr/local/share/perlex
				else
					if test -d /usr/share/perlex; then
						perlexdir=/usr/share/perlex
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for PerLex)

	# check validity
	if test -d "$perlexdir"; then
		# expand to an absolute path
		perlexdir=`cd $perlexdir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	falexdir=$perlexdir
	AC_SUBST(perlexdir)
	AC_SUBST(falexdir)
])


# AC_PATH_SLOLEKS
# Test for SloLeks installation
# defines sloleksdir
AC_DEFUN([AC_PATH_SLOLEKS], [
	AC_ARG_WITH(
		sloleksdir,
		AC_HELP_STRING(
		       --with-sloleksdir=DIR,
		       path where sloleks is installed
		),
		sloleksdir=,
		if test -d $datadir/sloleks; then
			sloleksdir=$datadir/sloleks
		else
			if test -d $prefix/share/sloleks; then
				sloleksdir=$prefix/share/sloleks
			else
				if test -d /usr/local/share/sloleks; then
					sloleksdir=/usr/local/share/sloleks
				else
					if test -d /usr/share/sloleks; then
						sloleksdir=/usr/share/sloleks
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for SloLeks)

	# check validity
	if test -d "$sloleksdir"; then
		# expand to an absolute path
		sloleksdir=`cd $sloleksdir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	silexdir=$sloleksdir
	AC_SUBST(sloleksdir)
	AC_SUBST(silexdir)
])


# AC_PATH_PROLEX_ALEXINA
# Test for prolex_alexina installation
# defines prolex_alexinadir
AC_DEFUN([AC_PATH_PROLEX_ALEXINA], [
	AC_ARG_WITH(
		prolex_alexinadir,
		AC_HELP_STRING(
		       --with-prolex_alexinadir=DIR,
		       path where prolex_alexina is installed
		),
		prolex_alexinadir=,
		if test -d $datadir/prolex_alexina; then
			prolex_alexinadir=$datadir/prolex_alexina
		else
			if test -d $prefix/share/prolex_alexina; then
				prolex_alexinadir=$prefix/share/prolex_alexina
			else
				if test -d /usr/local/share/prolex_alexina; then
					prolex_alexinadir=/usr/local/share/prolex_alexina
				else
					if test -d /usr/share/prolex_alexina; then
						prolex_alexinadir=/usr/share/prolex_alexina
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for prolex_alexina)

	# check validity
	if test -d "$prolex_alexinadir"; then
		# expand to an absolute path
		prolex_alexinadir=`cd $prolex_alexinadir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	frPlexdir=$prolex_alexinadir
	AC_SUBST(prolex_alexinadir)
	AC_SUBST(frPlexdir)
])


# AC_PATH_KHALEX
# Test for KhaLex installation
# defines khalexdir
AC_DEFUN([AC_PATH_KHALEX], [
	AC_ARG_WITH(
		khalexdir,
		AC_HELP_STRING(
		       --with-khalexdir=DIR,
		       path where khalex is installed
		),
		khalexdir=,
		if test -d $datadir/khalex; then
			khalexdir=$datadir/khalex
		else
			if test -d $prefix/share/khalex; then
				khalexdir=$prefix/share/khalex
			else
				if test -d /usr/local/share/khalex; then
					khalexdir=/usr/local/share/khalex
				else
					if test -d /usr/share/khalex; then
						khalexdir=/usr/share/khalex
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for KhaLex)

	# check validity
	if test -d "$khalexdir"; then
		# expand to an absolute path
		khalexdir=`cd $khalexdir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	klrlexdir=$khalexdir
	AC_SUBST(khalexdir)
	AC_SUBST(klrlexdir)
])


# AC_PATH_MORPH_IT
# Test for Morph_it installation
# defines morph_itdir
AC_DEFUN([AC_PATH_MORPH_IT], [
	AC_ARG_WITH(
		morph_itdir,
		AC_HELP_STRING(
		       --with-morph_itdir=DIR,
		       path where morph_it is installed
		),
		morph_itdir=,
		if test -d $datadir/morph_it; then
			morph_itdir=$datadir/morph_it
		else
			if test -d $prefix/share/morph_it; then
				morph_itdir=$prefix/share/morph_it
			else
				if test -d /usr/local/share/morph_it; then
					morph_itdir=/usr/local/share/morph_it
				else
					if test -d /usr/share/morph_it; then
						morph_itdir=/usr/share/morph_it
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for Morph_it)

	# check validity
	if test -d "$morph_itdir"; then
		# expand to an absolute path
		morph_itdir=`cd $morph_itdir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	itlexdir=$morph_itdir
	AC_SUBST(morph_itdir)
	AC_SUBST(itlexdir)
])


# AC_PATH_DELEX
# Test for DeLex installation
# defines delexdir
AC_DEFUN([AC_PATH_DELEX], [
	AC_ARG_WITH(
		delexdir,
		AC_HELP_STRING(
		       --with-delexdir=DIR,
		       path where delex is installed
		),
		delexdir=,
		if test -d $datadir/delex; then
			delexdir=$datadir/delex
		else
			if test -d $prefix/share/delex; then
				delexdir=$prefix/share/delex
			else
				if test -d /usr/local/share/delex; then
					delexdir=/usr/local/share/delex
				else
					if test -d /usr/share/delex; then
						delexdir=/usr/share/delex
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for DeLex)

	# check validity
	if test -d "$delexdir"; then
		# expand to an absolute path
		delexdir=`cd $delexdir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	delexdir=$delexdir
	AC_SUBST(delexdir)
	AC_SUBST(delexdir)
])


# AC_PATH_KURLEX
# Test for KurLex installation
# defines kurlexdir
AC_DEFUN([AC_PATH_KURLEX], [
	AC_ARG_WITH(
		kurlexdir,
		AC_HELP_STRING(
		       --with-kurlexdir=DIR,
		       path where kurlex is installed
		),
		kurlexdir=,
		if test -d $datadir/kurlex; then
			kurlexdir=$datadir/kurlex
		else
			if test -d $prefix/share/kurlex; then
				kurlexdir=$prefix/share/kurlex
			else
				if test -d /usr/local/share/kurlex; then
					kurlexdir=/usr/local/share/kurlex
				else
					if test -d /usr/share/kurlex; then
						kurlexdir=/usr/share/kurlex
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for KurLex)

	# check validity
	if test -d "$kurlexdir"; then
		# expand to an absolute path
		kurlexdir=`cd $kurlexdir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	kulexdir=$kurlexdir
	AC_SUBST(kurlexdir)
	AC_SUBST(kulexdir)
])


# AC_PATH_VOCAPIALEX
# Test for vocapialex installation
# defines vocapialexdir
AC_DEFUN([AC_PATH_VOCAPIALEX], [
	AC_ARG_WITH(
		vocapialexdir,
		AC_HELP_STRING(
		       --with-vocapialexdir=DIR,
		       path where vocapialex is installed
		),
		vocapialexdir=,
		if test -d $datadir/vocapialex; then
			vocapialexdir=$datadir/vocapialex
		else
			if test -d $prefix/share/vocapialex; then
				vocapialexdir=$prefix/share/vocapialex
			else
				if test -d /usr/local/share/vocapialex; then
					vocapialexdir=/usr/local/share/vocapialex
				else
					if test -d /usr/share/vocapialex; then
						vocapialexdir=/usr/share/vocapialex
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for vocapialex)

	# check validity
	if test -d "$vocapialexdir"; then
		# expand to an absolute path
		vocapialexdir=`cd $vocapialexdir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	frVlexdir=$vocapialexdir
	AC_SUBST(vocapialexdir)
	AC_SUBST(frVlexdir)
])


# AC_PATH_POLLEX
# Test for PolLex installation
# defines pollexdir
AC_DEFUN([AC_PATH_POLLEX], [
	AC_ARG_WITH(
		pollexdir,
		AC_HELP_STRING(
		       --with-pollexdir=DIR,
		       path where pollex is installed
		),
		pollexdir=,
		if test -d $datadir/pollex; then
			pollexdir=$datadir/pollex
		else
			if test -d $prefix/share/pollex; then
				pollexdir=$prefix/share/pollex
			else
				if test -d /usr/local/share/pollex; then
					pollexdir=/usr/local/share/pollex
				else
					if test -d /usr/share/pollex; then
						pollexdir=/usr/share/pollex
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for PolLex)

	# check validity
	if test -d "$pollexdir"; then
		# expand to an absolute path
		pollexdir=`cd $pollexdir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	pllexdir=$pollexdir
	AC_SUBST(pollexdir)
	AC_SUBST(pllexdir)
])


# AC_PATH_MORPHALOU_ALEXINA
# Test for morphalou_alexina installation
# defines morphalou_alexinadir
AC_DEFUN([AC_PATH_MORPHALOU_ALEXINA], [
	AC_ARG_WITH(
		morphalou_alexinadir,
		AC_HELP_STRING(
		       --with-morphalou_alexinadir=DIR,
		       path where morphalou_alexina is installed
		),
		morphalou_alexinadir=,
		if test -d $datadir/morphalou_alexina; then
			morphalou_alexinadir=$datadir/morphalou_alexina
		else
			if test -d $prefix/share/morphalou_alexina; then
				morphalou_alexinadir=$prefix/share/morphalou_alexina
			else
				if test -d /usr/local/share/morphalou_alexina; then
					morphalou_alexinadir=/usr/local/share/morphalou_alexina
				else
					if test -d /usr/share/morphalou_alexina; then
						morphalou_alexinadir=/usr/share/morphalou_alexina
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for morphalou_alexina)

	# check validity
	if test -d "$morphalou_alexinadir"; then
		# expand to an absolute path
		morphalou_alexinadir=`cd $morphalou_alexinadir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	frMlexdir=$morphalou_alexinadir
	AC_SUBST(morphalou_alexinadir)
	AC_SUBST(frMlexdir)
])


# AC_PATH_SORALEX
# Test for SoraLex installation
# defines soralexdir
AC_DEFUN([AC_PATH_SORALEX], [
	AC_ARG_WITH(
		soralexdir,
		AC_HELP_STRING(
		       --with-soralexdir=DIR,
		       path where soralex is installed
		),
		soralexdir=,
		if test -d $datadir/soralex; then
			soralexdir=$datadir/soralex
		else
			if test -d $prefix/share/soralex; then
				soralexdir=$prefix/share/soralex
			else
				if test -d /usr/local/share/soralex; then
					soralexdir=/usr/local/share/soralex
				else
					if test -d /usr/share/soralex; then
						soralexdir=/usr/share/soralex
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for SoraLex)

	# check validity
	if test -d "$soralexdir"; then
		# expand to an absolute path
		soralexdir=`cd $soralexdir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	ckblexdir=$soralexdir
	AC_SUBST(soralexdir)
	AC_SUBST(ckblexdir)
])


# AC_PATH_ALPINO_LEX
# Test for Alpino_lex installation
# defines alpino_lexdir
AC_DEFUN([AC_PATH_ALPINO_LEX], [
	AC_ARG_WITH(
		alpino_lexdir,
		AC_HELP_STRING(
		       --with-alpino_lexdir=DIR,
		       path where alpino_lex is installed
		),
		alpino_lexdir=,
		if test -d $datadir/alpino_lex; then
			alpino_lexdir=$datadir/alpino_lex
		else
			if test -d $prefix/share/alpino_lex; then
				alpino_lexdir=$prefix/share/alpino_lex
			else
				if test -d /usr/local/share/alpino_lex; then
					alpino_lexdir=/usr/local/share/alpino_lex
				else
					if test -d /usr/share/alpino_lex; then
						alpino_lexdir=/usr/share/alpino_lex
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for Alpino_lex)

	# check validity
	if test -d "$alpino_lexdir"; then
		# expand to an absolute path
		alpino_lexdir=`cd $alpino_lexdir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	nllexdir=$alpino_lexdir
	AC_SUBST(alpino_lexdir)
	AC_SUBST(nllexdir)
])


# AC_PATH_LEFFP
# Test for Leffp installation
# defines leffpdir
AC_DEFUN([AC_PATH_LEFFP], [
	AC_ARG_WITH(
		leffpdir,
		AC_HELP_STRING(
		       --with-leffpdir=DIR,
		       path where leffp is installed
		),
		leffpdir=,
		if test -d $datadir/leffp; then
			leffpdir=$datadir/leffp
		else
			if test -d $prefix/share/leffp; then
				leffpdir=$prefix/share/leffp
			else
				if test -d /usr/local/share/leffp; then
					leffpdir=/usr/local/share/leffp
				else
					if test -d /usr/share/leffp; then
						leffpdir=/usr/share/leffp
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for Leffp)

	# check validity
	if test -d "$leffpdir"; then
		# expand to an absolute path
		leffpdir=`cd $leffpdir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	ptlexdir=$leffpdir
	AC_SUBST(leffpdir)
	AC_SUBST(ptlexdir)
])


# AC_PATH_ENLEX
# Test for EnLex installation
# defines enlexdir
AC_DEFUN([AC_PATH_ENLEX], [
	AC_ARG_WITH(
		enlexdir,
		AC_HELP_STRING(
		       --with-enlexdir=DIR,
		       path where enlex is installed
		),
		enlexdir=,
		if test -d $datadir/enlex; then
			enlexdir=$datadir/enlex
		else
			if test -d $prefix/share/enlex; then
				enlexdir=$prefix/share/enlex
			else
				if test -d /usr/local/share/enlex; then
					enlexdir=/usr/local/share/enlex
				else
					if test -d /usr/share/enlex; then
						enlexdir=/usr/share/enlex
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for EnLex)

	# check validity
	if test -d "$enlexdir"; then
		# expand to an absolute path
		enlexdir=`cd $enlexdir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	enlexdir=$enlexdir
	AC_SUBST(enlexdir)
	AC_SUBST(enlexdir)
])


# AC_PATH_LEFFE
# Test for Leffe installation
# defines leffedir
AC_DEFUN([AC_PATH_LEFFE], [
	AC_ARG_WITH(
		leffedir,
		AC_HELP_STRING(
		       --with-leffedir=DIR,
		       path where leffe is installed
		),
		leffedir=,
		if test -d $datadir/leffe; then
			leffedir=$datadir/leffe
		else
			if test -d $prefix/share/leffe; then
				leffedir=$prefix/share/leffe
			else
				if test -d /usr/local/share/leffe; then
					leffedir=/usr/local/share/leffe
				else
					if test -d /usr/share/leffe; then
						leffedir=/usr/share/leffe
					fi
				fi
			fi
		fi
	)

	AC_MSG_CHECKING(for Leffe)

	# check validity
	if test -d "$leffedir"; then
		# expand to an absolute path
		leffedir=`cd $leffedir && pwd`
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
	fi

	eslexdir=$leffedir
	AC_SUBST(leffedir)
	AC_SUBST(eslexdir)
])

