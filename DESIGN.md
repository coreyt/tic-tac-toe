# Tic-Tac-Toe Design

## Overview

The game is a terminal application implemented as one Python module. It uses a list of nine strings to represent the board and supports either two human players or one human player against a computer. In one-player mode, the human is `O` and the computer is `X`. The computer blocks immediate human winning threats and otherwise chooses randomly.

## Board representation

The board is stored as a nine-element list. List indexes 0 through 8 correspond to displayed positions 1 through 9:

```text
 0 | 1 | 2
---+---+---
 3 | 4 | 5
---+---+---
 6 | 7 | 8
```

An empty string represents an unoccupied square. The display function shows the corresponding position number for empty squares and the player's mark for occupied squares.

## Terminal layout

Render each cell with at least one space to either side of its number or mark and one blank line above and below it. Keep the board at a fixed terminal position throughout each game. Maintain an ordered in-memory journal of valid moves as player and position pairs, resetting it when a new game starts. Render the journal to the board's right with exactly five spaces between the board's right edge and the journal text. Place game prompts, including replay, below the board with two blank lines after its bottom edge.

Use terminal cursor positioning and redraw the same screen regions after moves and validation errors, rather than printing successive boards. Reserve a status area for errors so they do not displace the board. The fixed layout assumes a terminal large enough to display the board, journal, and prompts; cursor-control handling must also be considered for non-interactive output and tests.

## Winning logic

The `WINNING_LINES` constant contains the eight possible winning combinations:

- Three horizontal rows
- Three vertical columns
- Two diagonals

After every valid move, `has_won` checks whether all three indexes in any winning combination contain the current player's mark.

## Computer move selection

On each computer turn, inspect the winning combinations for a line containing two `O` marks and one empty square. If a line matches, select its empty square to block the human's immediate win. If more than one line matches, blocking any one of them satisfies the requirement. If no line matches, select randomly from all empty squares. A blocking move takes priority even if the computer has an immediate winning move of its own.

## Program flow

1. `main` prints the game introduction.
2. `main` asks whether to play in one-player or two-player mode.
3. In one-player mode, `main` identifies `O` as the human and `X` as the computer.
4. `play_game` creates an empty board and sets the current player to `O`.
5. The board is displayed. Human turns prompt for a position; the computer blocks an immediate threat if one exists, otherwise it chooses randomly from the empty positions.
6. Invalid or occupied human selections are rejected until a valid move is entered.
7. The move is recorded in the board and journal, the fixed layout is refreshed, and the move is checked for a win.
8. If there is no win, the player changes and the next turn begins.
9. After nine moves without a winner, the game reports a draw.
10. `main` asks whether to start another game. A new game asks for the mode again, resets the board, and starts with `O`.

## Input handling

Input is read as text and stripped of surrounding whitespace. A mode is accepted only when it is `1` or `2`. A human move is accepted only when it is a number from 1 through 9 and its board position is empty. When there is no immediate human winning threat, the computer selects uniformly from the currently empty positions using Python's random module. The replay prompt indicates yes is the default: an empty response, `y`, or `yes` starts another game; any other response exits the program.

## Module responsibilities

- Board rendering: displays the padded board, move journal, status, and prompts in fixed screen regions.
- `has_won(board, player)`: checks all winning combinations.
- `choose_mode()`: validates the one-player or two-player selection.
- `get_human_move(board, player)`: validates a human player's move.
- `get_computer_move(board)`: selects an empty square that blocks an immediate human win, or randomly selects an empty square if no threat exists.
- `play_game(mode)`: manages one complete game in the selected mode.
- `main()`: manages the introduction and replay loop.

## Constraints

The design uses only the Python standard library and has no external runtime dependencies.
