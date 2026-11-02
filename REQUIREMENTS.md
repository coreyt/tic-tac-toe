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
12. The computer must never select an occupied position.
13. The game must reject non-numeric input and numbers outside the range 1 through 9.
14. The game must reject positions that have already been selected.
15. The game must alternate turns between `O` and `X` after each valid move.
16. The game must detect a win when a player occupies three positions in a row, column, or diagonal.
17. When a player wins, the game must display the final board and identify the winning player.
18. If all nine positions are filled without a winner, the game must identify the result as a draw.
19. After each game, the game must ask whether the players want to play again.
20. If the players choose to play again, the game must ask for the player mode again, reset the board, and have `O` start the new game.
21. If the players decline to play again, the game must exit with a brief closing message.

## 3. Non-functional requirements

1. The game must use only the Python standard library.
2. The game must be runnable with `python tic_tac_toe.py`.
3. The source code should be organized into small, readable functions.
4. The game should provide clear prompts and error messages for players.
