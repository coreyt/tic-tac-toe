# Tic-Tac-Toe Design

## Overview

The game is a terminal application implemented as one Python module. It uses a list of nine strings to represent the board and supports either two human players or one human player against a computer. The human or player 1 selects a mark for each game; the other participant receives the other mark. The computer follows the ordered rules in `spec-computer-strategy.txt`.

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

Render `X` in yellow and `O` in blue wherever marks are displayed on a color-capable terminal. Apply and reset color around each mark so numbers, borders, and other text retain their normal color. For redirected output or terminals without color support, render plain `X` and `O`. Color escape sequences do not count toward the visible widths used for board padding or journal positioning.

## Participant selection and session scores

After choosing the mode for each game, prompt the human or player 1 for `X` or `O`, accepting either case. Assign the other mark to the computer or player 2, respectively, and display both assignments. Select the next controller by the current mark: in one-player mode the computer plays whenever its assigned mark is current, including the opening turn when it is `O`.

Initialize an in-memory score record for `X` wins, `O` wins, and draws to zero once when the program starts. Each completed game returns a structured outcome (`X`, `O`, or draw); increment its corresponding count exactly once. Render all three totals after each game and throughout later games in the same session, without resetting them when the board, journal, mode, or marks change. Do not persist scores across program runs. Reserve a fixed area for the totals so they do not disturb the board, journal spacing, or prompt position.

## Winning logic

The `WINNING_LINES` constant contains the eight possible winning combinations:

- Three horizontal rows
- Three vertical columns
- Two diagonals

After every valid move, `has_won` checks whether all three indexes in any winning combination contain the current player's mark.

## Leaderboard

Store up to five entries as initials and win count in `leaderboard.csv`, ordered by descending score. Read and write the file with ordinary file operations and manually handled comma-separated fields; start with an empty leaderboard if the file does not exist. Keep human-player session win counts separately from mark-based session scores so that changing marks does not transfer a player's wins. Player 1 and player 2 identify the human participants in two-player mode; the single human is player 1 in one-player mode. A computer win or draw does not increase a human player's count.

After a human win, check that player's cumulative session wins against the saved entries: a free slot qualifies, or a full board qualifies only if the score strictly exceeds an existing entry. Ask for initials when qualifying, insert the score, retain the top five, and save. Display the leaderboard on startup and exit, and allow `l` or `L` at a human move prompt to display it and return to the unchanged turn. Preserve the fixed board layout when returning from the leaderboard.

## Computer move selection

On each computer turn, first select index 4 if the center is empty, even if the human has an immediate winning threat. Otherwise, inspect `WINNING_LINES` in its existing order for a line containing two marks belonging to the human and one empty square; select the empty square of the first matching line. Blocking takes priority over the computer's own winning moves. If no line matches, select uniformly at random from all empty squares. The full ordered behavior and test descriptions are in `spec-computer-strategy.txt`.

The `computer_strategy` function applies the center and blocking rules in that order and returns a board index, or `None` when neither applies. `get_computer_move` calls it and uses uniform random selection from empty positions only when it returns `None`.

## Program flow

1. `main` prints the game introduction.
2. `main` asks whether to play in one-player or two-player mode; invalid choices produce an explanatory error and the prompt repeats until `1` or `2` is entered.
3. Prompt the human or player 1 for a mark, assign the other mark to the other participant, and identify both assignments.
4. `play_game` creates an empty board and sets the current player to `O`.
5. The board is displayed. Human turns prompt for a position; the computer applies the center, block, and random rules in that order.
6. Invalid or occupied human selections are rejected until a valid move is entered.
7. The move is recorded in the board and journal, the fixed layout is refreshed, and the move is checked for a win.
8. If a player wins, record that mark as the outcome, display the final board and identify the winner. Otherwise, if the game continues, alternate from `O` to `X` or from `X` to `O`.
9. After nine moves without a winner, record and report a draw. Update and display the session totals exactly once per completed game.
10. `main` asks whether to start another game. A new game asks for the mode again, resets the board, and starts with `O`. If the player declines, display a brief closing message and exit.

## Input handling

Input is read as text and stripped of surrounding whitespace. A mode is accepted only when it is `1` or `2`. A human move is accepted only when it is a number from 1 through 9 and its board position is empty. When the center is occupied and there is no immediate human winning threat, the computer selects uniformly from the currently empty positions using Python's random module. The replay prompt indicates yes is the default: an empty response, `y`, or `yes` starts another game; any other response exits the program.

Mode, mark, and move prompts state the permitted choices; move prompts identify the current player. Normalize the chosen mark to uppercase and accept only `X` or `O`. Invalid entries produce an error that identifies the problem and explains the valid choices, followed by another prompt. In two-player mode, both marks use human move input; in one-player mode, the assigned human mark uses human input and the assigned computer mark moves automatically.

## Module responsibilities

- Board rendering: displays the padded and colorized board, move journal, session scores, status, and prompts in fixed screen regions.
- `has_won(board, player)`: checks all winning combinations.
- `choose_mode()`: validates the one-player or two-player selection.
- Mark selection: validates and assigns the two marks for each game.
- `get_human_move(board, player)`: validates a human player's move.
- Computer move selection: takes the empty center first, then uses the human's assigned mark to find a blocking square, or randomly selects an empty square if neither rule applies.
- Game control: manages one complete game with the chosen mode and assignments, and returns a structured result.
- `main()`: manages session scores, the introduction, and replay loop.

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
| Functional 6 | Participant selection and session scores; Input handling: assign the chosen mark to the human and the other to the computer. |
| Functional 7 | Program flow, step 3: identify the computer's mark. |
| Functional 8 | Overview; Board representation: use `O` and `X` marks. |
| Functional 9 | Program flow, step 4: initialize the current player to `O`. |
| Functional 10 | Program flow, step 5; Input handling: prompt the current human for an available position. |
| Functional 11 | Computer move selection; Input handling: select the computer move automatically from empty squares. |
| Functional 12 | Computer move selection; `spec-computer-strategy.txt`: center, then block, then random, with defined tie-breaking and test descriptions. |
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
| Functional 28 | Participant selection and session scores; Input handling: prompt, validate, assign, and identify marks for each mode. |
| Functional 29 | Participant selection and session scores; Program flow: maintain and display session totals, updating once per result. |
| Functional 30 | Terminal layout: color marks on supported terminals and use plain text otherwise. |
| Functional 31 | Leaderboard: maintain up to five entries ordered by human win count. |
| Functional 32 | Leaderboard: track human session wins and accept initials for qualifying scores. |
| Functional 33 | Leaderboard: display on startup, exit, and on `l`/`L` during a move. |
| Functional 34 | Leaderboard: load and save `leaderboard.csv` using manual file handling. |
| Non-functional 1 | Constraints: use the standard library only. |
| Non-functional 2 | Overview; Constraints: Python terminal application without external runtime dependencies; entry point is `tic_tac_toe.py`. |
| Non-functional 3 | Module responsibilities: separate named functions by responsibility. |
| Non-functional 4 | Input handling: identify valid choices, the current player, and corrective action for errors. |
