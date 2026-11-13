> **Play it with Asciiverse.** With [av](https://asciiverse.sh), the Asciiverse
> client:
>
> ```
> av install blackjack-tui
> av play blackjack-tui
> ```
>
> The original README follows.

## Deal. Hit. Stand. Repeat.

This is a 1v1 blackjack game where you play against the dealer, with hole card and late surrender rules. It includes all the key mechanics of blackjack, minus splitting and insurance.

### Game Features

- Adjustable Settings:
  - Blackjack payout (3:2, 7:5, 6:5)
  - Soft 17 rule (dealer hits or stands on soft 17)
  - Number of decks (1-255), configurable in `strings.json` file
  - Penetration point, i.e. when to shuffle (0%, 25%, 50%, 75%)
- Betting Structure: Bet between 10-50 in increments of 10
- Starting Bankroll: Begin with 100
- Save/Load System: Continue your session where you left off
- Language Support: Customize most text through the `strings.json` file

## How to Play

### Option 1: Download Pre-built (Windows x86-64)
1. Go to the [Releases](../../releases) page
2. Download the latest `.zip` file
3. Extract the contents to a folder of your choice
4. Run the `.exe` file

### Option 2: Build from Source
1. Make sure you have [Go](https://golang.org/dl/) installed (version ≥ 1.25.0 at best)
2. Clone this repository:
   ```bash
   git clone https://github.com/MarcusBilo/blackjack-tui
   cd blackjack-tui
   ```
3. Build and run:
   ```bash
   go build
   .\blackjack-tui
   ```

## Game Controls
Once the game is running, simply use your keyboard to navigate through the menus and make your selections. 🍀

## Credits

@rivo [Unicode Handling](https://github.com/rivo/uniseg)

@charmbracelet [TUI framework](https://github.com/charmbracelet/bubbletea)

@dkorunic [Struct Field Alignment](https://github.com/dkorunic/betteralign)
