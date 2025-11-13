import tkinter as tk
from tkinter import messagebox
import random

# Sudoku logic
def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    if num in [board[i][col] for i in range(9)]:
        return False
    start_row, start_col = 3*(row//3), 3*(col//3)
    for i in range(3):
        for j in range(3):
            if board[start_row+i][start_col+j] == num:
                return False
    return True

def solve(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve(board):
                            return True
                        board[i][j] = 0
                return False
    return True

def generate_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    for k in range(0, 9, 3):
        nums = random.sample(range(1, 10), 9)
        for i in range(3):
            for j in range(3):
                board[k+i][k+j] = nums.pop()
    solution = [row[:] for row in board]  # copy for solution
    solve(solution)
    puzzle = [row[:] for row in solution]
    # Remove some numbers to create puzzle
    for _ in range(random.randint(40, 55)):
        i, j = random.randint(0, 8), random.randint(0, 8)
        puzzle[i][j] = 0
    return puzzle, solution

# GUI
class SudokuUI:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku")
        self.puzzle, self.solution = generate_board()
        self.entries = [[None]*9 for _ in range(9)]

        # Canvas for grid lines
        self.canvas = tk.Canvas(master, width=450, height=450)
        self.canvas.grid(row=0, column=0, rowspan=9, columnspan=9)

        # Draw thicker 3x3 borders
        for i in range(10):
            width = 3 if i % 3 == 0 else 1
            self.canvas.create_line(50*i, 0, 50*i, 450, width=width)
            self.canvas.create_line(0, 50*i, 450, 50*i, width=width)

        # Place Entry widgets
        for i in range(9):
            for j in range(9):
                e = tk.Entry(master, width=2, font=('Arial', 24), justify='center')
                e.place(x=j*50 + 5, y=i*50 + 5, width=40, height=40)

                if self.puzzle[i][j] != 0:
                    e.insert(0, str(self.puzzle[i][j]))
                    e.config(state='disabled', disabledforeground='black', disabledbackground='#DDDDDD')
                else:
                    e.bind('<KeyRelease>', lambda event, x=i, y=j: self.validate_input(event, x, y))

                self.entries[i][j] = e

        self.check_button = tk.Button(master, text="Check", command=self.check)
        self.check_button.place(x=180, y=460)

    def validate_input(self, event, row, col):
        entry = self.entries[row][col]
        val = entry.get()

        # Only allow 1 digit 1-9
        if len(val) > 1 or (val and (not val.isdigit() or val == '0')):
            entry.delete(0, tk.END)
            val = ''

        # Highlight instantly
        if val:
            if int(val) == self.solution[row][col]:
                entry.config(bg='lightgreen')
            else:
                entry.config(bg='red')
        else:
            entry.config(bg='white')

    def check(self):
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                if val == "":
                    messagebox.showinfo("Sudoku", "Not complete yet!")
                    return
                if int(val) != self.solution[i][j]:
                    messagebox.showerror("Sudoku", "Incorrect solution!")
                    return
        messagebox.showinfo("Sudoku", "Congratulations! You solved it!")

root = tk.Tk()
root.geometry("450x500")
app = SudokuUI(root)
root.mainloop()
