from enum import Enum
import random



class GameState:
    """
    Keeps track of the situation of the game.
    The UI-functions should be handled elsewhere.
    """

    def __init__(self, number_of_rows):
        """
        :param number_of_rows: The number of turns for the player to break the code. (difficulty)
        """

        self.turnsPlayed = 0
        self.maxTurns = number_of_rows
        self.playerGuesses = [[PlayerPeg.empty]*number_of_rows for i in range(number_of_rows)]  # Stores the player's guesses.
        self.key_pegs = []  # 2d array containing the current key peg amounts (KeyPegAmount) for each row.

        self.gameFinished = False
        self.gameWon = False

        self.code = self.__generate_code()


    def __generate_code(self):
        """
        Generates the code for the player to solve.
        """
        code = []
        for i in range(4):
            code.append(random.randint(1, 6))
        return code


    def take_turn(self, guess):
        """
        Moves the game forward by one turn.
        :param guess: The guess of the player as a 4-sequence.
        """
        if self.gameFinished: return  # The game has ended already so don't take any more turns.

        self.__record_guess(guess)

        self.turnsPlayed += 1

        final_turn_taken = self.turnsPlayed == self.maxTurns
        if final_turn_taken:
            self.gameFinished = True

    def __record_guess(self, guess):
        """
        Adds a player guess into the game state.
        :param guess: The guessed pegs as a 4-list
        """
        self.playerGuesses[self.turnsPlayed] = guess  # Record the newly played guess
        self.__evaluate_new_guess(guess)  # and evaluate it.

    def __evaluate_new_guess(self, guess):
        """
        Evaluates the guess and places the appropriate
        key peg amounts into self.key_pegs.
        :parameter guess: The guessed pegs as a 4-list
        """

        correct_guesses = 0
        correct_colors = 0

        for i in range(4):
            peg = guess[i]

            if peg == self.code[i]:
                correct_guesses += 1

            elif peg in self.code:
                correct_colors += 1

        self.key_pegs.append(KeyPegAmount(correct_guesses, correct_colors))

        if correct_guesses == 4:
            self.gameWon = True
            self.gameFinished = True

class KeyPegAmount:
    def __init__(self, reds, whites):
        self.red_pegs = reds
        self.white_pegs = whites

class PlayerPeg:
    """
    Enum for the pegs the player places.
    The numerical values are just for identification
    """
    empty = 0
    cyan = 6
    red = 2
    purple = 3
    yellow = 4
    blue = 5
    white = 1

class KeyPeg:
    """
    Enum for the key pegs (the smaller pegs)
    The numerical values are just for identification
    """
    empty = 0
    white = 1
    red = 2



