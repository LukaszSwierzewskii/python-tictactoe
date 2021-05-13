"""Board module containing board class and it's exceptions, handles the gameboard logic"""
from numpy import array, int8


class Board:
    """Handles the game board"""

    def __init__(self, starting_player):
        self._board = array([[0] * 3] * 3, dtype=int8)
        self._has_won = False
        self._who_won = None
        self._next_play_by = starting_player

    def add(self, location, item):
        """Adds and item to the location\n
        location should be an array with two numbers in it (numbers from 0 to 2)
        """
        if not item is self._next_play_by:
            # if for some reason wrong player tries to move raise exception
            raise WrongPlayerException()
        if len(location) < 2:
            raise NotEnoughArgumentsException()
        if not (
            location[0] >= 0
            and location[0] <= 2
            and location[1] >= 0
            and location[1] <= 2
        ):
            raise OutsideBoardException()  # if outside the playing field raise exception

        if self._board[location] == 0:
            self._board[location] = item
        else:
            # if position is diffrent from 0, it's busy so raise exception
            raise PositionTakenException()


class BoardException(Exception):
    """Base for board class exceptions"""


class OutsideBoardException(BoardException):
    """Raised if the location is outside the board"""


class WrongPlayerException(BoardException):
    """Raised if the move is made by a wrong player"""


class PositionTakenException(BoardException):
    """Raised if the position is already taken by another item"""


class NotEnoughArgumentsException(BoardException):
    """Raised if the array doesn't have enough arguments to attempt to move"""
