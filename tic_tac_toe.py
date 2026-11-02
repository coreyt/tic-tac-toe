"""Text-based tic-tac-toe with human and computer modes."""

import random
import sys
import os
import re


WINNING_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def supports_color():
    return sys.stdout.isatty() and os.environ.get("TERM") != "dumb" and "NO_COLOR" not in os.environ


def color_mark(mark):
    if supports_color() and mark in ("X", "O"):
        return f"\033[{33 if mark == 'X' else 34}m{mark}\033[0m"
    return mark


def color_text(text):
    return re.sub(r"\b[OX]\b", lambda match: color_mark(match.group()), text)


def display_board(board, journal=(), status="", prompt="", scores=None):
    """Render the padded board, journal, status, and prompt."""
    cells = [color_mark(mark) if mark else str(index + 1)
             for index, mark in enumerate(board)]
    border = "+---+---+---+"
    lines = [border]
    for row in range(3):
        lines.extend(("|   |   |   |",
                      "| " + " | ".join(cells[row * 3:row * 3 + 3]) + " |",
                      "|   |   |   |", border))
    entries = ["Move journal"] + [f"{number}. {color_mark(player)}: {position}"
                                  for number, (player, position) in enumerate(journal, 1)]
    if scores is not None:
        entries += ["", color_text(f"X Wins: {scores['X']} | O Wins: {scores['O']} | Draws: {scores['draw']}")]
    if sys.stdout.isatty():
        print("\033[H\033[2J", end="")
    for index, line in enumerate(lines):
        print(line + ("     " + entries[index] if index < len(entries) else ""))
    print("\n")
    print(color_text(prompt), end="", flush=True)
    if status:
        # Save the prompt cursor; put status below it without moving the board.
        if sys.stdout.isatty():
            print("\033[s\033[2B\r\033[2K" + color_text(status) + "\033[u", end="", flush=True)
        else:
            print("\n" + color_text(status))


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


def choose_mark():
    while True:
        choice = input("Choose your mark (X/O): ").strip().upper()
        if choice in ("X", "O"):
            return choice
        print("Please enter X or O.")


def get_human_move(board, player, journal=None, mode="2", human_mark="O", scores=None):
    """Prompt until the human selects an available board position."""
    error = ""
    while True:
        prompt = f"Player {player}, choose a position (1-9): "
        if journal is not None:
            computer_mark = "X" if human_mark == "O" else "O"
            status = error or (f"You are {human_mark}; the computer is {computer_mark}." if mode == "1" else f"Player 1: {human_mark}; Player 2: {computer_mark}")
            display_board(board, journal, status, prompt, scores)
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


def get_computer_move(board, human_mark="O"):
    """Block an immediate human win, or choose a random empty position."""
    position = None
    for line in WINNING_LINES:
        if sum(board[index] == human_mark for index in line) == 2:
            empty = [index for index in line if not board[index]]
            if empty:
                position = empty[0]
                break
    if position is None:
        position = random.choice([index for index, mark in enumerate(board)
                                  if not mark])
    return position


def play_game(mode, human_mark="O", scores=None):
    board = [""] * 9
    journal = []
    player = "O"

    for _ in range(9):
        if mode == "1" and player != human_mark:
            position = get_computer_move(board, human_mark)
        else:
            position = get_human_move(board, player, journal, mode, human_mark, scores)

        board[position] = player
        journal.append((player, position + 1))
        if has_won(board, player):
            return board, journal, player
        player = "X" if player == "O" else "O"

    return board, journal, "draw"


def main():
    print("Tic-Tac-Toe")
    print("O always goes first.")
    scores = {"X": 0, "O": 0, "draw": 0}
    while True:
        mode = choose_mode()
        human_mark = choose_mark()
        other_mark = "X" if human_mark == "O" else "O"
        if mode == "1":
            print(f"One-player mode: You are {human_mark}; the computer is {other_mark}.")
        else:
            print(f"Two-player mode: Player 1: {human_mark}; Player 2: {other_mark}.")
        board, journal, outcome = play_game(mode, human_mark, scores)
        scores[outcome] += 1
        result = "It's a draw!" if outcome == "draw" else f"Player {outcome} wins!"
        display_board(board, journal, result, "Play again? [Y/n]: ", scores)
        answer = input().strip().lower()
        if answer not in ("", "y", "yes"):
            print("Thanks for playing!")
            return


if __name__ == "__main__":
    main()
