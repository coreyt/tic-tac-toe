import contextlib
import io
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tic_tac_toe as game


class TicTacToeTests(unittest.TestCase):
    def test_computer_move_reasons(self):
        self.assertEqual(game.get_computer_move([""] * 9), (4, "center"))
        self.assertEqual(game.get_computer_move(["O", "O", "", "", "X", "", "", "", ""]), (2, "block"))
        with patch("tic_tac_toe.random.choice", return_value=3):
            self.assertEqual(game.get_computer_move(["O", "X", "", "", "X", "", "", "", ""]), (3, "random"))

    def test_journal_shows_computer_reason_only(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            game.display_board([""] * 9, [("O", 1), ("X", 5, "center")])
        self.assertIn("1. O: 1", output.getvalue())
        self.assertIn("2. X: 5 (center)", output.getvalue())

    def test_center_precedes_block(self):
        for board in ([""] * 9, ["O", "O", "", "X", "", "", "", "", ""]):
            with self.subTest(board=board), patch("tic_tac_toe.random.choice") as random_choice:
                self.assertEqual(game.get_computer_move(board), (4, "center"))
                random_choice.assert_not_called()

    def test_block_precedes_computer_win(self):
        board = ["O", "O", "", "X", "X", "", "", "", ""]
        self.assertEqual(game.get_computer_move(board, "O"), (2, "block"))

    def test_block_tie_follows_line_order(self):
        board = ["O", "O", "", "O", "X", "", "", "", "X"]
        self.assertEqual(game.get_computer_move(board), (2, "block"))

    def test_blocked_line_is_not_a_threat(self):
        board = ["O", "O", "X", "", "X", "", "", "", ""]
        with patch("tic_tac_toe.random.choice", return_value=3) as choice:
            self.assertEqual(game.get_computer_move(board), (3, "random"))
        self.assertEqual(choice.call_args.args[0], [3, 5, 6, 7, 8])
    def test_hidden_zero_mode(self):
        with patch("builtins.input", return_value="0") as prompt:
            self.assertEqual(game.choose_mode(), "0")
        self.assertNotIn("0", prompt.call_args.args[0])

    def test_computer_versus_computer_game(self):
        output = io.StringIO()
        with patch("tic_tac_toe.random.choice", side_effect=lambda choices: choices[0]), patch("tic_tac_toe.get_human_move", side_effect=AssertionError("human prompt")), patch("tic_tac_toe.get_computer_move", wraps=game.get_computer_move) as computer, contextlib.redirect_stdout(output):
            board, journal, outcome = game.play_game("0")
        self.assertEqual([entry[0] for entry in journal], ["O" if i % 2 == 0 else "X" for i in range(len(journal))])
        self.assertEqual(len({entry[1] for entry in journal}), len(journal))
        self.assertTrue(all(entry[2] in ("center", "block", "random") for entry in journal))
        self.assertEqual(journal[0], ("O", 5, "center"))
        self.assertIn(outcome, ("O", "X", "draw"))
        self.assertIn("Move journal", output.getvalue())
        self.assertEqual(sum(bool(cell) for cell in board), len(journal))
        self.assertEqual([call.args[1] for call in computer.call_args_list], ["X" if entry[0] == "O" else "O" for entry in journal])

    def test_computer_game_updates_scores_without_leaderboard_entry(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["0", "n"]), patch("tic_tac_toe.load_leaderboard", return_value=[]), patch("tic_tac_toe.save_leaderboard") as save, patch("tic_tac_toe.random.choice", side_effect=lambda choices: choices[0]), contextlib.redirect_stdout(output):
            game.main()
        save.assert_not_called()
        self.assertIn("Play again? [Y/n]", output.getvalue())
        totals = re.findall(r"X Wins: (\d+) \| O Wins: (\d+) \| Draws: (\d+)", output.getvalue())
        self.assertTrue(totals)
        self.assertEqual(sum(map(int, totals[-1])), 1)
        self.assertNotIn("enter initials", output.getvalue())

    def test_leaderboard_persistence(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "leaderboard.csv"
            self.assertEqual(game.load_leaderboard(path), [])
            entries = [("ABC", 4), ("DEF", 2)]
            game.save_leaderboard(entries, path)
            self.assertEqual(game.load_leaderboard(path), entries)

    def test_leaderboard_during_turn_preserves_board(self):
        board = ["O"] + [""] * 8
        output = io.StringIO()
        with patch("builtins.input", side_effect=["L", "", "2"]), contextlib.redirect_stdout(output):
            move = game.get_human_move(board, "X", [], leaderboard=[("ABC", 3)])
        self.assertEqual(move, 1)
        self.assertEqual(board, ["O"] + [""] * 8)
        self.assertIn("ABC: 3 wins", output.getvalue())

    def test_human_win_is_saved_and_shown_on_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "leaderboard.csv"
            output = io.StringIO()
            load = game.load_leaderboard
            save = game.save_leaderboard
            with patch("builtins.input", side_effect=["2", "O", "1", "4", "2", "5", "3", "ABC", "n"]), patch("tic_tac_toe.load_leaderboard", side_effect=lambda: load(path)), patch("tic_tac_toe.save_leaderboard", side_effect=lambda entries: save(entries, path)), contextlib.redirect_stdout(output):
                game.main()
            self.assertIn("ABC: 1 wins", output.getvalue())
            self.assertEqual(path.read_text(), "ABC,1\n")

    def test_mark_selection_validation(self):
        with patch("builtins.input", side_effect=["bad", " x "]), patch("builtins.print") as out:
            self.assertEqual(game.choose_mark(), "X")
            self.assertEqual(out.call_count, 1)

    def test_computer_blocks_x(self):
        with patch("tic_tac_toe.random.choice", return_value=8):
            self.assertEqual(game.get_computer_move(["X", "X", "", "O", "O", "", "", "", ""], "X"), (2, "block"))

    def test_colorized_board_and_plain_fallback(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch.object(output, "isatty", return_value=True), patch("tic_tac_toe.supports_color", return_value=True):
            game.display_board(["X", "O"] + [""] * 7)
        self.assertIn("\033[33mX\033[0m", output.getvalue())
        self.assertIn("\033[34mO\033[0m", output.getvalue())
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            game.display_board(["X", "O"] + [""] * 7)
        self.assertNotIn("\033[", output.getvalue())

    def test_session_scores_and_mark_changes(self):
        output = self.run_main(["2", "x", "1", "4", "2", "5", "3", "y", "2", "o", "1", "2", "3", "5", "4", "6", "8", "7", "9", "n"])
        self.assertIn("Player 1: X", output)
        self.assertIn("Player 2: O", output)
        self.assertIn("X Wins: 0 | O Wins: 1 | Draws: 1", output)

    def test_computer_opens_when_human_is_x(self):
        with patch("tic_tac_toe.random.choice", side_effect=lambda choices: choices[-1]):
            output = self.run_main(["1", "x", "1", "2", "4", "n"])
        self.assertIn("1. O:", output)
        self.assertIn("You are X; the computer is O", output)

    def run_main(self, inputs):
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs), patch("tic_tac_toe.load_leaderboard", return_value=[]), patch("tic_tac_toe.qualifies_for_leaderboard", return_value=False), contextlib.redirect_stdout(output):
            game.main()
        return output.getvalue()

    def test_terminal_entry_point(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(Path(game.__file__).resolve())], cwd=directory, input="2\nO\n1\n4\n2\n5\n3\nABC\nn\n", text=True, capture_output=True, check=True)
        self.assertIn("Player O wins!", result.stdout)

    def test_board_display(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            game.display_board([""] * 9)
        self.assertIn(" 1 | 2 | 3", output.getvalue())
        self.assertIn(" 4 | 5 | 6", output.getvalue())
        self.assertIn(" 7 | 8 | 9", output.getvalue())

    def test_mode_validation(self):
        with patch("builtins.input", side_effect=["bad", "no", " 2 "]), patch("builtins.print") as out:
            self.assertEqual(game.choose_mode(), "2")
        self.assertEqual(out.call_count, 2)

    def test_move_validation(self):
        with patch("builtins.input", side_effect=["bad", "0", "10", "1", "2"]), patch("builtins.print") as out:
            self.assertEqual(game.get_human_move(["O"] + [""] * 8, "X"), 1)
        self.assertEqual(out.call_count, 4)

    def test_two_player_win_and_replay(self):
        output = self.run_main(["2", "O", "1", "4", "2", "5", "3", "y", "2", "O", "1", "4", "2", "5", "3", "n"])
        self.assertEqual(output.count("Player O wins!"), 2)
        self.assertEqual(output.count(" 1 | 2 | 3"), 2)
        self.assertIn("Thanks for playing!", output)

    def test_draw(self):
        output = self.run_main(["2", "O", "1", "2", "3", "5", "4", "6", "8", "7", "9", "n"])
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
                if missing == 4:
                    continue
                for human in ("O", "X"):
                    board = [""] * 9
                    for index in line:
                        if index != missing:
                            board[index] = human
                    if not board[4]:
                        board[4] = "X" if human == "O" else "O"
                    with self.subTest(line=line, missing=missing, human=human), patch("tic_tac_toe.random.choice", side_effect=lambda choices: next((x for x in choices if x != missing), choices[0])):
                        self.assertEqual(game.get_computer_move(board, human), (missing, "block"))

    def test_multiple_threats(self):
        board = ["O", "O", "", "O", "X", "", "", "", "X"]
        with patch("tic_tac_toe.random.choice", side_effect=lambda choices: choices[-1]):
            self.assertIn(game.get_computer_move(board), ((2, "block"), (6, "block")))

    def test_computer_chooses_available_square_when_no_threat(self):
        board = ["O", "X", "", "", "X", "", "", "", ""]
        with patch("tic_tac_toe.random.choice", return_value=5) as choice:
            self.assertEqual(game.get_computer_move(board), (5, "random"))
        self.assertEqual(choice.call_args.args[0], [2, 3, 5, 6, 7, 8])

    def test_one_player_assignment_and_automatic_turn(self):
        with patch("tic_tac_toe.random.choice", side_effect=lambda choices: choices[-1]):
            output = self.run_main(["1", "O", "1", "2", "4", "n"])
        self.assertIn("You are O; the computer is X", output)
        self.assertIn("2. X: 5 (center)", output)
        self.assertIn("4. X: 3 (block)", output)
        self.assertIn("Player X wins!", output)

    def test_padded_layout_journal_and_prompt(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            game.display_board(["O"] + [""] * 8, [("O", 1), ("X", 5)], prompt="Move: ")
        lines = output.getvalue().splitlines()
        self.assertEqual(lines[0], "+---+---+---+     Move journal")
        self.assertEqual(lines[1], "|   |   |   |     1. O: 1")
        self.assertEqual(lines[2], "| O | 2 | 3 |     2. X: 5")
        self.assertEqual(lines[3], "|   |   |   |")
        self.assertEqual(lines[13:16], ["", "", "Move: "])

    def test_empty_replay_starts_new_game_and_resets_journal(self):
        output = self.run_main(["2", "O", "1", "4", "2", "5", "3", "", "2", "O", "1", "4", "2", "5", "3", "n"])
        self.assertEqual(output.count("Player O wins!"), 2)
        self.assertEqual(output.count("| 1 | 2 | 3 |"), 2)

    def test_terminal_redraw_uses_fixed_origin(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch.object(output, "isatty", return_value=True):
            game.display_board([""] * 9, status="Invalid move", prompt="Move: ")
        self.assertTrue(output.getvalue().startswith("\033[H\033[2J+---+"))
        self.assertIn("\033[s\033[2B\r\033[2KInvalid move\033[u", output.getvalue())


if __name__ == "__main__":
    unittest.main()
