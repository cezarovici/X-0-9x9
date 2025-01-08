class Minimax:
    @staticmethod
    def find_best_move(board, ai_player):
        """Căutăm cea mai bună mutare pe tabla principală 3x3."""
        best_move = None
        best_score = -float('inf')  # Începe cu cel mai mic scor posibil

        for i in range(3):
            for j in range(3):
                if board[i][j] == "":  # Verificăm dacă celula este goală
                    board[i][j] = ai_player  # Plasăm temporar piesa AI
                    score = Minimax.minimax(board, 0, False, ai_player, -float('inf'), float('inf'))
                    board[i][j] = ""  # Anulăm mutarea

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)  # Salvăm mutarea cu cel mai bun scor

        return best_move

    @staticmethod
    def minimax(board, depth, is_maximizing_player, ai_player, alpha, beta):
        """Algoritmul Minimax cu tăiere alfa-beta."""
        winner = Minimax.check_winner(board, ai_player)
        if winner == ai_player:
            return 1  # Scor maxim pentru AI
        elif winner == ("O" if ai_player == "X" else "X"):
            return -1  # Scor minim pentru AI (când câștigă inamicii)
        elif all(board[i][j] != "" for i in range(3) for j in range(3)):
            return 0  # Remiză

        if is_maximizing_player:
            max_eval = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = ai_player
                        eval = Minimax.minimax(board, depth + 1, False, ai_player, alpha, beta)
                        board[i][j] = ""
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break  # Tăiere beta
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = "O" if ai_player == "X" else "X"
                        eval = Minimax.minimax(board, depth + 1, True, ai_player, alpha, beta)
                        board[i][j] = ""
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break  # Tăiere alfa
            return min_eval

    @staticmethod
    def check_winner(board, ai_player):
        """Verifică dacă există un câștigător pe tabla 3x3."""
        for i in range(3):
            # Verifică liniile
            if board[i][0] == board[i][1] == board[i][2] != "":
                return board[i][0]
            # Verifică coloanele
            if board[0][i] == board[1][i] == board[2][i] != "":
                return board[0][i]

        # Verifică diagonalele
        if board[0][0] == board[1][1] == board[2][2] != "":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != "":
            return board[0][2]

        return None  # Dacă nu există câștigător
