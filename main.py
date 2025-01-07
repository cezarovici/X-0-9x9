import random
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QWidget,
    QGridLayout,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

from player import Board, Minimax, Move

# GameSettingsDialog for customizing the game
class GameSettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setări Joc")
        self.resize(300, 200)
        self.selection = {"shape": "X", "first_player": True, "board_size": 9}
        layout = QVBoxLayout()

        # Shape selection (X or O)
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

        # First player selection
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

        # Start button
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

# TicTacToe Game interface
class TicTacToe(QWidget):
    def __init__(self, shape, first_player):
        super().__init__()
        self.setWindowTitle("Ultimate Tic-Tac-Toe")
        self.resize(600, 600)

        self.logic = Board()
        self.human_player = shape
        self.ai_player = "O" if shape == "X" else "X"
        self.current_player = self.human_player if first_player else self.ai_player

        # Initialize the game board
        self.board_size = 9
        self.game_over = False
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.board_layout = QGridLayout()
        self.main_layout.addLayout(self.board_layout)

        self.buttons = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                button = QPushButton("")
                button.setFont(QFont("Arial", 16))
                button.setFixedSize(60, 60)
                button.clicked.connect(lambda _, r=i, c=j: self.make_move(r, c))
                self.board_layout.addWidget(button, i, j)
                row.append(button)
            self.buttons.append(row)

        self.status_label = QLabel(f"Jucător curent: {self.current_player}")
        self.status_label.setFont(QFont("Arial", 16))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.status_label)

        if self.current_player == self.ai_player:
            self.ai_move()

    def make_move(self, row, col):
        if self.game_over:
            return

        sub_x = row % 3
        sub_y = col % 3
        move = Move(self.current_player, sub_x, sub_y)
        subgrid_idx = self.logic.get_subboard_index(row, col)
        
        # Verifică dacă mișcarea este validă
        if not self.logic.subboards[subgrid_idx].is_valid_move(sub_x, sub_y):
            self.status_label.setText("Mișcare invalidă!")
            return
        
        # Aplica mișcarea
        
        print(row,col)
        
        self.logic.subboards[subgrid_idx].make_move(move)
        self.buttons[row][col].setText(self.current_player)

        if self.logic.subboards[subgrid_idx].check_winner(self.current_player):
            self.status_label.setText(f"Jucătorul {self.current_player} a câștigat această sub-tabelă!")
        
        if self.logic.check_winner(self.current_player):
            self.status_label.setText(f"Jucătorul {self.current_player} a câștigat!")
            self.game_over = True
            return

        if all(self.logic.subboards[subgrid_idx].pieces[i][j] != "" for i in range(3) for j in range(3)):
            self.status_label.setText("Remiză!")
            self.game_over = True
            return

        # Schimbă jucătorul
        self.current_player = self.ai_player if self.current_player == self.human_player else self.human_player
        self.status_label.setText(f"Jucător curent: {self.current_player}")

        if self.current_player == self.ai_player:
            QTimer.singleShot(500, self.ai_move)

    def ai_move(self):
        move = Minimax.find_best_move(self.logic, self.ai_player, self.human_player)
        if move:
            subgrid_idx = self.logic.get_subboard_index(move.x, move.y)
            row = (subgrid_idx // 3) * 3 + move.x
            col = (subgrid_idx % 3) * 3 + move.y
            self.make_move(row, col)

    def highlight_subgrid(self, subgrid_idx):
        """ Evidentiaza sub-tabela in care se poate face mutarea """
        row_start = (subgrid_idx // 3) * 3
        col_start = (subgrid_idx % 3) * 3
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                self.buttons[i][j].setStyleSheet("background-color: lightblue")

    def update_board(self):
        """ Actualizează UI-ul cu starea curentă a tablei de joc """
        for row in range(self.board_size):
            for col in range(self.board_size):
                subgrid_idx = self.logic.get_subboard_index(row, col)
                piece = self.logic.subboards[subgrid_idx].pieces[row % 3][col % 3]
                self.buttons[row][col].setText(piece)

        # Evidentiază sub-tabela în care se poate face mutarea
        if self.logic.last_move:
            last_move = self.logic.last_move
            next_subgrid = self.logic.get_subboard_index(last_move.x, last_move.y)
            self.highlight_subgrid(next_subgrid)

# Application entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = GameSettingsDialog()
    if dialog.exec_() == QDialog.Accepted:
        settings = dialog.selection
        window = TicTacToe(settings["shape"], settings["first_player"])
        window.show()
        sys.exit(app.exec_())
