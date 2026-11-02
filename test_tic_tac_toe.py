import contextlib
import io
import subprocess
import sys
import unittest
from unittest.mock import patch

import tic_tac_toe as game


class TicTacToeTests(unittest.TestCase):
    def run_main(self, inputs):
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs), contextlib.redirect_stdout(output):
            game.main()
        return output.getvalue()

    def test_terminal_entry_point(self):
        result = subprocess.run([sys.executable, "tic_tac_toe.py"], input="2\n1\n4\n2\n5\n3\nn\n", text=True, capture_output=True, check=True)
        self.assertIn("Player O wins!", result.stdout)

    def test_board_display(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            game.display_board([""] * 9)
        self.assertIn(" 1 | 2 | 3", output.getvalue())
        self.assertIn(" 4 | 5 | 6", output.getvalue())
        self.assertIn(" 7 | 8 | 9", output.getvalue())

    def test_mode_validation(self):
        with patch("builtins.input", side_effect=["bad", "3", " 2 "]), patch("builtins.print") as out:
            self.assertEqual(game.choose_mode(), "2")
        self.assertEqual(out.call_count, 2)

    def test_move_validation(self):
        with patch("builtins.input", side_effect=["bad", "0", "10", "1", "2"]), patch("builtins.print") as out:
            self.assertEqual(game.get_human_move(["O"] + [""] * 8, "X"), 1)
        self.assertEqual(out.call_count, 4)

    def test_two_player_win_and_replay(self):
        output = self.run_main(["2", "1", "4", "2", "5", "3", "y", "2", "1", "4", "2", "5", "3", "n"])
        self.assertEqual(output.count("Player O wins!"), 2)
        self.assertEqual(output.count(" 1 | 2 | 3"), 2)
        self.assertIn("Thanks for playing!", output)

    def test_draw(self):
        output = self.run_main(["2", "1", "2", "3", "5", "4", "6", "8", "7", "9", "n"])
        self.assertIn("It's a draw!", output)

    def test_all_winning_lines(self):
        for line in game.WINNING_LINES:
            for mark in ("O", "X"):
                board = [""] * 9
                for index in line:
                    board[index] = mark
                with self.subTest(line=line, mark=mark):
                    self.assertTrue(game.has_won(board, mark))
                    self.assertFalse(game.has_won(board, "X" if mark == "O" else "O"))

    def test_computer_blocks_each_line(self):
        for line in game.WINNING_LINES:
            for missing in line:
                board = [""] * 9
                for index in line:
                    if index != missing:
                        board[index] = "O"
                with self.subTest(line=line, missing=missing), patch("tic_tac_toe.random.choice", side_effect=lambda choices: next((x for x in choices if x != missing), choices[0])):
                    self.assertEqual(game.get_computer_move(board), missing)

    def test_multiple_threats(self):
        board = ["O", "O", "", "O", "X", "", "", "", "X"]
        with patch("tic_tac_toe.random.choice", side_effect=lambda choices: choices[-1]):
            self.assertIn(game.get_computer_move(board), (2, 6))

    def test_computer_chooses_available_square_when_no_threat(self):
        board = ["O", "X", "", "", "", "", "", "", ""]
        with patch("tic_tac_toe.random.choice", return_value=5) as choice:
            self.assertEqual(game.get_computer_move(board), 5)
        self.assertEqual(choice.call_args.args[0], [2, 3, 4, 5, 6, 7, 8])

    def test_one_player_assignment_and_automatic_turn(self):
        with patch("tic_tac_toe.random.choice", side_effect=lambda choices: choices[-1]):
            output = self.run_main(["1", "1", "2", "4", "5", "n"])
        self.assertIn("you are O and the computer is X", output)
        self.assertIn("Computer (X) chooses position", output)
        self.assertIn("Player X wins!", output)


if __name__ == "__main__":
    unittest.main()
