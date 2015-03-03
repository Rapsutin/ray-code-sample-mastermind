import gamestate

LINE_LENGTH = 4

class RowBuilder:

    def __init__(self):
        self.reset_row()

    def add_peg(self, peg):
        if self.current_index >= 4:
            return
        self.line[self.current_index] = peg
        self.current_index += 1

    def backspace(self):
        if self.current_index > 0:
            self.current_index -= 1
        self.line[self.current_index] = gamestate.PlayerPeg.empty

    def reset_row(self):
        self.line = [0] * LINE_LENGTH
        self.current_index = 0

    def is_line_finished(self):
        return self.line[-1] != gamestate.PlayerPeg.empty
