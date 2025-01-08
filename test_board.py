import unittest
from board import Board
from player import Move
from minimax import Minimax


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_valid_move(self):
        move = Move("X", 1, 1)
        subgrid_idx = self.board.get_subboard_index(1, 1)
        self.assertTrue(self.board.subboards[subgrid_idx].is_valid_move(1, 1))
        self.board.subboards[subgrid_idx].make_move(move)
        self.assertFalse(self.board.subboards[subgrid_idx].is_valid_move(1, 1))

    def test_subgrid_winner(self):
        subgrid_idx = self.board.get_subboard_index(0, 0)
        moves = [
            Move("X", 0, 0),
            Move("X", 0, 1),
            Move("X", 0, 2),
        ]
        for move in moves:
            self.board.subboards[subgrid_idx].make_move(move)
        self.assertTrue(self.board.subboards[subgrid_idx].check_winner("X"))

    def test_full_subgrid(self):
        subgrid_idx = self.board.get_subboard_index(0, 0)
        moves = [
            Move("X", i // 3, i % 3) for i in range(9)
        ]
        for move in moves:
            self.board.subboards[subgrid_idx].make_move(move)
        self.assertTrue(self.board.subboards[subgrid_idx].is_full())

    def test_main_board_winner(self):
        # Simulează o victorie pe tabla principală
        winning_moves = [
            Move("X", 0, 0),
            Move("X", 0, 1),
            Move("X", 0, 2),
        ]
        for move in winning_moves:
            subgrid_idx = self.board.get_subboard_index(move.x, move.y)
            self.board.subboards[subgrid_idx].make_move(move)
        self.assertTrue(self.board.check_winner("X"))

    def test_main_board_draw(self):
        # Simulează o remiză pe tabla principală
        for i in range(9):
            for j in range(9):
                subgrid_idx = self.board.get_subboard_index(i, j)
                player = "X" if (i + j) % 2 == 0 else "O"
                self.board.subboards[subgrid_idx].make_move(Move(player, i % 3, j % 3))
        self.assertTrue(self.board.is_full())
        self.assertFalse(self.board.check_winner("X"))
        self.assertFalse(self.board.check_winner("O"))

    def test_ai_block_win(self):
        # AI-ul trebuie să blocheze victoria adversarului
        moves = [
            Move("X", 0, 0),
            Move("X", 0, 1),
        ]
        subgrid_idx = self.board.get_subboard_index(0, 0)
        for move in moves:
            self.board.subboards[subgrid_idx].make_move(move)
        
        ai_move = Minimax.find_best_move(self.board, "O", "X")
        self.assertEqual(ai_move.x, 0)
        self.assertEqual(ai_move.y, 2)

    def test_ai_win(self):
        # AI-ul trebuie să aleagă o mutare care îi aduce victoria
        moves = [
            Move("O", 1, 0),
            Move("O", 1, 1),
        ]
        subgrid_idx = self.board.get_subboard_index(1, 1)
        for move in moves:
            self.board.subboards[subgrid_idx].make_move(move)
        
        ai_move = Minimax.find_best_move(self.board, "O", "X")
        self.assertEqual(ai_move.x, 1)
        self.assertEqual(ai_move.y, 2)

    def test_ai_draw(self):
        # AI-ul ar trebui să joace pentru remiză dacă nu poate câștiga
        for i in range(9):
            for j in range(9):
                subgrid_idx = self.board.get_subboard_index(i, j)
                player = "X" if (i + j) % 2 == 0 else "O"
                if not (i == 8 and j == 8):  # Lasă un spațiu gol
                    self.board.subboards[subgrid_idx].make_move(Move(player, i % 3, j % 3))
        
        ai_move = Minimax.find_best_move(self.board, "O", "X")
        self.assertEqual(ai_move.x, 8)
        self.assertEqual(ai_move.y, 8)


if __name__ == "__main__":
    unittest.main()
