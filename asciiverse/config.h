/*
 * config.h for the Asciiverse build (asciiverse/build.sh), in place of
 * the one upstream's configure writes: robotfindskitten is one C file,
 * so the build is one compiler call on every target. build.sh picks the
 * curses header with -DHAVE_NCURSES_H (ncurses) or -DHAVE_CURSES_H
 * (PDCurses on Windows).
 */
#define PACKAGE_VERSION "3.0000000.726"
#define HAVE_SIGNAL_H 1

/*
 * The non-kitten items are read from nki/ in the folder the game is
 * started in, which is where av installs them, and from
 * ~/.robotfindskitten. No system folder: one that held another copy of
 * vanilla.nki would load every item twice.
 */
#define SYSTEM_NKI_DIR ""

#ifdef _WIN32
/* MinGW has no random() and srandom() */
#define random() rand()
#define srandom(seed) srand(seed)
#endif
