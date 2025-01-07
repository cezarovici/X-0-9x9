import random

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

class SmallBoard:
    """ 
    Reprezinta o sub-tabela de 3x3 a jocului
    """
    def __init__(self):
        self.pieces = [["" for _ in range(3)] for _ in range(3)]
        self.winner = None  # Castigatorul acestei sub-table
    
    def is_valid_move(self, x, y):
        """ Verifica daca o mutare este valida """
        if x < 0 or x >= 3 or y < 0 or y >= 3:
            return False
        if self.pieces[x][y] != "":
            return False
        return True

    def make_move(self, move):
        """ Aplica mutarea pe sub-tabela """
        if self.is_valid_move(move.x, move.y):
            self.pieces[move.x][move.y] = move.symbol
            return True
        return False

    def check_winner(self, symbol):
        """ Verifica daca jucatorul a castigat pe sub-tabela """
        for i in range(3):
            if all(self.pieces[i][j] == symbol for j in range(3)):
                return True
            if all(self.pieces[j][i] == symbol for j in range(3)):
                return True
        if all(self.pieces[i][i] == symbol for i in range(3)):
            return True
        if all(self.pieces[i][2 - i] == symbol for i in range(3)):
            return True
        return False

class Board:
    """ Reprezinta tabla de joc mare formata din 9 sub-table mici """
    def __init__(self):
        self.size = 9
        self.subboards = [SmallBoard() for _ in range(9)]
        self.last_move = None

    def get_subboard_index(self, x, y):
        """ Determina indexul sub-tablei pe baza coordonatelor """
        return (x // 3) * 3 + (y // 3)

    def get_valid_subboard_indices(self):
        """ Returneaza lista de subboard-uri valide in care se pot face mutari """
        if not self.last_move:
            return [i for i in range(9)]  # Daca nu a fost nicio miscare, sunt valide toate subboard-urile
        
        # Subboard-ul in care trebuie sa se faca mutarea, determinat de ultima mutare
        subboard_idx = self.get_subboard_index(self.last_move.x, self.last_move.y)
        
        # Verifica daca subboard-ul este complet. Daca este, se pot face mutari in alt subboard
        subboard = self.subboards[subboard_idx]
        if all(cell != "" for row in subboard.pieces for cell in row):
            # Daca subboard-ul este complet, returneaza toate subboard-urile libere
            return [i for i in range(9) if any(self.subboards[i].pieces[x][y] == "" for x in range(3) for y in range(3))]
        
        return [subboard_idx]  # Daca subboard-ul nu este complet, doar acest subboard este valid

    def is_valid_move(self, move):
        """ Verifica daca mutarea este valida pe tabla mare """
        valid_subboards = self.get_valid_subboard_indices()
        
        if not (0 <= move.x < self.size and 0 <= move.y < self.size):
            return False

        subboard_idx = self.get_subboard_index(move.x, move.y)
        
        # Verifica daca subboard-ul este valid (daca se afla in lista de subboard-uri valide)
        if subboard_idx not in valid_subboards:
            return False

        sub_x = move.x % 3
        sub_y = move.y % 3
        if not self.subboards[subboard_idx].is_valid_move(sub_x, sub_y):
            return False

        return True

    def make_move(self, move):
        """ Aplica mutarea pe tabla mare """
        if self.is_valid_move(move):
            subboard_idx = self.get_subboard_index(move.x, move.y)
            sub_x = move.x % 3
            sub_y = move.y % 3
            if self.subboards[subboard_idx].make_move(Move(move.symbol, sub_x, sub_y)):
                self.last_move = move
                return True
        return False

    def check_winner(self, symbol):
        """ Verifica daca jucatorul a castigat pe tabla mare """
        for subboard in self.subboards:
            if subboard.check_winner(symbol):
                return True
        return False


class Minimax:
    @staticmethod
    def find_best_move(board, player_symbol, opponent_symbol):
        empty_cells = []

        valid_subboards = board.get_valid_subboard_indices()
        
        # Alegem un subboard valid în care să căutăm mutări
        for subboard_idx in valid_subboards:
            sub_x_start = (subboard_idx // 3) * 3
            sub_y_start = (subboard_idx % 3) * 3
            
            for i in range(sub_x_start, sub_x_start + 3):
                for j in range(sub_y_start, sub_y_start + 3):
                    if board.subboards[subboard_idx].pieces[i % 3][j % 3] == "":
                        empty_cells.append((i, j))

        if empty_cells:
            # Alegem aleatoriu o celulă liberă
            row, col = random.choice(empty_cells)
            return Move(player_symbol, row, col)  # Returnăm instanța Move
        
        return None
