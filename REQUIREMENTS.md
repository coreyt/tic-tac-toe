# Tic-Tac-Toe Requirements

## 1. Purpose

Create a basic text-based tic-tac-toe game supporting either two human players or one human player against the computer.

## 2. Functional requirements

1. The game must run in a terminal using Python.
2. The game must display a 3-by-3 board with positions numbered 1 through 9.
3. At the start of each game session, the game must ask whether to play with one player or two players.
4. The game must accept only `1` or `2` as valid player-mode selections and re-prompt for invalid selections.
5. In two-player mode, both `O` and `X` must be controlled by human players.
6. In one-player mode, the human player must control `O` and the computer must control `X`.
7. The game must clearly identify which mark is controlled by the computer.
8. Players must use the marks `O` and `X`.
9. Player `O` must always take the first turn.
10. On each human turn, the game must ask the current player to select an available position from 1 through 9.
11. On each computer turn, the game must select an unoccupied position automatically.
12. If the human has two marks in a row, column, or diagonal with the third position empty, the computer must play in that empty position to block the immediate winning threat. If multiple threats exist, it must block one of them. If no such threat exists, the computer must choose randomly from the currently unoccupied positions.
13. The computer must never select an occupied position.
14. The game must reject non-numeric input and numbers outside the range 1 through 9.
15. The game must reject positions that have already been selected.
16. The game must alternate turns between `O` and `X` after each valid move.
17. The game must detect a win when a player occupies three positions in a row, column, or diagonal.
18. When a player wins, the game must display the final board and identify the winning player.
19. If all nine positions are filled without a winner, the game must identify the result as a draw.
20. After each game, the game must ask whether the players want to play again.
21. If the players choose to play again, the game must ask for the player mode again, reset the board, and have `O` start the new game.
22. If the players decline to play again, the game must exit with a brief closing message.

## 3. Non-functional requirements

1. The game must use only the Python standard library.
2. The game must be runnable with `python tic_tac_toe.py`.
3. The source code should be organized into small, readable functions.
4. The game should provide clear prompts and error messages for players.

## 4. Acceptance criteria

The implementation is acceptable when all of the following scenarios pass:

1. **Start and mode selection**
   - Given the program has started, when it displays the mode prompt, then it offers one-player and two-player modes.
   - Given an invalid mode is entered, when the entry is submitted, then the game displays an error and asks again.
   - Given a valid mode is selected, when the game begins, then the board is empty and `O` is announced as the first player.

2. **Two-player mode**
   - Given two-player mode is selected, when a turn begins, then both `O` and `X` are prompted for human moves.
   - Given a valid move is entered, when the move is accepted, then the selected square displays that player’s mark and the turn changes.

3. **One-player mode**
   - Given one-player mode is selected, when the game begins, then the human is identified as `O` and the computer as `X`.
   - Given it is the computer’s turn, when the computer moves, then it selects one of the currently empty squares automatically.
   - Given the human has two marks in a row, column, or diagonal and the third square is empty, when the computer moves, then it occupies that empty square.
   - Given the human has multiple such threats, when the computer moves, then it blocks one of them.
   - Given the human has no such threat, when the computer moves, then it chooses randomly from the empty squares.

4. **Move validation**
   - Given a human is prompted for a move, when non-numeric input or a number outside 1 through 9 is entered, then the game displays an error and asks again.
   - Given a human is prompted for a move, when an occupied square is entered, then the game displays an error and asks again.

5. **Game results**
   - Given a player completes a row, column, or diagonal, when the move is made, then the game displays the final board and identifies that player as the winner.
   - Given all nine squares are occupied without a winning line, when the final move is made, then the game identifies the result as a draw.

6. **Replay and exit**
   - Given a game has ended, when the player chooses to play again, then the game asks for the mode again, clears the board, and starts with `O`.
   - Given a game has ended, when the player declines to play again, then the game displays a closing message and exits.
