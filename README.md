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
2. Choose `X` or `O` for yourself (player 1 in two-player mode). The computer or player 2 receives the other mark. `O` always plays first.
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

The computer takes the center if it is empty. Otherwise, it blocks an immediate opposing winning line if possible, or selects an empty square randomly. The move journal shows the reason for each computer move.

The game keeps `X` wins, `O` wins, and draws for the current session and displays the totals as you play. The totals reset when you exit and start the program again. On supported terminals, `X` appears in yellow and `O` in blue.

The leaderboard keeps up to five qualifying human scores in `leaderboard.csv` in the directory where you run the game. When your win total qualifies, enter your initials; commas and quotation marks are supported. Enter `L` at a move prompt to view the leaderboard and press Enter to return to the game.

## Run the tests

```sh
python -m unittest discover -v
```
