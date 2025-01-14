from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QPushButton,
    QWidget,
)
from PyQt5.QtGui import QFont


class SmallBoard(QWidget):
    def __init__(self, parent, row, col):
        super().__init__()
        self.parent = parent #cale de notificare catre tabela mare
        self.winner = None #parametru ce retine castigatorul pentru o tabela mica
        self.row = row #randul tabelei mici in tabela mare
        self.col = col #coloana tabelei mici in tabela mare
        self.board = [["" for _ in range(3)] for _ in range(3)] #matricea de status a tablei mici ce va contine x sau 0 
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.buttons = [] #matrice de butoane pentru actiune si marcare/afisare cu simbolul fiecarui player

        #populare cu butoane a matricei "buttons" si setarea acestora
        for i in range(3):
            row_buttons = [] #creare linie goala initial
            for j in range(3):
                button = QPushButton("")
                button.setFont(QFont("Arial", 14))
                button.setFixedSize(40, 40)
                button.clicked.connect(lambda _, r=i, c=j: self.make_user_move(r, c)) #adaugam evenimentul de click pe buton ce face legaruta l;a make_move cu parametrii pentru row si col din matricea de status
                self.layout.addWidget(button, i, j) #adaugare widget de buton
                row_buttons.append(button) #adaugare buton la linie noua
            self.buttons.append(row_buttons) #adaugarea liniei noi la matrice de butoane
    
    def make_user_move(self, row, col):
        if self.parent.active_board is not None: #daca avem o tabela activa, adica pe care trebuie sa marcam obligatoriu
            active_row, active_col = self.parent.active_board #coorodnatele tabelei mici active din tabela mare
            if self.parent.main_board[active_row][active_col].winner: #daca tablea mica activa este castigata
                if not self.parent.main_board[row][col].winner: #si daca se incearca marcarea in alta tabela necastigata se face lucrul asta.
                    return self.parent.main_board[row][col].make_move(row, col) 
                else:
                    print("Mutare invalidă! Tabela mică este deja câștigată.")
                    return False
            elif (self.row, self.col) != (active_row, active_col): #daca mutarea nu e in tabela activa
                print("Mutare invalidă! Trebuie să pui simbolul în tabla mică corespunzătoare.")
                return False

        #mutarea se face 
        return self.make_move(row, col)

    
    def make_move(self, row, col):
        # verifica dacă e plina tabela
        if self.board[row][col] != "":
            return False

        # se face marcarea
        self.board[row][col] = self.parent.current_player
        self.buttons[row][col].setText(self.parent.current_player)

        # verificam daca este vreun castigator pe tabela mcia
        if self.check_winner():
            self.winner = self.parent.current_player
            self.parent.update_main_board(self.row, self.col, self.winner)

        # actualizam 
        self.parent.update_active_board(row, col)

        self.parent.switch_player()
        return True


    #metoda de verificare daca exista vreun castigfator pe tabela mica 
    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        return False