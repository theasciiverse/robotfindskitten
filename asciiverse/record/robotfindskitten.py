"""robotfindskitten preview: robot looks for kitten.

After the instructions, robot walks to the nearest thing on the field,
touches it, and lingers on what it turns out to be, then goes on to the
next nearest, until one of them is kitten: the meeting is played out and
the game ends by itself. Where kitten is hiding is up to the game, so a
search that ends in under 25 seconds or runs past 55 is recorded again,
up to ten times.

    python3 asciiverse/record/robotfindskitten.py
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rec

ROBOT = "#"
# robot's moves, as (dy, dx): the nethack keys the game takes
KEYS = {(-1, -1): "y", (-1, 0): "k", (-1, 1): "u", (0, -1): "h",
        (0, 1): "l", (1, -1): "b", (1, 0): "j", (1, 1): "n"}
SHORTEST, LONGEST = 25.0, 55.0


def field(r):
    """Robot's position and every thing on the field, inside the frame."""
    rows = r.rows()
    robot, things = None, set()
    for y in range(3, len(rows) - 1):
        for x in range(1, len(rows[y]) - 1):
            ch = rows[y][x]
            if ch == ROBOT:
                robot = (y, x)
            elif ch != " ":
                things.add((y, x))
    return robot, things


def over(r):
    """True once the game, and so the recording, has ended."""
    r.pump(0.0)
    return os.waitpid(r.pid, os.WNOHANG)[0] != 0


def sign(n):
    return (n > 0) - (n < 0)


def play():
    r = rec.Rec("robotfindskitten", "robotfindskitten", cwd=rec.ROOT)
    r.wait_for("Press any key to start")
    r.pump(3.0)
    r.key(" ", 1.0)
    touched = set()
    while not over(r):
        robot, things = field(r)
        if robot is None:
            break  # kitten found: the meeting is on screen
        left = things - touched
        if not left:
            break
        ty, tx = min(left, key=lambda t: max(abs(t[0] - robot[0]), abs(t[1] - robot[1])))
        # walk next to it, then into it: robot stays put and reads it
        while True:
            y, x = robot
            step = (sign(ty - y), sign(tx - x))
            r.key(KEYS[step], 0.09)
            if (y + step[0], x + step[1]) == (ty, tx):
                break
            robot, _ = field(r)
            if robot is None or robot == (y, x):
                break  # touched something on the way, or the game is over
        touched.add((ty, tx))
        # kitten's meeting takes a few seconds before the game ends
        for _ in range(24):
            if not r.pump(0.1):
                break
    r.finish(b"", grace=12.0)
    return r


def main():
    for attempt in range(10):
        r = play()
        length = r.elapsed()
        if SHORTEST <= length <= LONGEST:
            return
        print(f"attempt {attempt + 1}: {length:.0f} s, recording again", file=sys.stderr)
    sys.exit("no search of the right length in ten attempts")


main()
