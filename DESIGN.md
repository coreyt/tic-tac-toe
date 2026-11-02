# Tic-Tac-Toe Design

## Overview

The game is a terminal application implemented as one Python module. It uses a list of nine strings to represent the board and alternates between two players, `O` and `X`.

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
2. `main` calls `play_game`.
3. `play_game` creates an empty board and sets the current player to `O`.
4. The board is displayed and the current player is prompted for a position.
5. Invalid or occupied positions are rejected until a valid move is entered.
6. The move is recorded and checked for a win.
7. If there is no win, the player changes and the next turn begins.
8. After nine moves without a winner, the game reports a draw.
9. `main` asks whether to start another game. A new game resets the board and starts with `O`.

## Input handling

Input is read as text and stripped of surrounding whitespace. A move is accepted only when it is a number from 1 through 9 and its board position is empty. Replay accepts `y` or `yes` in any letter case; any other response exits the program.

## Module responsibilities

- `display_board(board)`: renders the current board.
- `has_won(board, player)`: checks all winning combinations.
- `play_game()`: manages one complete game.
- `main()`: manages the introduction and replay loop.

## Constraints

The design uses only the Python standard library and has no external runtime dependencies.
