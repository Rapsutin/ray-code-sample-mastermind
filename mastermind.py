from gameui import *
from gamestate import *
from difficultyselect import *



class Main:
    def __init__(self):
        self.open_difficulty_select_window()

    def open_difficulty_select_window(self):
        DifficultySelectWindow(self)

    def start_game(self, difficulty):
        game_state = GameState(difficulty)
        ui = GameUI(self, difficulty, game_state)

main = Main()