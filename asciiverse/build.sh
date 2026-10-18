#!/bin/sh
# Builds robotfindskitten into out/. It is one C file on curses, so one
# compiler call serves every target, with asciiverse/config.h in place of
# the config.h upstream's configure writes (see
# .github/workflows/release.yml):
#
#   asciiverse/build.sh                                        # Debian, Ubuntu
#   LIBS=-lncursesw LDFLAGS="-static -s" asciiverse/build.sh   # Alpine, static
#   CFLAGS="-O2 -arch arm64" LDFLAGS="-arch arm64" asciiverse/build.sh  # macOS
#   CC=x86_64-w64-mingw32-gcc CURSES=HAVE_CURSES_H CFLAGS="-O2 -I$PDC" \
#     LIBS="$PDC/wincon/pdcurses.a" LDFLAGS="-static -s" EXE=.exe \
#     asciiverse/build.sh                                      # Windows, PDCurses
set -eu
cd "$(dirname "$0")/.."
CC="${CC:-cc}"
CFLAGS="${CFLAGS:--O2}"
LDFLAGS="${LDFLAGS:-}"
LIBS="${LIBS:--lncurses}"
CURSES="${CURSES:-HAVE_NCURSES_H}"
EXE="${EXE:-}"
mkdir -p out
# shellcheck disable=SC2086
$CC $CFLAGS -D"$CURSES" -Iasciiverse src/robotfindskitten.c $LDFLAGS $LIBS \
  -o "out/robotfindskitten$EXE"
echo "built robotfindskitten$EXE"
