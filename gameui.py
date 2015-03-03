from tkinter import *
from tkinter.ttk import *
import gamestate

from rowbuilder import RowBuilder


PLAYER_PEG_DIAMETER = 30
KEY_PEG_DIAMETER = 12

class GameUI:
    """
    The whole UI in which the game (not including the difficulty selector) runs.
    """

    def __init__(self, main, number_of_guesses, game):
        """
        :param main: The main class.
        :param number_of_guesses: How many guesses the player can make.
        :param game: The current GameState-object.
        """

        self.gamestate = game

        self.main = main
        self.root = Tk()
        self.root.geometry("400x700+300+300")

        self.root.resizable(width=FALSE, height=FALSE)

        self.frame = GameFrame(self, self.root, number_of_guesses)
        self.root.mainloop()

    def open_the_new_game_window(self):
        """
        Switches the current UI to DifficultySelect where
        the player can start a new game.
        """
        self.root.destroy()
        self.main.open_difficulty_select_window()


class GameFrame(Frame):
    """
    The frame including the canvas in which the game is drawn
    and the
    """

    def __init__(self, parent_ui, parent_window, number_of_guesses):
        """
        :param parent_ui: GameUI-instance.
        :param parent_window: The window which holds this frame.
        :param number_of_guesses: The number of times the player is allowed to guess.
        """
        Frame.__init__(self, parent_window)

        self.parent_ui = parent_ui

        self.number_of_guesses = number_of_guesses

        self.parent = parent_window

        self.blue_image = PhotoImage(file="textures/blue.gif")
        self.white_image = PhotoImage(file="textures/white.gif")
        self.purple_image = PhotoImage(file="textures/purple.gif")
        self.yellow_image = PhotoImage(file="textures/yellow.gif")
        self.red_image = PhotoImage(file="textures/red.gif")
        self.cyan_image = PhotoImage(file="textures/cyan.gif")

        self.create_frame()


    def create_frame(self):
        """
        Creates the frame and the widgets.
        """

        self.parent.title("Mastermind")
        self.style = Style()
        self.style.theme_use("default")

        self.top_frame = Frame(self, relief=RAISED, borderwidth=1)
        self.top_frame.pack(fill=BOTH)

        self.game_graphics = GameGraphics(self, self.number_of_guesses)

        self.row_builder = self.game_graphics.row_builder

        self.pack(fill=BOTH, expand=1)

        self.__create_buttons()


    def __create_buttons(self):
        """
        Creates the buttons into the GameFrame.
        """

        blue_button = self.__create_color_button(self.blue_image, gamestate.PlayerPeg.blue)
        white_button = self.__create_color_button(self.white_image, gamestate.PlayerPeg.white)
        red_button = self.__create_color_button(self.red_image, gamestate.PlayerPeg.red)
        cyan_button = self.__create_color_button(self.cyan_image, gamestate.PlayerPeg.cyan)
        yellow_button = self.__create_color_button(self.yellow_image, gamestate.PlayerPeg.yellow)
        purple_button = self.__create_color_button(self.purple_image, gamestate.PlayerPeg.purple)

        horizontal_padding = 3
        backspace_button = Button(self, text="<--", command=self.__on_backspace).pack(side=LEFT, padx=horizontal_padding, pady=5)
        submit_button = Button(self, text="Guess", command=self.__on_submit).pack(side=LEFT, padx=horizontal_padding, pady=5)

        new_game_button = Button(self.top_frame, text="New game", width=50, command=self.__on_new_game).pack()

    def __create_color_button(self, button_image, peg):
        """
        Creates a button that can be used to select a peg to be placed.
        :param button_image: The image of the button.
        :param peg: The peg this button will place.
        """

        horizontal_padding = 3

        color_button = Button(self, image=button_image, command=lambda: self.__on_colored_button(peg))
        color_button.pack(side=LEFT, padx=horizontal_padding, pady=5)

        return color_button

    def __on_new_game(self):
        self.parent_ui.open_the_new_game_window()

    def __on_backspace(self):
        if self.parent_ui.gamestate.gameFinished:
            return
        self.row_builder.backspace()
        self.game_graphics.update_current_player_peg_row_graphics()

    def __on_submit(self):

        game = self.parent_ui.gamestate
        if not self.row_builder.is_line_finished() or game.gameFinished:
            return

        game.take_turn(self.row_builder.line)

        previous_turn = game.turnsPlayed - 1
        self.game_graphics.update_key_pegs_of_row(previous_turn, game.key_pegs[previous_turn])

        if game.gameFinished:
            self.game_graphics.reveal_answer(game.code)
            return

        self.game_graphics.to_next_row()

    def __on_colored_button(self, peg):
        self.row_builder.add_peg(peg)
        self.game_graphics.update_current_player_peg_row_graphics()

