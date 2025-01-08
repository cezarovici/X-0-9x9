from PyQt5.QtWidgets import QApplication
from tictactoe import TicTacToe

import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Configurăm jucătorul și ordinea de start
    shape = "X"  # Poate fi configurat dintr-un meniu ulterior
    first_player = True  # Jucătorul uman începe
    
    window = TicTacToe(shape, first_player)
    window.show()
    
    sys.exit(app.exec_())