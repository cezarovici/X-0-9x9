class PlayerType:
    NO_PLAYER = 0
    HUMAN = 1
    COMPUTER = 2

class Player:
    """ 
    Reprezinta o piesa de joc
    """
    def __init__(self, x, y, symbol, player):
        self.x = x           # pozitia X pe tabla de joc
        self.y = y           # pozitia Y pe tabla de joc
        self.symbol = symbol   # identificatorul piesei
        self.player = player # carui tip de jucator apartine piesa (om sau calculator)

class Move:
    """ Reprezinta o miscare a unui jucator """
    def __init__(self, symbol, x, y):
        self.symbol = symbol  # simbolul jucatorului (X sau O)
        self.x = x            # pozitia pe linia X (randul)
        self.y = y            # pozitia pe coloana Y (coloana)

    def is_valid(self, board):
        """ Verifica daca o miscare este valida """
        if not (0 <= self.x < board.size and 0 <= self.y < board.size):
            return False
        if board.pieces[self.x][self.y] != "":
            return False
        return True



