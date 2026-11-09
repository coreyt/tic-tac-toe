# Tic-Tac-Toe Requirements

## 1. Purpose

Create a basic text-based tic-tac-toe game supporting two human players, one human against the computer, or two computers.

## 2. Functional requirements

1. The game must run in a terminal using Python.
2. The game must display a 3-by-3 board with positions numbered 1 through 9.
3. At the start of each game session, the game must ask whether to play with one player or two players.
4. The game must accept `0`, `1`, or `2` as valid player-mode selections and re-prompt for invalid selections; the prompt must display only the `1`- and `2`-player options.
5. In two-player mode, both `O` and `X` must be controlled by human players.
6. In one-player mode, the human player must choose `X` or `O`; the computer must control the other mark.
7. The game must clearly identify which mark is controlled by the computer.
8. Players must use the marks `O` and `X`.
9. Player `O` must always take the first turn.
10. On each human turn, the game must ask the current player to select an available position from 1 through 9.
11. On each computer turn, the game must select an unoccupied position automatically.
12. The computer must select moves according to `spec-computer-strategy.txt`: first take the center if empty, otherwise block the first immediate opponent threat, otherwise choose randomly from empty positions.
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
23. Each displayed board cell must have at least one blank character of padding on the left and right and one blank line of padding above and below its number or mark, within the cell boundaries.
24. The replay prompt must indicate that yes is the default; pressing Enter without a response must start another game.
25. During a game, the board must remain at a fixed position in the terminal as moves are made and prompts or errors are displayed, provided the terminal is large enough to show the layout.
26. A move journal must appear to the right of the board, separated from its right edge by five spaces. It must list valid moves in order, identifying the player and selected position, and reset for each new game.
27. Prompts displayed during a game, including the replay prompt, must appear below the board with two blank lines between the board's bottom edge and the prompt.
28. At the start of each game, the human player in one-player mode, or player 1 in two-player mode, must choose `X` or `O`. In two-player mode, player 2 receives the other mark. The game must accept either letter case, reject other choices, re-prompt, and identify each participant's mark.
29. The game must keep in-memory counts of `X` wins, `O` wins, and draws for the current program session. It must display all three counts after each completed game and during subsequent games when players play again. Each completed game increments exactly one count; starting a new game does not reset the counts. Exiting and restarting the program resets all counts to zero.
30. On a color-capable terminal, displayed `X` marks must be yellow and displayed `O` marks must be blue. Empty-square numbers and other text must not inherit the mark colors. When color is unavailable, the marks must remain distinguishable as text.
31. The game must maintain a leaderboard of up to five human-player entries ranked by number of wins against a human or computer opponent.
32. When a human player's current-session win total exceeds a leaderboard entry, or an empty slot is available, the player must be offered the opportunity to enter initials and have the qualifying score recorded. A score tied with a full leaderboard entry does not displace it.
33. The leaderboard must be displayed at program startup, when the player declines to play again, and when a player enters `l` or `L` at a move prompt during a game; viewing it during a game must return to the same turn without making a move.
34. The leaderboard must persist in `leaderboard.csv` and be loaded on later program runs. The program must implement CSV reading and writing manually without a CSV library, preserving initials containing commas or quotation marks.
35. Each computer move must be accompanied by its selection reason (`center`, `block`, or `random`), and the move journal must display that reason alongside the computer's mark and position. Human moves must remain identifiable without a computer-selection reason.
36. **Computer can play computer:** The game must support a computer-versus-computer mode.
   - 36a. Entering `0` at the player-mode prompt selects this mode, but `0` must not appear as an option in that prompt.
   - 36b. The computer must control both `O` and `X`, with `O` first. Each side must use the existing computer strategy against the opposing mark; no human mark-selection or move prompt is needed.
   - 36c. The game must display the board, moves, result, and replay prompt. The result must update the session totals exactly once, but must not add an entry to the human leaderboard or prompt for initials.

## 3. Non-functional requirements

1. The game must use only the Python standard library.
2. The game must be runnable with `python tic_tac_toe.py`.
3. The source code should be organized into small, readable functions.
4. The game should provide clear prompts and error messages for players.

## 4. Acceptance criteria

The implementation is acceptable when all of the following scenarios pass:

1. **Start and mode selection**
   - Given Python is installed, when `python tic_tac_toe.py` is run in a terminal, then the game starts without installing third-party packages.
   - Given a new game, when the board is displayed, then it has three rows and three columns showing positions 1 through 9 for empty squares.
   - Given any board position, when the board is displayed, then its number or mark has at least one blank character on each side and one blank line above and below it within the cell boundaries.
   - Given a terminal large enough for the layout, when a player makes a move or a prompt or error is displayed, then the board remains at the same terminal position.
   - Given a game in progress, when the board is displayed, then the move journal begins five spaces to the right of the board's right edge and lists each valid move in order with its player and position; invalid moves do not appear.
   - Given a new game after replay, when the journal is displayed, then it contains no moves from the previous game.
   - Given a game prompt, including the replay prompt, when it is displayed, then two blank lines separate it from the bottom edge of the board.
   - Given the program has started, when it displays the mode prompt, then it offers one-player and two-player modes.
   - Given a mode is entered, when it is `0`, `1`, or `2`, then the game accepts it; for any other entry, it displays an error and asks again. The prompt displays only `1` and `2` as options.
   - Given a valid mode is selected, when the game begins, then the board is empty and `O` is announced as the first player.

