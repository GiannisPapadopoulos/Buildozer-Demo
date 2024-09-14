import tkinter as tk
from tkinter import messagebox
import random
import copy

ROWS = 6
COLS = 7
DEPTH = 6

nodes = 0

class Connect4:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4")
        
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = 1  # Player 1 starts
        self.buttons = [tk.Button(root, text="Drop", command=lambda col=col: self.player_move(col)) for col in range(COLS)]
        
        self.create_widgets()

    def create_widgets(self):
        for col in range(COLS):
            self.buttons[col].grid(row=0, column=col)

        self.canvas = tk.Canvas(self.root, width=COLS*100, height=ROWS*100, bg="blue")
        self.canvas.grid(row=1, column=0, columnspan=COLS)

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x0 = c * 100 + 10
                y0 = r * 100 + 10
                x1 = (c + 1) * 100 - 10
                y1 = (r + 1) * 100 - 10
                color = "white"
                if self.board[r][c] == 1:
                    color = "red"
                elif self.board[r][c] == 2:
                    color = "yellow"
                self.canvas.create_oval(x0, y0, x1, y1, fill=color)

    def player_move(self, col):
        if self.drop_disc(col, self.current_player):
            if self.check_game_over(self.current_player):
                return
            self.current_player = 2
            self.ai_move()

    def ai_move(self):
        global nodes
        nodes = 0
        col = self.minimax(self.board, DEPTH, True, 2)[1]
        self.drop_disc(col, 2)
        if self.check_game_over(self.current_player):
            return
        self.current_player = 1
        print("nodes searched:" , nodes)

    def drop_disc(self, col, player):
        for row in reversed(range(ROWS)):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                self.draw_board()
                return True
        return False

    def check_game_over(self, player):
        if self.check_win(player):
            messagebox.showinfo("Game Over", f"Player {player} wins!")
            self.reset_board()
            return True
        elif all(self.board[r][c] != 0 for r in range(ROWS) for c in range(COLS)):
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset_board()
            return True
        return False

    def check_win(self, player):
        for r in range(ROWS):
            for c in range(COLS):
                if (c <= COLS - 4 and all(self.board[r][c + i] == player for i in range(4))) or \
                   (r <= ROWS - 4 and all(self.board[r + i][c] == player for i in range(4))) or \
                   (r <= ROWS - 4 and c <= COLS - 4 and all(self.board[r + i][c + i] == player for i in range(4))) or \
                   (r <= ROWS - 4 and c >= 3 and all(self.board[r + i][c - i] == player for i in range(4))):
                    return True
        return False

    def reset_board(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = 1
        self.draw_board()

    def minimax(self, board, depth, maximizing, player):
        global nodes
        nodes += 1
        valid_moves = [col for col in range(COLS) if board[0][col] == 0]
        is_terminal = self.check_terminal_state(board)
        
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_win_state(board, 2):
                    return (100000000, None)
                elif self.check_win_state(board, 1):
                    return (-100000000, None)
                else: 
                    return (0, None)
            else:
                return (self.evaluate_board(board), None)

        if maximizing:
            value = -float('inf')
            best_col = random.choice(valid_moves)
            for col in valid_moves:
                new_board = self.simulate_move(board, col, player)
                new_score = self.minimax(new_board, depth - 1, False, 1)[0]
                if new_score > value:
                    value = new_score
                    best_col = col
            return value, best_col

        else:
            value = float('inf')
            best_col = random.choice(valid_moves)
            for col in valid_moves:
                new_board = self.simulate_move(board, col, player)
                new_score = self.minimax(new_board, depth - 1, True, 2)[0]
                if new_score < value:
                    value = new_score
                    best_col = col
            return value, best_col

    def simulate_move(self, board, col, player):
        temp_board = copy.deepcopy(board)
        for row in reversed(range(ROWS)):
            if temp_board[row][col] == 0:
                temp_board[row][col] = player
                break
        return temp_board

    def check_terminal_state(self, board):
        return self.check_win_state(board, 1) or self.check_win_state(board, 2) or all(board[0][c] != 0 for c in range(COLS))

    def check_win_state(self, board, player):
        for r in range(ROWS):
            for c in range(COLS):
                if (c <= COLS - 4 and all(board[r][c + i] == player for i in range(4))) or \
                   (r <= ROWS - 4 and all(board[r + i][c] == player for i in range(4))) or \
                   (r <= ROWS - 4 and c <= COLS - 4 and all(board[r + i][c + i] == player for i in range(4))) or \
                   (r <= ROWS - 4 and c >= 3 and all(board[r + i][c - i] == player for i in range(4))):
                    return True
        return False

    def evaluate_board(self, board):
        score = 0
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] == 2:  # AI's pieces
                    score += 1
                elif board[r][c] == 1:  # Player's pieces
                    score -= 1
        return score

if __name__ == "__main__":
    root = tk.Tk()
    game = Connect4(root)
    root.mainloop()
