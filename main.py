import sys
from PyQt5.QtWidgets import (
    QApplication,

    QPushButton,
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
)

from TicTacToe import *

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




if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = GameSettingsDialog()
    if dialog.exec_() == QDialog.Accepted:
        settings = dialog.selection
        window = TicTacToe(settings["shape"], settings["first_player"])
        window.show()
        sys.exit(app.exec_())
