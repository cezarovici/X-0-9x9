from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QWidget,
    QVBoxLayout,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from small import *

class TicTacToe(QWidget):
    def __init__(self, shape, first_player, difficulty="Hard"):
        super().__init__()
        self.setWindowTitle("Minimaxu' 9x9")
        self.resize(600, 600)

        self.main_winner = None #proprietate castigator
        self.active_board = None  # proprietate pentru tabla curenta
        self.difficulty = difficulty

        #setare forma si ordine de start
        self.human_player = shape
        self.ai_player = "X" if shape == "O" else "O"
        self.current_player = self.human_player if first_player else self.ai_player

        #setari layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        #matrice pentru tabela mare formata din tabele mici
        self.main_board = [[SmallBoard(self, i, j) for j in range(3)] for i in range(3)]

        #se asaza cate un widget care reprezinta cate o tabela mica
        for i in range(3):
            for j in range(3):
                self.grid_layout.addWidget(self.main_board[i][j], i, j)

        #mesajul de status
        self.status_label = QLabel(f"Jucator curent: {self.current_player}")
        self.status_label.setFont(QFont("Arial", 16))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.status_label)

    
    def switch_player(self):
        # Oprește jocul dacă există un câștigător pe tabla mare
        if self.main_winner is not None:
            return

        # se schimba jucatorul
        self.current_player = self.human_player if self.current_player == self.ai_player else self.ai_player
        self.status_label.setText(f"Jucător curent: {self.current_player}")

        if self.active_board is not None:
            #coloram si mutam
            if self.current_player == self.human_player:
                if self.active_board is not None:
                    row, col = self.active_board
                    self.highlight_active_board(row, col, "human")
            elif self.current_player == self.ai_player:
                row, col = self.active_board
                self.highlight_active_board(row, col, "ai")
                QTimer.singleShot(800, self.ai_move)
                
        else:
            # Nu există o mutare obligatorie; resetează stilizarea tuturor tablelor
            for i in range(3):
                for j in range(3):
                    if self.main_board[i][j].winner is None:
                        self.main_board[i][j].setStyleSheet("")

             

        
    def highlight_active_board(self, row, col, player):
        #resetam fundalul la tabele mici daca nu s winner si coloram 
        for i in range(3):
            for j in range(3):
                if self.main_board[i][j].winner is None:  
                    self.main_board[i][j].setStyleSheet("")

        if self.active_board is not None:
            if self.main_board[row][col].winner is None:
                if player == "human":
                    self.main_board[row][col].setStyleSheet("background-color: lightgreen; border: 2px solid darkblue;")
                elif player == "ai":
                    self.main_board[row][col].setStyleSheet("background-color: lightcoral; border: 2px solid darkblue;")

    
    def update_active_board(self, row, col):
        #daca tablea pe care suntem are castigator nu avem o tabela de obligatie
        if self.main_board[row][col].winner:
            self.active_board = None
        else:
            self.active_board = (row, col) #salvam coordonatele din tabela mare a tabelei mici de obligativitate


    #verifica daca exista vreun castigator al tablei mari, 
    def update_main_board(self, row, col, winner):
        if self.main_winner is not None:
            return

        if winner == "X":
            self.main_board[row][col].setStyleSheet("background-color: green;")
        else:
            self.main_board[row][col].setStyleSheet("background-color: red;")

        if self.check_main_winner():
            self.status_label.setText(f"Jucătorul {self.main_winner} a câștigat!")
            self.main_winner = self.current_player  # Setăm câștigătorul jocului


    #verifica castigatorul pe tabela mare
    def check_main_winner(self):
        for i in range(3):
            if (
                self.main_board[i][0].winner == self.main_board[i][1].winner == self.main_board[i][2].winner != None
                or self.main_board[0][i].winner == self.main_board[1][i].winner == self.main_board[2][i].winner != None
            ):
                self.main_winner = self.current_player
                return True
        if (
            self.main_board[0][0].winner == self.main_board[1][1].winner == self.main_board[2][2].winner != None
            or self.main_board[0][2].winner == self.main_board[1][1].winner == self.main_board[2][0].winner != None
        ):
            self.main_winner = self.current_player
            return True
        return False


    def ai_move(self):
        depth = 2 if self.difficulty == "Easy" else 4
        available_boards = [(i, j) for i in range(3) for j in range(3) if self.main_board[i][j].winner is None]

        if self.active_board is None or self.main_board[self.active_board[0]][self.active_board[1]].winner is not None:
            if available_boards:
                best_score = -float("inf")
                best_board = None
                for board_pos in available_boards:
                    row, col = board_pos
                    small_board = self.main_board[row][col]
                    available_moves = [(r, c) for r in range(3) for c in range(3) if small_board.board[r][c] == ""]
                    for move in available_moves:
                        r, c = move
                        small_board.board[r][c] = self.ai_player
                        score, _ = self.minimax(self.main_board, False, depth - 1, -float("inf"), float("inf"))
                        small_board.board[r][c] = ""
                        if score > best_score:
                            best_score = score
                            best_board = board_pos
                if best_board:
                    self.active_board = best_board

        if self.active_board:
            row, col = self.active_board
            small_board = self.main_board[row][col]
            available_moves = [(r, c) for r in range(3) for c in range(3) if small_board.board[r][c] == ""]
            if available_moves:
                best_score = -float("inf")
                best_move = None
                for move in available_moves:
                    r, c = move
                    small_board.board[r][c] = self.ai_player
                    score, _ = self.minimax(self.main_board, False, depth - 1, -float("inf"), float("inf"))
                    small_board.board[r][c] = ""
                    if score > best_score:
                        best_score = score
                        best_move = move

                if best_move:
                    r, c = best_move
                    small_board.make_move(r, c)

    def minimax(self, board, is_maximizing, depth, alpha, beta):
        if self.check_main_winner():
            return (1 if self.current_player == self.ai_player else -1), None

        if depth == 0 or all(
            small_board.winner is not None or all(cell != "" for row in small_board.board for cell in row)
            for row_boards in board for small_board in row_boards
        ):
            return 0, None

        best_score = -float("inf") if is_maximizing else float("inf")
        best_move = None

        for i in range(3):
            for j in range(3):
                small_board = board[i][j]
                if small_board.winner is None:
                    for r in range(3):
                        for c in range(3):
                            if small_board.board[r][c] == "":
                                small_board.board[r][c] = self.ai_player if is_maximizing else self.human_player
                                score, _ = self.minimax(board, not is_maximizing, depth - 1, alpha, beta)
                                small_board.board[r][c] = ""

                                if is_maximizing:
                                    if score > best_score:
                                        best_score = score
                                        best_move = (i, j, r, c)
                                    alpha = max(alpha, best_score)
                                else:
                                    if score < best_score:
                                        best_score = score
                                        best_move = (i, j, r, c)
                                    beta = min(beta, best_score)

                                if beta <= alpha:
                                    break

        return best_score, best_move