class GameGraphics():
    """
    Handles the graphical aspects of the game.
    """

    def __init__(self, parent_frame, number_of_guesses):
        """
        :param parent_frame: The frame in which the canvas is placed.
        :param number_of_guesses: How many times the player can guess.
        """

        self.number_of_guesses = number_of_guesses

        self.canvas = Canvas(parent_frame, relief=RAISED, borderwidth=3)

        self.canvas.pack(fill=BOTH, expand=1)


        self.player_peg_graphics = []
        self.key_peg_graphics = []

        self.current_row = 0
        self.row_builder = RowBuilder()

        number_of_pegs = 4
        empty_rows = [[gamestate.PlayerPeg.empty] * number_of_pegs for i in range(self.number_of_guesses)]
        self.create_all_player_pegs(empty_rows)



    def reveal_answer(self, answer):
        """
        Shows the correct answer
        :param answer: The correct answer as a 4-list
        """
        distance_from_left_border = PLAYER_PEG_DIAMETER
        text = self.canvas.create_text(distance_from_left_border, self.canvas.winfo_height()-100, text="Code:", font=("arial", 15), anchor="nw")
        self.create_player_row(self.canvas.winfo_height()-65, answer)

    def to_next_row(self):
        """
        Make the graphics handle the next row, if there is one.
        """
        last_row_index = self.number_of_guesses - 1
        if self.current_row < last_row_index:
            self.current_row += 1
            self.row_builder.reset_row()

    def create_all_player_pegs(self, guesses):
        """
        Create all the oval-objects representing pegs.
        :param guesses: Guesses made as a number_of_guesses x 4 list.
        """

        min_y = 30
        padding_height = 10

        for i in range(len(guesses)):
            y = min_y + PLAYER_PEG_DIAMETER * i + padding_height * i

            self.create_player_row(y, guesses[i])
            self.create_key_peg_block(y+2) # The +2 is for better aligning

    def create_player_row(self, top_y, pegs):
        """
        Creates the graphics of a row of player pegs.
        :param top_y: The top y-coordinate of the row.
        :param pegs: Pegs in the row as a 4-list.
        """

        padding_width = 10
        distance_from_border = 30

        self.guesses_right_border = distance_from_border + PLAYER_PEG_DIAMETER * 4

        row = []

        for i in range(4):

            x = distance_from_border + PLAYER_PEG_DIAMETER * i + padding_width * i

            peg_color = self.get_peg_color_code(pegs[i])
            peg_graphic = self.canvas.create_oval(x, top_y, x + PLAYER_PEG_DIAMETER, top_y + PLAYER_PEG_DIAMETER, fill=peg_color)

            row.append(peg_graphic)

        self.player_peg_graphics.append(row)

    def create_key_peg_block(self, top_y):
        """
        Creates the graphics of a key peg square.
        :param top_y: The top y-coordinate of the block.
        """
        padding = 3
        distance_to_guesses = PLAYER_PEG_DIAMETER * 2

        top_left_x = self.guesses_right_border + distance_to_guesses

        left_x = top_left_x
        right_x = top_left_x + KEY_PEG_DIAMETER + padding
        bottom_y = top_y + KEY_PEG_DIAMETER + padding

        top_left_peg = self.create_key_peg(left_x, top_y)
        top_right_peg = self.create_key_peg(right_x, top_y)
        bottom_left_peg = self.create_key_peg(left_x, bottom_y)
        bottom_right_peg = self.create_key_peg(right_x, bottom_y)

        block = [top_left_peg, top_right_peg, bottom_left_peg, bottom_right_peg]
        self.key_peg_graphics.append(block)

    def create_key_peg(self, top_left_x, top_left_y):
        """
        Creates the graphics of a single key peg.
        :param top_left_x: Coordinate.
        :param top_left_y: Coordinate.
        """

        color = self.get_peg_color_code(gamestate.KeyPeg.empty)
        return self.canvas.create_oval(top_left_x, top_left_y,
                                       top_left_x + KEY_PEG_DIAMETER, top_left_y + KEY_PEG_DIAMETER)

    def update_key_pegs_of_row(self, row, key_peg_amounts):
        """
        Update the key peg graphics of a single row.
        :param row: The row which should be updated
        :key_peg_amounts A KeyPegAmount-object defined in gamestate.py
        that specifies which key pegs should be placed.
        """

        key_peg_block = self.key_peg_graphics[row]
        red_pegs = key_peg_amounts.red_pegs
        white_pegs = key_peg_amounts.white_pegs

        for i in range(red_pegs):
            peg_graphic_id = key_peg_block[i]
            color = self.get_peg_color_code(gamestate.KeyPeg.red)

            self.change_peg_color(peg_graphic_id, color)

        for i in range(red_pegs, red_pegs + white_pegs):
            peg_graphic_id = key_peg_block[i]
            color =  self.get_peg_color_code(gamestate.KeyPeg.white)

            self.change_peg_color(peg_graphic_id, color)

        for i in range(red_pegs + white_pegs, 4):
            peg_graphic_id = key_peg_block[i]
            color =  self.get_peg_color_code(gamestate.KeyPeg.empty)

            self.change_peg_color(peg_graphic_id, color)

    def update_current_player_peg_row_graphics(self):
        """
        Update the graphics of the current single player peg row.
        """
        for i in range(len(self.row_builder.line)):

            peg_graphic_id = self.player_peg_graphics[self.current_row][i]
            color = self.get_peg_color_code(self.row_builder.line[i])

            self.change_peg_color(peg_graphic_id, color)

    def change_peg_color(self, peg_graphic_id, color):
        """
        Change the color of a single peg.
        :param peg_graphic_id: The id of the peg graphic in the canvas.
        :param color: The new color
        """
        self.canvas.itemconfig(peg_graphic_id, fill=color)



    @staticmethod
    def get_peg_color_code(peg):
        """
        Get the color corresponding to the peg type.
        :param peg: Peg type.
        """
        if peg == gamestate.PlayerPeg.cyan:
            return "cyan"
        elif peg == gamestate.PlayerPeg.blue:
            return "blue"
        elif peg == gamestate.PlayerPeg.purple:
            return "purple"
        elif peg == gamestate.PlayerPeg.red:
            return "red"
        elif peg == gamestate.PlayerPeg.white:
            return "ivory"
        elif peg == gamestate.PlayerPeg.yellow:
            return "yellow"
        elif peg == gamestate.PlayerPeg.empty:
            return "#404040"