class SmallBoard:
    def __init__(self):
        # Tabla este reprezentată ca o matrice 3x3
        self.pieces = [["" for _ in range(3)] for _ in range(3)]
        self.winner = None

    def is_valid_move(self, row, col):
        """Verifică dacă o mișcare este validă."""
        return self.pieces[row][col] == "" and self.winner is None

    def make_move(self, move):
        """Aplică mișcarea pe tablă."""
        if not self.is_valid_move(move.x, move.y):
            raise ValueError("Mutare invalidă!")
        self.pieces[move.x][move.y] = move.symbol

    def check_winner(self, player):
        """Verifică dacă jucătorul a câștigat această sub-tabelă."""
        # Linie orizontală sau verticală
        for i in range(3):
            if all(self.pieces[i][j] == player for j in range(3)) or \
               all(self.pieces[j][i] == player for j in range(3)):
                self.winner = player
                return True

        # Diagonale
        if all(self.pieces[i][i] == player for i in range(3)) or \
           all(self.pieces[i][2 - i] == player for i in range(3)):
            self.winner = player
            return True

        return False

    def is_full(self):
        """Verifică dacă tabla este completă."""
        return all(self.pieces[i][j] != "" for i in range(3) for j in range(3))
