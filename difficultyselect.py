from tkinter import *

class DifficultySelectWindow(Frame):
    def __init__(self, main):

        self.main = main

        self.root = Tk()
        self.root.geometry("200x210+300+300")

        self.root.resizable(width=FALSE, height=FALSE)

        Frame.__init__(self, self.root)

        self.root.title("Select difficulty")

        Label(self, text="Difficulty:").pack(pady=10)
        button_width = 18
        Button(self, text="Easy (12 guesses)", width=button_width,
               command=lambda: self.select_difficulty(Difficulty.easy)).pack(pady=5)

        Button(self, text="Medium (10 guesses)", width=button_width,
               command=lambda: self.select_difficulty(Difficulty.medium)).pack(pady=5)

        Button(self, text="Hard (8 guesses)", width=button_width,
               command=lambda: self.select_difficulty(Difficulty.hard)).pack(pady=5)

        Button(self, text="I work for RAY (1 guess)", width=button_width,
               command=lambda: self.select_difficulty(Difficulty.ray)).pack(pady=5)

        self.pack(fill=BOTH, expand=1)

        self.root.mainloop()

    def select_difficulty(self, difficulty):
        self.root.destroy()
        self.main.start_game(difficulty)


class Difficulty:
    """
    The number of turns to break the code.
    """
    easy = 12
    medium = 10
    hard = 8
    ray = 1