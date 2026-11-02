"""Text-based tic-tac-toe with human and random-computer modes."""

import random


WINNING_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def display_board(board):
    """Display empty squares as their positions from 1 through 9."""
    cells = [mark if mark else str(index + 1)
             for index, mark in enumerate(board)]
    print(f"\n {cells[0]} | {cells[1]} | {cells[2]}")
    print("---+---+---")
    print(f" {cells[3]} | {cells[4]} | {cells[5]}")
    print("---+---+---")
    print(f" {cells[6]} | {cells[7]} | {cells[8]}\n")


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


def get_human_move(board, player):
    """Prompt until the human selects an available board position."""
    while True:
        choice = input(f"Player {player}, choose a position (1-9): ").strip()
        if not choice.isdigit() or not 1 <= int(choice) <= 9:
            print("Please enter a number from 1 to 9.")
            continue
        position = int(choice) - 1
        if board[position]:
            print("That position is already taken. Choose another one.")
            continue
        return position


def get_computer_move(board):
    """Choose randomly from the currently available positions."""
    position = random.choice([index for index, mark in enumerate(board)
                              if not mark])
    print(f"Computer (X) chooses position {position + 1}.")
    return position


def play_game(mode):
    board = [""] * 9
    player = "O"

    for _ in range(9):
        display_board(board)
        if mode == "1" and player == "X":
            position = get_computer_move(board)
        else:
            position = get_human_move(board, player)

        board[position] = player
        if has_won(board, player):
            display_board(board)
            print(f"Player {player} wins!")
            return
        player = "X" if player == "O" else "O"

    display_board(board)
    print("It's a draw!")


def main():
    print("Tic-Tac-Toe")
    print("O always goes first.")
    while True:
        mode = choose_mode()
        if mode == "1":
            print("One-player mode: you are O and the computer is X.")
        else:
            print("Two-player mode: one human player is O and the other is X.")
        play_game(mode)
        answer = input("Play again? (y/n): ").strip().lower()
        if answer not in ("y", "yes"):
            print("Thanks for playing!")
            return


if __name__ == "__main__":
    main()
