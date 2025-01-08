from smallboard import SmallBoard
from player import Move

class Board:
    def __init__(self):
        # Tabla mare conține 9 subtabele
        self.subboards = [SmallBoard() for _ in range(9)]
        self.last_move = None

    def get_subboard_index(self, row, col):
        """Returnează indexul subboard-ului pe baza coordonatelor mari."""
        return (row % 3) * 3 + (col % 3)

    def is_valid_move(self, row, col):
        """Verifică dacă o mutare este validă pe tabla mare."""
        subboard_idx = self.get_subboard_index(row, col)
        sub_x, sub_y = row % 3, col % 3
        return self.subboards[subboard_idx].is_valid_move(sub_x, sub_y)

    def make_move(self, move):
        """Aplica mișcarea pe tabla corespunzătoare."""
        subboard_idx = self.get_subboard_index(move.x, move.y)
        self.subboards[subboard_idx].make_move(move)
        self.last_move = move

    def check_winner(self, player):
        """Verifică dacă jucătorul a câștigat tabla mare."""
        # Creează o reprezentare a câștigătorilor subtabelelor
        winners = [subboard.winner for subboard in self.subboards]

        # Linie orizontală sau verticală
        for i in range(3):
            if all(winners[i * 3 + j] == player for j in range(3)) or \
               all(winners[j * 3 + i] == player for j in range(3)):
                return True

        # Diagonale
        if all(winners[i * 3 + i] == player for i in range(3)) or \
           all(winners[i * 3 + (2 - i)] == player for i in range(3)):
            return True

        return False

    def is_draw(self):
        """Verifică dacă toate subtabelele sunt pline și nu există câștigător."""
        return all(subboard.is_full() for subboard in self.subboards)
