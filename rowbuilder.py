import gamestate

LINE_LENGTH = 4

class RowBuilder:
    """
    Helps with building partial guesses in the ui
    since the GameState only accepts whole guesses
    as input.
    """

    def __init__(self):
        """
        Creates an empty RowBuilder.
        """

        self.reset_row()

    def add_peg(self, peg):
        """
        Adds a peg into the row if the row isn't completed.
        :param peg: The peg to be added
        """
        if self.current_index >= 4:
            return
        self.line[self.current_index] = peg
        self.current_index += 1

    def backspace(self):
        """
        Works like backspace in a regular computer.
        Removes the last peg placed from the row.
        """
        if self.current_index > 0:
            self.current_index -= 1
        self.line[self.current_index] = gamestate.PlayerPeg.empty

    def reset_row(self):
        """
        Sets the RowBuilder back into the (empty) starting position.
        """

        self.line = [0] * LINE_LENGTH
        self.current_index = 0

    def is_line_finished(self):
        """
        :return: True, if the row is filled with pegs. Otherwise False.
        """
        return self.line[-1] != gamestate.PlayerPeg.empty
