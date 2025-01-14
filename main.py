import sys
from gameSettings import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = GameSettingsDialog()
    
    if dialog.exec_() == QDialog.Accepted:
        settings = dialog.selection
        
        game = TicTacToe(settings["shape"], settings["first_player"])
        game.show()
        
        sys.exit(app.exec_())
