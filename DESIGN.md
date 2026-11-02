# Tic-Tac-Toe Design

## Overview

The game is a terminal application implemented as one Python module. It uses a list of nine strings to represent the board and supports either two human players or one human player against a computer. In one-player mode, the human is `O`, the computer is `X`, and the computer chooses moves randomly.

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

## Winning logic

The `WINNING_LINES` constant contains the eight possible winning combinations:

- Three horizontal rows
- Three vertical columns
- Two diagonals

After every valid move, `has_won` checks whether all three indexes in any winning combination contain the current player's mark.

## Program flow

1. `main` prints the game introduction.
2. `main` asks whether to play in one-player or two-player mode.
3. In one-player mode, `main` identifies `O` as the human and `X` as the computer.
4. `play_game` creates an empty board and sets the current player to `O`.
5. The board is displayed. Human turns prompt for a position; the computer chooses randomly from the empty positions.
6. Invalid or occupied human selections are rejected until a valid move is entered.
7. The move is recorded and checked for a win.
8. If there is no win, the player changes and the next turn begins.
9. After nine moves without a winner, the game reports a draw.
10. `main` asks whether to start another game. A new game asks for the mode again, resets the board, and starts with `O`.

## Input handling

Input is read as text and stripped of surrounding whitespace. A mode is accepted only when it is `1` or `2`. A human move is accepted only when it is a number from 1 through 9 and its board position is empty. In one-player mode, the computer selects uniformly from the currently empty positions using Python's random module; it does not evaluate or optimize its move. Replay accepts `y` or `yes` in any letter case; any other response exits the program.

## Module responsibilities

- `display_board(board)`: renders the current board.
- `has_won(board, player)`: checks all winning combinations.
- `choose_mode()`: validates the one-player or two-player selection.
- `get_human_move(board, player)`: validates a human player's move.
- `get_computer_move(board)`: randomly selects an empty position.
- `play_game(mode)`: manages one complete game in the selected mode.
- `main()`: manages the introduction and replay loop.

## Constraints

The design uses only the Python standard library and has no external runtime dependencies.
