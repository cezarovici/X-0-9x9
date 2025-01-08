from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QWidget,
    QGridLayout,
    QMenuBar,
    QAction,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from minimax import Minimax
from player import Move


class TicTacToe(QWidget):
    def __init__(self, shape, first_player):
        super().__init__()
        self.setWindowTitle("Tic-Tac-Toe")
        self.resize(400, 450)

        self.board_size = 3  # 3x3 pentru un Tic-Tac-Toe clasic
        self.logic = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]  # Tabla 3x3
        self.human_player = shape
        self.ai_player = "O" if shape == "X" else "X"
        self.current_player = self.human_player if first_player else self.ai_player
        self.game_over = False

        # Configurare UI
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Meniu
        self.menu_bar = QMenuBar(self)
        self.main_layout.setMenuBar(self.menu_bar)
        game_menu = self.menu_bar.addMenu("Game")
        reset_action = QAction("Reset", self)
        reset_action.triggered.connect(self.reset_game)
        game_menu.addAction(reset_action)

        # Tabla de joc
        self.board_layout = QGridLayout()
        self.main_layout.addLayout(self.board_layout)

        self.buttons = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                button = QPushButton("")
                button.setFont(QFont("Arial", 16))
                button.setFixedSize(100, 100)
                button.clicked.connect(lambda _, r=i, c=j: self.make_move(r, c))
                self.board_layout.addWidget(button, i, j)
                row.append(button)
            self.buttons.append(row)

        # Etichetă pentru status
        self.status_label = QLabel(f"Jucător curent: {self.current_player}")
        self.status_label.setFont(QFont("Arial", 16))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.status_label)

        if self.current_player == self.ai_player:
            self.ai_move()

    def make_move(self, row, col):
        if self.game_over:
            return

        if self.logic[row][col] != "":  # Verificăm dacă celula este deja ocupată
            self.status_label.setText("Mișcare invalidă! Celula este deja ocupată.")
            return

        self.logic[row][col] = self.current_player
        self.buttons[row][col].setText(self.current_player)

        if self.check_winner():
            self.status_label.setText(f"Jucătorul {self.current_player} a câștigat!")
            self.game_over = True
            return

        if all(self.logic[i][j] != "" for i in range(self.board_size) for j in range(self.board_size)):
            self.status_label.setText("Remiză!")
            self.game_over = True
            return

        self.current_player = self.ai_player if self.current_player == self.human_player else self.human_player
        self.status_label.setText(f"Jucător curent: {self.current_player}")

        if self.current_player == self.ai_player:
            QTimer.singleShot(500, self.ai_move)

    def ai_move(self):
        move = Minimax.find_best_move(self.logic, self.ai_player)
        if move:
            self.make_move(move[0], move[1])

    def reset_game(self):
        """Resetează jocul complet."""
        self.logic = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = self.human_player
        self.game_over = False
        self.status_label.setText(f"Jucător curent: {self.current_player}")
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.buttons[row][col].setText("")

    def check_winner(self):
        """Verifică dacă există un câștigător."""
        for i in range(self.board_size):
            # Verifică liniile
            if self.logic[i][0] == self.logic[i][1] == self.logic[i][2] != "":
                return True
            # Verifică coloanele
            if self.logic[0][i] == self.logic[1][i] == self.logic[2][i] != "":
                return True

        # Verifică diagonalele
        if self.logic[0][0] == self.logic[1][1] == self.logic[2][2] != "":
            return True
        if self.logic[0][2] == self.logic[1][1] == self.logic[2][0] != "":
            return True

        return False
