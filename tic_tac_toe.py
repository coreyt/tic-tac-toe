"""Text-based tic-tac-toe with human and computer modes."""

import random
import sys


WINNING_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def display_board(board, journal=(), status="", prompt=""):
    """Render the padded board, journal, status, and prompt."""
    cells = [mark if mark else str(index + 1)
             for index, mark in enumerate(board)]
    border = "+---+---+---+"
    lines = [border]
    for row in range(3):
        lines.extend(("|   |   |   |",
                      "| " + " | ".join(cells[row * 3:row * 3 + 3]) + " |",
                      "|   |   |   |", border))
    entries = ["Move journal"] + [f"{number}. {player}: {position}"
                                  for number, (player, position) in enumerate(journal, 1)]
    if sys.stdout.isatty():
        print("\033[H\033[2J", end="")
    for index, line in enumerate(lines):
        print(line + ("     " + entries[index] if index < len(entries) else ""))
    print("\n")
    print(prompt, end="", flush=True)
    if status:
        # Save the prompt cursor; put status below it without moving the board.
        if sys.stdout.isatty():
            print("\033[s\033[2B\r\033[2K" + status + "\033[u", end="", flush=True)
        else:
            print("\n" + status)


def has_won(board, player):
    return any(all(board[index] == player for index in line)
               for line in WINNING_LINES)


def choose_mode():
    """Ask whether this game has one human player or two."""
    while True:
        choice = input("Choose a mode: 1 player or 2 players (1/2): ").strip()
        if choice in ("1", "2"):
            return choice
        print("Please enter 1 for one player or 2 for two players.")


def get_human_move(board, player, journal=None, mode="2"):
    """Prompt until the human selects an available board position."""
    error = ""
    while True:
        prompt = f"Player {player}, choose a position (1-9): "
        if journal is not None:
            status = error or ("You are O; the computer is X." if mode == "1" else "")
            display_board(board, journal, status, prompt)
            choice = input().strip()
        else:
            choice = input(prompt).strip()
        if choice not in tuple(str(number) for number in range(1, 10)):
            error = "Please enter a number from 1 to 9."
            if journal is None:
                print(error)
            continue
        position = int(choice) - 1
        if board[position]:
            error = "That position is already taken. Choose another one."
            if journal is None:
                print(error)
            continue
        return position


def get_computer_move(board):
    """Block an immediate human win, or choose a random empty position."""
    position = None
    for line in WINNING_LINES:
        if sum(board[index] == "O" for index in line) == 2:
            empty = [index for index in line if not board[index]]
            if empty:
                position = empty[0]
                break
    if position is None:
        position = random.choice([index for index, mark in enumerate(board)
                                  if not mark])
    return position


def play_game(mode):
    board = [""] * 9
    journal = []
    player = "O"

    for _ in range(9):
        if mode == "1" and player == "X":
            position = get_computer_move(board)
        else:
            position = get_human_move(board, player, journal, mode)

        board[position] = player
        journal.append((player, position + 1))
        if has_won(board, player):
            return board, journal, f"Player {player} wins!"
        player = "X" if player == "O" else "O"

    return board, journal, "It's a draw!"


def main():
    print("Tic-Tac-Toe")
    print("O always goes first.")
    while True:
        mode = choose_mode()
        if mode == "1":
            print("One-player mode: you are O and the computer is X.")
        else:
            print("Two-player mode: one human player is O and the other is X.")
        board, journal, result = play_game(mode)
        display_board(board, journal, result, "Play again? [Y/n]: ")
        answer = input().strip().lower()
        if answer not in ("", "y", "yes"):
            print("Thanks for playing!")
            return


if __name__ == "__main__":
    main()
