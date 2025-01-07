import sys
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer


class GameSettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setari Joc")
        self.resize(300, 200)

        self.selection = {"shape": "X", "first_player": True}

        layout = QVBoxLayout()

        # Alegerea formei
        layout.addWidget(QLabel("Alege forma:"))
        shape_layout = QHBoxLayout()
        self.x_button = QPushButton("X")
        self.o_button = QPushButton("O")
        self.x_button.setCheckable(True)
        self.o_button.setCheckable(True)
        self.x_button.setChecked(True)
        self.x_button.clicked.connect(self.select_x)
        self.o_button.clicked.connect(self.select_o)
        shape_layout.addWidget(self.x_button)
        shape_layout.addWidget(self.o_button)
        layout.addLayout(shape_layout)

        # Alegerea ordinii
        layout.addWidget(QLabel("Alege ordinea:"))
        order_layout = QHBoxLayout()
        self.first_button = QPushButton("Primul")
        self.second_button = QPushButton("Al doilea")
        self.first_button.setCheckable(True)
        self.second_button.setCheckable(True)
        self.first_button.setChecked(True)
        self.first_button.clicked.connect(self.select_first)
        self.second_button.clicked.connect(self.select_second)
        order_layout.addWidget(self.first_button)
        order_layout.addWidget(self.second_button)
        layout.addLayout(order_layout)

        # Butonul Start
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.accept)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def select_x(self):
        self.x_button.setChecked(True)
        self.o_button.setChecked(False)
        self.selection["shape"] = "X"

    def select_o(self):
        self.o_button.setChecked(True)
        self.x_button.setChecked(False)
        self.selection["shape"] = "O"

    def select_first(self):
        self.first_button.setChecked(True)
        self.second_button.setChecked(False)
        self.selection["first_player"] = True

    def select_second(self):
        self.second_button.setChecked(True)
        self.first_button.setChecked(False)
        self.selection["first_player"] = False


class TicTacToe(QWidget):
    def __init__(self, shape, first_player):
        super().__init__()
        self.setWindowTitle("Minimax")
        self.resize(400, 400)

        # setare caracter
        self.human_player = shape
        if shape == "X":
            self.ai_player = "O"
        else:
            self.ai_player = "X"

        # alegere player
        if first_player:
            self.current_player = self.human_player
        else:
            self.current_player = self.ai_player

        #setare tabela
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.board_layout = QGridLayout()
        self.main_layout.addLayout(self.board_layout)

        #initializare matrice si interfata
        self.buttons = [] # matrice joc
        for i in range(3):
            row = []
            for j in range(3):
                button = QPushButton("")
                button.setFont(QFont("Arial", 24))
                button.setFixedSize(100, 100)
                button.clicked.connect(lambda _, r=i, c=j: self.make_move(r, c))
                self.board_layout.addWidget(button, i, j)
                row.append(button)
            self.buttons.append(row)

        # Mesaj de status
        self.status_label = QLabel(f"Jucător curent: {self.current_player}")
        self.status_label.setFont(QFont("Arial", 16))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.status_label)

        # Daca AI-ul incepe facem manual o mutare pentru start
        if self.current_player == self.ai_player:
            self.ai_move()

    #mutarea humanoidului
    def make_move(self, row, col):
        #daca e game over/remiza sau butonul este completat oprim
        if self.game_over or self.board[row][col] != "":
            return

        # 
        self.board[row][col] = self.current_player
        self.buttons[row][col].setText(self.current_player)

        # Verifică dacă cineva a câștigat
        if self.check_winner():
            self.status_label.setText(f"Jucătorul {self.current_player} a câștigat!")
            self.game_over = True
            return

        # Verifică remiza
        if all(cell != "" for row in self.board for cell in row):
            self.status_label.setText("Remiză!")
            self.game_over = True
            return

        # Schimbă jucătorul
        self.current_player = (
            self.ai_player if self.current_player == self.human_player else self.human_player
        )
        self.status_label.setText(f"Jucător curent: {self.current_player}")

        # Mutarea AI-ului
        if self.current_player == self.ai_player:
            QTimer.singleShot(500, self.ai_move)  

        
    def ai_move(self):
        # Folosește algoritmul Minimax pentru a găsi mutarea optimă
        best_move = self.minimax(self.board, True)[1]
        if best_move:
            row, col = best_move
            self.make_move(row, col)
            

    def minimax(self, board, is_maximizing):
        # Verifică dacă este o stare finală
        if self.check_winner_on_board(board, self.ai_player):
            return 1, None  # AI câștigă
        if self.check_winner_on_board(board, self.human_player):
            return -1, None  # Jucătorul uman câștigă
        if all(cell != "" for row in board for cell in row):
            return 0, None  # Remiză

        best_score = -float("inf") if is_maximizing else float("inf")
        best_move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = self.ai_player if is_maximizing else self.human_player
                    score = self.minimax(board, not is_maximizing)[0]
                    board[i][j] = ""

                    if is_maximizing:
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)
                    else:
                        if score < best_score:
                            best_score = score
                            best_move = (i, j)

        return best_score, best_move

    def check_winner(self):
        return self.check_winner_on_board(self.board, self.current_player)

    def check_winner_on_board(self, board, player):
        # Verifică rânduri, coloane și diagonale
        for i in range(3):
            if (
                board[i][0] == board[i][1] == board[i][2] == player
                or board[0][i] == board[1][i] == board[2][i] == player
            ):
                return True
        if (
            board[0][0] == board[1][1] == board[2][2] == player
            or board[0][2] == board[1][1] == board[2][0] == player
        ):
            return True
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = GameSettingsDialog()
    if dialog.exec_() == QDialog.Accepted:
        settings = dialog.selection
        window = TicTacToe(settings["shape"], settings["first_player"])
        window.show()
        sys.exit(app.exec_())
