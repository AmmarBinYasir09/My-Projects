import unittest
import numpy as np
from project import create_board, drop_piece, is_valid_location, get_next_open_row, winning_move, get_valid_locations, score_position, minimax

class TestConnectFour(unittest.TestCase):

    def setUp(self):
        self.board = create_board()

    def test_create_board(self):
        self.assertEqual(self.board.shape, (6, 7))
        self.assertTrue(np.all(self.board == 0))

    def test_drop_piece(self):
        drop_piece(self.board, 0, 0, 1)
        self.assertEqual(self.board[0][0], 1)

    def test_is_valid_location(self):
        self.assertTrue(is_valid_location(self.board, 0))
        drop_piece(self.board, 5, 0, 1)

    def test_get_next_open_row(self):
        self.assertEqual(get_next_open_row(self.board, 0), 0)
        drop_piece(self.board, 0, 0, 1)
        self.assertEqual(get_next_open_row(self.board, 0), 1)

    def test_winning_move(self):
        for col in range(4):
            drop_piece(self.board, 0, col, 1)
        self.assertTrue(winning_move(self.board, 1))
        self.board = create_board()
        for row in range(4):
            drop_piece(self.board, row, 0, 1)
        self.assertTrue(winning_move(self.board, 1))
        self.board = create_board()
        for i in range(4):
            drop_piece(self.board, i, i, 1)
        self.assertTrue(winning_move(self.board, 1))
        self.board = create_board()
        for i in range(4):
            drop_piece(self.board, i, 3-i, 1)
        self.assertTrue(winning_move(self.board, 1))

    def test_get_valid_locations(self):
        valid_locations = get_valid_locations(self.board)
        self.assertEqual(valid_locations, list(range(7)))
        for col in range(7):
            for row in range(6):
                drop_piece(self.board, row, col, 1)
        valid_locations = get_valid_locations(self.board)
        self.assertEqual(valid_locations, [])

    def test_score_position(self):
        score = score_position(self.board, 1)
        self.assertEqual(score, 0)
        drop_piece(self.board, 0, 3, 1)
        score = score_position(self.board, 1)
        self.assertGreater(score, 0)

    def test_minimax(self):
        col, score = minimax(self.board, 5, -np.inf, np.inf, True)
        self.assertIn(col, range(7))
        self.assertIsInstance(score, (int, float))

if __name__ == '__main__':
    unittest.main()