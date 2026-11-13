# Changes from upstream

This is the Asciiverse packaging of
[blackjack-tui](https://github.com/MarcusBilo/blackjack-tui) by MarcusBilo:
one-on-one blackjack against the dealer in the terminal (Go and Bubble
Tea), with a hole card and late surrender, a choice of payout (3:2, 7:5,
6:5), soft-17 rule, number of decks and shuffle point, and saved games.
Upstream is the `upstream` remote; the `asciiverse` branch carries the
changes below.

Built from upstream `main` at `c7ffa9d` (2026-08-11, a README update),
after its one release, v1.0.0 (2025-09-09, a Windows zip). The catalog
title is "Blackjack", the game's own title screen.

## Licence

BSD-3-Clause (LICENSE, "Copyright (c) 2026, MarcusBilo"). The Go modules
built into the binary are MIT or BSD-style: the Charm libraries,
rivo/uniseg, mattn's and muesli's terminal packages and others MIT;
golang.org/x BSD-3-Clause.

## Code

Each of these is its own commit, written to be offered upstream as a
pull request:

- **save.txt and debug.log in the state folder.** Saves were written
  beside the executable but read from the current folder, so a game saved
  after starting from another folder could not be loaded; debug.log was
  created wherever the game started. Both now live in
  `$XDG_STATE_HOME/blackjack-tui`, else `~/.local/state/blackjack-tui`
  (Linux), `~/Library/Application Support/blackjack-tui` (macOS) or
  `%LocalAppData%\blackjack-tui` (Windows), created on first use
  (`paths.go`). save.txt is written 0644 instead of 0777.
- **strings.json built in.** The text was read from strings.json in the
  current folder, so the game stopped with an error when started from
  anywhere else. It is built in with go:embed; a strings.json beside the
  program still takes its place, so the text can be edited or translated
  as before (`strings_embed.go`).
- **No language screen with one language.** strings.json ships English
  only, so the first screen offered a choice of one. With a single
  language the game goes straight to the start screen.
- **Session logging.** Every key is written to debug.log as it arrives,
  followed by the game state after it (phase, config step, cursor, money,
  bet, totals, cards dealt), the Asciiverse convention for diagnosing
  reports.

## Packaging

- `.github/workflows/release.yml`: on `v*-av.*` tags, static builds for
  Linux, macOS and Windows (x86-64 and ARM64), SHA256SUMS, and .deb, .rpm,
  .apk and Arch packages, attached to a GitHub release. Pure Go with CGO
  off, so every target cross-compiles on one Linux runner.
- `asciiverse/nfpm.yaml`: the system packages. No .desktop file: av is
  the one place titles are started from.
- `asciiverse/record-preview.py` and `asciiverse/blackjack-tui.cast`: the
  catalog preview at 100x30, a new game (3:2, dealer stands on soft 17,
  six decks, shuffle at 75%) played by basic strategy read off the screen,
  best of several takes.

Tags look like `v1.0.0+20260811-av.1`: upstream's last tag, the date of
the upstream commit built, then our packaging release.
