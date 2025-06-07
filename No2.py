import tkinter as tk
from tkinter import messagebox

class OthelloGame:
    def __init__(self, master):
        self.master = master
        self.master.title("オセロゲーム")
        self.board_size = 8
        self.cell_size = 60
        self.board = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'white'  # 白が先手
        self.canvas = tk.Canvas(self.master, width=self.board_size*self.cell_size, height=self.board_size*self.cell_size)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)
        self.initialize_board()
        self.draw_board()

    def initialize_board(self):
        mid = self.board_size // 2
        self.board[mid-1][mid-1] = 'white'
        self.board[mid][mid] = 'white'
        self.board[mid-1][mid] = 'black'
        self.board[mid][mid-1] = 'black'

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='green')
                if self.board[row][col] != '':
                    color = self.board[row][col]
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill=color)

    def handle_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if self.is_valid_move(row, col, self.current_player):
            self.place_piece(row, col, self.current_player)
            self.current_player = 'white' if self.current_player == 'black' else 'black'
            self.draw_board()
            if not self.has_valid_moves(self.current_player):
             self.end_game()

    def is_valid_move(self, row, col, color):
        if self.board[row][col] != '':
            return False
        opponent = 'white' if color == 'black' else 'black'
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1),  (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            has_opponent_between = False
            while 0 <= r < self.board_size and 0 <= c < self.board_size:
                if self.board[r][c] == opponent:
                    has_opponent_between = True
                elif self.board[r][c] == color:
                    if has_opponent_between:
                        return True
                    else:
                        break
                else:
                    break
                r += dr
                c += dc
        return False

    def place_piece(self, row, col, color):
        self.board[row][col] = color
        opponent = 'white' if color == 'black' else 'black'
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1),  (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            pieces_to_flip = []
            while 0 <= r < self.board_size and 0 <= c < self.board_size:
                if self.board[r][c] == opponent:
                    pieces_to_flip.append((r, c))
                elif self.board[r][c] == color:
                    for rr, cc in pieces_to_flip:
                        self.board[rr][cc] = color
                    break
                else:
                    break
                r += dr
                c += dc

    def has_valid_moves(self, color):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.is_valid_move(row, col, color):
                    return True
        return False

    def end_game(self):
        black_count = sum(row.count('black') for row in self.board)
        white_count = sum(row.count('white') for row in self.board)
        if black_count > white_count:
            winner = "黒"
        elif white_count > black_count:
            winner = "白"
        else:
            winner = "引き分け"
        messagebox.showinfo("ゲーム終了", f"白: {white_count} 石\n黒: {black_count} 石\n勝者: {winner}")
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = OthelloGame(root)
    root.mainloop()
