import numpy as np
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

ROW_COUNT = 6
COLUMN_COUNT = 7

class Connect4App(App):
    def build(self):
        self.board = self.create_board()
        self.turn = 0  # 0 -> Player 1, 1 -> AI
        layout = BoxLayout(orientation='vertical')
        
        # Top layout to show game status
        self.status_label = Label(text="Player 1's Turn")
        layout.add_widget(self.status_label)
        
        # Grid layout for the Connect 4 board
        self.grid = GridLayout(cols=COLUMN_COUNT, rows=ROW_COUNT)
        self.buttons = []

        for row in range(ROW_COUNT):
            row_buttons = []
            for col in range(COLUMN_COUNT):
                button = Button(text="", font_size=32, on_press=self.button_pressed)
                row_buttons.append(button)
                self.grid.add_widget(button)
            self.buttons.append(row_buttons)

        layout.add_widget(self.grid)
        return layout

    def create_board(self):
        return np.zeros((ROW_COUNT, COLUMN_COUNT))

    def button_pressed(self, instance):
        # Determine which button was pressed
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                if self.buttons[row][col] == instance:
                    if self.is_valid_location(col):
                        row = self.get_next_open_row(col)
                        self.drop_piece(row, col, 1 if self.turn == 0 else 2)
                        self.update_button(row, col)

                        if self.winning_move(1 if self.turn == 0 else 2):
                            self.show_winner_popup(f"Player {1 if self.turn == 0 else 2} wins!")
                            return

                        self.turn = (self.turn + 1) % 2
                        self.status_label.text = f"Player {1 if self.turn == 0 else 2}'s Turn"
                        break

    def update_button(self, row, col):
        # Update the button text based on the piece
        piece = self.board[row][col]
        if piece == 1:
            self.buttons[row][col].text = "R"  # Red for Player 1
        elif piece == 2:
            self.buttons[row][col].text = "Y"  # Yellow for Player 2
        self.buttons[row][col].disabled = True

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def winning_move(self, piece):
        # Check horizontal locations
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece and self.board[r][c + 3] == piece:
                    return True

        # Check vertical locations
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece and self.board[r + 3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][c + 2] == piece and self.board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][c + 2] == piece and self.board[r - 3][c + 3] == piece:
                    return True

    def show_winner_popup(self, message):
        # Display a popup when a player wins
        popup_layout = BoxLayout(orientation='vertical')
        popup_label = Label(text=message)
        popup_button = Button(text='Close', size_hint=(1, 0.3), on_press=self.reset_game)
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)

        popup = Popup(title='Game Over', content=popup_layout, size_hint=(0.6, 0.4))
        popup.open()

    def reset_game(self, instance):
        # Reset the game after a win
        self.board = self.create_board()
        self.turn = 0
        self.status_label.text = "Player 1's Turn"
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                self.buttons[row][col].text = ""
                self.buttons[row][col].disabled = False
        instance.parent.parent.dismiss()

if __name__ == '__main__':
    Connect4App().run()
