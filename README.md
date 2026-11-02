# Tic-Tac-Toe

Play tic-tac-toe in your terminal against another person or the computer. The game uses Python's standard library, so no additional packages are required.

## Start the game

From the project directory, run:

```sh
python tic_tac_toe.py
```

If your system uses `python3` for Python 3, run `python3 tic_tac_toe.py` instead.

## How to play

1. Enter `1` to play against the computer, or `2` for two human players.
2. `O` always plays first. In one-player mode, you are `O` and the computer is `X`.
3. On your turn, enter the number of an empty square. The board stays in place in a sufficiently large terminal, and the move journal appears to its right:

   ```text
    1 | 2 | 3
   ---+---+---
    4 | 5 | 6
   ---+---+---
    7 | 8 | 9
   ```

4. Take turns until a player gets three marks in a row, column, or diagonal. That player wins. If the board fills without a winner, the game is a draw.
5. After the game, press Enter or enter `y` or `yes` to play again; any other response exits. You can choose the player mode again for the next game.

The computer blocks an immediate winning line when you have two marks in a row with the third square empty. Otherwise, it selects an empty square randomly.

## Run the tests

```sh
python -m unittest discover -v
```
