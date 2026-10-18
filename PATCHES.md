# Changes from upstream

This is the Asciiverse packaging of robotfindskitten, the zen simulation
by Leonard Richardson and contributors (1997), in its canonical C and
ncurses version from <https://codeberg.org/robotfindskitten/robotfindskitten>
(the `upstream` remote). It starts from upstream `main` at `6e1cf41`
(2026-08-27): the 3.0000000.726 release (`4718727`, tag `3.0000000.726`)
plus three commits that only touch upstream's CI and lint setup. That is
newer than the "latest" release on the old GitHub repository, which
upstream left for Codeberg.

## Code

None: the game is upstream's, unchanged. Everything below is new files.

## Packaging (new files)

- `asciiverse/build.sh`: robotfindskitten is one C file, so the build is
  one compiler call on every target, with `asciiverse/config.h` in place
  of the `config.h` upstream's autotools write (the version, the curses
  header, and `random()`/`srandom()` mapped to `rand()`/`srand()` for
  MinGW). No autotools are needed.
- Items: the game reads its non-kitten items from `nki/` in the folder it
  is started in (and from `~/.robotfindskitten`), so the archive holds
  `nki/vanilla.nki` (726 items) beside the binary, where av installs and
  starts it. The system folder upstream also reads
  (`$(datadir)/games/robotfindskitten`) is set to none, so a copy
  installed by a distribution is not loaded a second time. The game
  writes no files.
- `asciiverse/package.sh` packs `asciiverse/archive/robotfindskitten.txt`
  (the binary, `nki/vanilla.nki`, the man page, `COPYING`, `README.md`)
  into `dist/robotfindskitten-<target>.tar.gz`, `.zip` on Windows; the
  NetBSD games' script, which now also places a file in a folder
  (`src -> nki/vanilla.nki`).
- `.github/workflows/release.yml`: on a tag, static Linux in Alpine
  (x86_64, aarch64; checked locally for x86_64), macOS (x86_64, arm64,
  system ncurses; not run yet) and Windows x86_64, cross-built with MinGW
  against PDCurses 3.9's Windows console port and linked statically
  (only system DLLs; checked under Wine), plus SHA256SUMS. Upstream's
  Woodpecker CI (`.woodpecker/`) is left as it is; GitHub ignores it.
- `asciiverse/record/`: `rec.py` (from MyMan's and the NetBSD games') and
  `robotfindskitten.py`, which walks robot to the nearest things one by
  one until it finds kitten, for the preview
  `asciiverse/casts/robotfindskitten.cast` (100x30, 52 s).
- `.gitignore`: build output, and an exception so `asciiverse/config.h`
  is tracked.
