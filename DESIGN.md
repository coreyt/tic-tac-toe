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
2. `main` asks whether to play in one-player or two-player mode; invalid choices produce an explanatory error and the prompt repeats until `1` or `2` is entered.
3. In one-player mode, `main` identifies `O` as the human and `X` as the computer.
4. `play_game` creates an empty board and sets the current player to `O`.
5. The board is displayed. Human turns prompt for a position; the computer blocks an immediate threat if one exists, otherwise it chooses randomly from the empty positions.
6. Invalid or occupied human selections are rejected until a valid move is entered.
7. The move is recorded in the board and journal, the fixed layout is refreshed, and the move is checked for a win.
8. If a player wins, display the final board and identify that player. Otherwise, if the game continues, alternate from `O` to `X` or from `X` to `O`.
9. After nine moves without a winner, the game reports a draw.
10. `main` asks whether to start another game. A new game asks for the mode again, resets the board, and starts with `O`. If the player declines, display a brief closing message and exit.

## Input handling

Input is read as text and stripped of surrounding whitespace. A mode is accepted only when it is `1` or `2`. A human move is accepted only when it is a number from 1 through 9 and its board position is empty. When there is no immediate human winning threat, the computer selects uniformly from the currently empty positions using Python's random module. The replay prompt indicates yes is the default: an empty response, `y`, or `yes` starts another game; any other response exits the program.

Mode and move prompts state the permitted choices; move prompts identify the current player. Invalid entries produce an error that identifies the problem and explains the valid choices, followed by another prompt. In two-player mode, both marks use human move input; in one-player mode, only `O` uses human input and `X` moves automatically.

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

## Requirement-to-design mapping

Requirement numbers refer to the functional and non-functional lists in `REQUIREMENTS.md`.

| Requirement | Design coverage |
| --- | --- |
| Functional 1 | Overview; Constraints: Python terminal application using the standard library. |
| Functional 2 | Board representation: nine positions shown as a 3-by-3 grid. |
| Functional 3 | Program flow, step 2: choose mode at the start of each game. |
| Functional 4 | Program flow, step 2; Input handling: accept `1` or `2`, explain errors and re-prompt. |
| Functional 5 | Input handling: both marks use human input in two-player mode. |
| Functional 6 | Overview; Input handling: human `O` and computer `X`. |
| Functional 7 | Program flow, step 3: identify the computer's mark. |
| Functional 8 | Overview; Board representation: use `O` and `X` marks. |
| Functional 9 | Program flow, step 4: initialize the current player to `O`. |
| Functional 10 | Program flow, step 5; Input handling: prompt the current human for an available position. |
| Functional 11 | Computer move selection; Input handling: select the computer move automatically from empty squares. |
| Functional 12 | Computer move selection: block a threat, or choose randomly if none exists. |
| Functional 13 | Computer move selection: select only an empty square. |
| Functional 14 | Input handling: validate the numeric range and re-prompt with an error. |
| Functional 15 | Input handling: reject occupied squares and re-prompt with an error. |
| Functional 16 | Program flow, step 8: alternate marks while the game continues. |
| Functional 17 | Winning logic: check rows, columns, and diagonals after valid moves. |
| Functional 18 | Program flow, step 8: display the final board and winning player. |
| Functional 19 | Program flow, step 9: report a draw after nine moves without a winner. |
| Functional 20 | Program flow, step 10: ask to start another game. |
| Functional 21 | Program flow, step 10; Terminal layout: select mode again, reset board and journal, and start with `O`. |
| Functional 22 | Program flow, step 10: display a closing message and exit on decline. |
| Functional 23 | Terminal layout: pad each cell horizontally and vertically. |
| Functional 24 | Input handling: indicate yes as the default and accept an empty response. |
| Functional 25 | Terminal layout: redraw fixed regions and reserve error space in a sufficiently large terminal. |
| Functional 26 | Terminal layout: render the ordered, per-game move journal five spaces right of the board. |
| Functional 27 | Terminal layout: place game and replay prompts two blank lines below the board. |
| Non-functional 1 | Constraints: use the standard library only. |
| Non-functional 2 | Overview; Constraints: Python terminal application without external runtime dependencies; entry point is `tic_tac_toe.py`. |
| Non-functional 3 | Module responsibilities: separate named functions by responsibility. |
| Non-functional 4 | Input handling: identify valid choices, the current player, and corrective action for errors. |
