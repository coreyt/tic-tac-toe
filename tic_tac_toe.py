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

LEADERBOARD_FILE = "leaderboard.csv"
LEADERBOARD_SLOTS = 5


def load_leaderboard(path=LEADERBOARD_FILE):
    try:
        with open(path, encoding="utf-8") as file:
            entries = []
            for line in file:
                initials, wins = line.rstrip("\n").split(",")
                entries.append((initials, int(wins)))
            return entries
    except FileNotFoundError:
        return []


def save_leaderboard(entries, path=LEADERBOARD_FILE):
    with open(path, "w", encoding="utf-8", newline="") as file:
        for initials, wins in entries:
            file.write(f"{initials},{wins}\n")


def qualifies_for_leaderboard(entries, wins):
    return len(entries) < LEADERBOARD_SLOTS - 1 or any(wins > score for _, score in entries)


def add_leaderboard_entry(entries, initials, wins):
    return sorted([*entries, (initials, wins)], key=lambda entry: entry[1], reverse=True)[:LEADERBOARD_SLOTS - 1]


def display_leaderboard(entries):
    print("\nLeaderboard")
    if not entries:
        print("No scores yet.")
    for index, (initials, wins) in enumerate(entries, 1):
        print(f"{index}. {initials}: {wins} wins")


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


def get_human_move(board, player, journal=None, mode="2", human_mark="O", scores=None, leaderboard=None):
    """Prompt until the human selects an available board position."""
    error = ""
    while True:
        prompt = f"Player {player}, choose a position (1-9) or L for leaderboard: "
        if journal is not None:
            computer_mark = "X" if human_mark == "O" else "O"
            status = error or (f"You are {human_mark}; the computer is {computer_mark}." if mode == "1" else f"Player 1: {human_mark}; Player 2: {computer_mark}")
            display_board(board, journal, status, prompt, scores)
            choice = input().strip()
        else:
            choice = input(prompt).strip()
        if choice.lower() == "l":
            display_leaderboard(leaderboard if leaderboard is not None else [])
            input("Press Enter to return to the game: ")
            continue
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


def play_game(mode, human_mark="O", scores=None, leaderboard=None):
    board = [""] * 9
    journal = []
    player = "O"

    for _ in range(9):
        if mode == "1" and player != human_mark:
            position = get_computer_move(board, human_mark)
        else:
            position = get_human_move(board, player, journal, mode, human_mark, scores, leaderboard)

        board[position] = player
        journal.append((player, position + 1))
        if has_won(board, player):
            return board, journal, player
        player = "X" if player == "O" else "O"

    return board, journal, "draw"


def main():
    print("Tic-Tac-Toe")
    print("O always goes first.")
    leaderboard = load_leaderboard()
    display_leaderboard(leaderboard)
    scores = {"X": 0, "O": 0, "draw": 0}
    human_wins = {1: 0, 2: 0}
    while True:
        mode = choose_mode()
        human_mark = choose_mark()
        other_mark = "X" if human_mark == "O" else "O"
        if mode == "1":
            print(f"One-player mode: You are {human_mark}; the computer is {other_mark}.")
        else:
            print(f"Two-player mode: Player 1: {human_mark}; Player 2: {other_mark}.")
        board, journal, outcome = play_game(mode, human_mark, scores, leaderboard)
        scores[outcome] += 1
        result = "It's a draw!" if outcome == "draw" else f"Player {outcome} wins!"
        human_winner = None
        if outcome != "draw":
            if outcome == human_mark:
                human_winner = 1
            elif mode == "2":
                human_winner = 2
        if human_winner is not None:
            human_wins[human_winner] += 1
            wins = human_wins[human_winner]
            if qualifies_for_leaderboard(leaderboard, wins):
                display_board(board, journal, result, f"Player {human_winner}, enter initials: ", scores)
                initials = input()
                leaderboard = add_leaderboard_entry(leaderboard, initials, wins)
                save_leaderboard(leaderboard)
        display_board(board, journal, result, "Play again? [Y/n]: ", scores)
        answer = input().strip().lower()
        if answer not in ("", "y", "yes"):
            display_leaderboard(leaderboard)
            print("Thanks for playing!")
            return


if __name__ == "__main__":
    main()
