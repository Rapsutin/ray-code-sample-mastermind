from tkinter import *

class DifficultySelectWindow(Frame):
    """
    The first window in the game.
    Provides difficulty selection and starts a new game.
    """
    def __init__(self, main):

        self.main = main

        self.root = Tk()
        self.root.geometry("200x210+300+300")

        self.root.resizable(width=FALSE, height=FALSE)

        Frame.__init__(self, self.root)

        self.init_UI()

        self.pack(fill=BOTH, expand=1)

        self.root.mainloop()

    def init_UI(self):
        """
        Creates the widgets of the window.
        """
        self.root.title("Select difficulty")
        Label(self, text="Difficulty:").pack(pady=10)
        button_width = 18

        Button(self, text="Easy (12 guesses)", width=button_width,
               command=lambda: self.start_game(Difficulty.easy)).pack(pady=5)

        Button(self, text="Medium (10 guesses)", width=button_width,
               command=lambda: self.start_game(Difficulty.medium)).pack(pady=5)

        Button(self, text="Hard (8 guesses)", width=button_width,
               command=lambda: self.start_game(Difficulty.hard)).pack(pady=5)

        Button(self, text="I work for RAY (1 guess)", width=button_width,
               command=lambda: self.start_game(Difficulty.ray)).pack(pady=5)

    def start_game(self, difficulty):
        """
        Starts the game.
        :param difficulty: How many guesses the player can do.
        """

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