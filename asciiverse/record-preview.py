#!/usr/bin/env python3
"""Records asciiverse/blackjack-tui.cast, the catalog preview, at 100x30
(hub/RECORDING.md). It starts a new game (3:2 payout, dealer stands on
soft 17, six decks, shuffle at 75%), then plays hands by basic strategy
read off the screen: hit below 12, hit 12 to 16 against a dealer 7 or
higher, double on 10 and 11 against a weaker dealer card, else stand. Bets
go up and down between 10 and 30. After about PLAY seconds it quits with
Ctrl+C.

The shoe is shuffled from the clock, so every take differs; pick the best.
blackjack-tui runs by name from the folder given (default stage/), in an
empty HOME, so the cast holds no local path and no saves of your own.

Needs asciinema 3.x and pyte. Usage, from the repo root:
  uv run --with pyte python3 asciiverse/record-preview.py [bindir]
With --dry-run it plays without recording."""
import fcntl, os, pty, random, re, select, struct, sys, tempfile, termios, time
import pyte

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if a != "--dry-run"]
dry = "--dry-run" in sys.argv
bindir = os.path.abspath(args[0]) if args else f"{root}/stage"
cast = f"{root}/asciiverse/blackjack-tui.cast"
COLS, ROWS, PLAY = 100, 30, float(os.environ.get("PLAY", "40"))
KEYS = {"up": b"\x1b[A", "down": b"\x1b[B", "enter": b"\r"}

home = tempfile.mkdtemp()
env = dict(os.environ, TERM="xterm-256color", COLORTERM="truecolor", LANG="C.UTF-8",
           HOME=home, USER="player", LOGNAME="player", XDG_STATE_HOME=f"{home}/.local/state",
           PATH=f"{bindir}:{os.environ['PATH']}")
for v in ("VTE_VERSION", "TERM_PROGRAM", "TERM_PROGRAM_VERSION", "TMUX", "COLORFGBG"):
    env.pop(v, None)

pid, fd = pty.fork()
if pid == 0:
    os.chdir(home)
    if dry:
        os.execvpe("blackjack-tui", ["blackjack-tui"], env)
    os.execvpe("asciinema", ["asciinema", "rec", "--overwrite", "-q", "--idle-time-limit", "2",
        "--window-size", f"{COLS}x{ROWS}", "--capture-env", "TERM,COLORTERM,LANG",
        "--title", "Blackjack", "--command", "blackjack-tui", cast], env)
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", ROWS, COLS, 0, 0))
screen = pyte.Screen(COLS, ROWS)
stream = pyte.ByteStream(screen)


def pump(seconds):
    end = time.time() + seconds
    while True:
        left = end - time.time()
        r, _, _ = select.select([fd], [], [], max(0.0, min(0.02, left)))
        if r:
            try:
                data = os.read(fd, 65536)
            except OSError:
                return False
            # Bubble Tea asks the terminal for its background colour and the
            # cursor position at start; answer as a dark terminal would.
            if b"\x1b]11;?" in data:
                os.write(fd, b"\x1b]11;rgb:0000/0000/0000\x1b\\")
            if b"\x1b[6n" in data:
                os.write(fd, b"\x1b[1;1R")
            stream.feed(data)
        if left <= 0:
            return True


def key(k, wait=0.3):
    os.write(fd, KEYS[k])
    pump(wait)


def text():
    return "\n".join(screen.display)


def options():
    """The menu lines under the prompt, in order."""
    return [l[2:].strip() for l in screen.display if l.startswith(("→ ", "  ")) and l.strip()]


def choose(label, wait=0.9):
    """Move the cursor from the top to the option named and press Enter."""
    opts = options()
    i = next((n for n, o in enumerate(opts) if o == label), 0)
    for _ in range(i):
        key("down", 0.18)
    pump(0.25)
    key("enter", wait)


def cards(label):
    for l in screen.display:
        if l.startswith(label):
            return re.findall(r"(10|[2-9JQKA?])[♥♦♣♠?]", l[len(label):])
    return []


def total(hand):
    t, aces = 0, 0
    for c in hand:
        if c == "A":
            t, aces = t + 11, aces + 1
        elif c in "JQK" or c == "10":
            t += 10
        elif c.isdigit():
            t += int(c)
    while t > 21 and aces:
        t, aces = t - 10, aces - 1
    return t


pump(2.0)
for label in ("Start new Game", "3:2", "Dealer stands on soft 17", "6 Decks", "75 %", "Start new Game"):
    choose(label, 0.7)

start = time.time()
stuck = 0
while time.time() - start < PLAY:
    t = text()
    stuck += 1
    if "Select Amount to Bet" in t:
        choose(random.choice(["10", "10", "20", "20", "30"]), 1.0)
        stuck = 0
    elif "→ Hit" in t or "  Hit" in t:
        me, up = cards("Player Cards:"), cards("Dealer Cards:")
        p = total(me)
        d = total(up[:1]) if up else 10
        pump(0.6)
        if len(me) == 2 and p in (10, 11) and d < 10 and "Double" in options():
            choose("Double", 1.6)
        elif p < 12 or (p < 17 and d >= 7):
            choose("Hit", 1.0)
        else:
            choose("Stand", 1.6)
        stuck = 0
    elif "Restart / Bet" in t:
        pump(1.4)
        choose("Restart / Bet", 0.8)
        stuck = 0
    else:
        pump(0.3)
    if stuck > 40 or "GAME OVER" in t:
        break

pump(1.5)
os.write(fd, b"\x03")
for _ in range(50):
    if os.waitpid(pid, os.WNOHANG)[0]:
        break
    pump(0.2)
