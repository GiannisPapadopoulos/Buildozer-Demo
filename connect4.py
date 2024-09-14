import tkinter as tk
from tkinter import messagebox

ROWS = 6
COLS = 7

class Connect4:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4")
        
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = 1  # Player 1 starts
        self.buttons = [tk.Button(root, text="Drop", command=lambda col=col: self.drop_disc(col)) for col in range(COLS)]
        
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

    def drop_disc(self, col):
        for row in reversed(range(ROWS)):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.draw_board()
                if self.check_win(row, col):
                    messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                    self.reset_board()
                elif all(self.board[r][c] != 0 for r in range(ROWS) for c in range(COLS)):
                    messagebox.showinfo("Game Over", "It's a draw!")
                    self.reset_board()
                else:
                    self.current_player = 3 - self.current_player  # Switch player (1 -> 2, 2 -> 1)
                return
        messagebox.showwarning("Invalid Move", "Column is full!")

    def check_win(self, row, col):
        def check_direction(delta_row, delta_col):
            count = 0
            r, c = row, col
            while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == self.current_player:
                count += 1
                r += delta_row
                c += delta_col
            return count

        for delta_row, delta_col in [(0, 1), (1, 0), (1, 1), (1, -1)]:
            total = check_direction(delta_row, delta_col) + check_direction(-delta_row, -delta_col) - 1
            if total >= 4:
                return True
        return False

    def reset_board(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = 1
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = Connect4(root)
    root.mainloop()