2. **Two-player mode**
   - Given two-player mode is selected, when a turn begins, then both `O` and `X` are prompted for human moves.
   - Given two-player mode, when player 1 selects `X` or `O`, then player 1 receives that mark, player 2 receives the other, and both assignments are identified.
   - Given a valid move is entered, when the move is accepted, then the selected square displays that player’s mark and the turn changes.
   - Given any player mode, when a valid move is made and the game has not ended, then the next turn belongs to the other mark, alternating between `O` and `X`.

3. **One-player mode**
   - Given one-player mode, when the human selects `X` or `O`, then the human receives that mark, the computer receives the other, and both assignments are identified.
   - Given either choice of human mark, when the game begins, then `O` moves first, including automatically when the computer is `O`.
   - Given it is the computer’s turn, when the computer moves, then it selects one of the currently empty squares automatically.
   - Given the center is empty, when the computer moves, then it selects the center, even if the human has an immediate winning threat.
   - Given the center is occupied and the human has two marks in a row, column, or diagonal with the third square empty, when the computer moves, then it occupies that empty square.
   - Given the center is occupied and the human has multiple such threats, when the computer moves, then it blocks the first matching line in the order specified in `spec-computer-strategy.txt`.
   - Given the center is occupied and the human has no such threat, when the computer moves, then it chooses uniformly at random from the empty squares.

4. **Move validation**
   - Given a human is prompted for a move, when non-numeric input or a number outside 1 through 9 is entered, then the game displays an error and asks again.
   - Given a human is prompted for a move, when an occupied square is entered, then the game displays an error and asks again.

5. **Game results**
   - Given a player completes a row, column, or diagonal, when the move is made, then the game displays the final board and identifies that player as the winner.
   - Given all nine squares are occupied without a winning line, when the final move is made, then the game identifies the result as a draw.

6. **Replay and exit**
   - Given a game has ended, when the player chooses to play again, then the game asks for the mode again, clears the board, and starts with `O`.
   - Given a game has ended, when the replay prompt is displayed, then it indicates yes is the default; pressing Enter starts another game.
   - Given a game has ended, when the player declines to play again, then the game displays a closing message and exits.
   - Given one-player or two-player mode, when a mark is selected using lowercase or uppercase `x` or `o`, then it is accepted; any other entry displays an error and repeats the selection prompt.
   - Given completed games with wins for `X`, wins for `O`, and draws, when each game ends and a new game begins, then all three displayed totals reflect exactly those results and are retained across mode or mark changes.
   - Given a newly started program, when the session totals are displayed, then `X` wins, `O` wins, and draws each start at zero, regardless of a previous session.

7. **Mark colors**
   - Given a color-capable terminal, when occupied squares are displayed, then every `X` is yellow and every `O` is blue, without coloring empty-square numbers or unrelated text.
   - Given output without color support, when marks are displayed, then `X` and `O` remain readable and distinguishable without color.

8. **Code and usability review**
   - When the source is reviewed, then its imports use only the Python standard library.
   - When the source is reviewed, then distinct responsibilities such as rendering, input validation, move selection, and game control are separated into functions with descriptive names.
   - When players select modes or moves, then prompts identify the permitted choices and the current player where applicable; errors identify the invalid selection and describe a valid alternative.

9. **Leaderboard**
   - Given fewer than five entries, when a human wins, then a qualifying player can enter initials and a score; when the board is full, a score must strictly exceed an existing score to qualify.
   - Given five scores and a new higher qualifying score, when initials are entered, then the leaderboard retains the five highest scores in descending order; a tie does not displace an existing entry.
   - Given a computer win or a draw, when a game ends, then no human leaderboard score is awarded for that result.
   - Given a running session, when a human wins multiple games, then their qualifying score reflects their session win total.
   - Given the program starts or a player declines replay, when the leaderboard is displayed, then its saved entries are shown.
   - Given a human move prompt, when `l` or `L` is entered, then the leaderboard is displayed and the same player can resume the same turn without changing the board.
   - Given leaderboard entries have been saved, when the program is restarted, then the same entries and scores are loaded from `leaderboard.csv` using manual CSV handling.
   - Given initials containing commas or quotation marks, when a leaderboard entry is saved and reloaded, then the initials and score are preserved without a parsing error.

10. **Computer move explanations**
   - Given a computer selects the center, blocks an opponent, or chooses randomly, when the move is returned and displayed, then its reason is respectively `center`, `block`, or `random` and appears alongside that move in the journal.
   - Given a human move, when the journal displays it, then it has no computer-selection reason.
11. **Computer versus computer**
   - Given the mode prompt, when it is displayed, then it offers `1` and `2` without showing `0`; entering `0` starts computer-versus-computer mode.
   - Given computer-versus-computer mode, when the game starts, then no mark-selection or human-move prompt appears, and the computer plays `O` first and `X` second.
   - Given either computer's turn, when it moves, then it applies the existing computer strategy using the other mark as its opponent and selects an empty square.
   - Given a computer-versus-computer game, when it progresses and ends, then the board and journal show its moves, the final result is displayed, and the replay prompt appears.
   - Given a computer-versus-computer game ends, when its result is recorded, then the corresponding `X` wins, `O` wins, or draws total increases exactly once; no initials are requested and the human leaderboard is unchanged.
   - Given replay is selected after a computer-versus-computer game, when a new game begins, then the player can choose any supported mode and the session totals are retained.
