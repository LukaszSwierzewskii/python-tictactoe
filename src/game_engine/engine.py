"""Engine module containing all classes and functions, handles the game"""

from .board import Board, DrawStatus, PlayerWonStatus


class Engine:
    """Instance of the engine handling the game"""

    def __init__(self):
        self.board = Board()
        self.has_won = False
        self.winner = None

    def make_move(self, move):
        """Tries to make a move\n
        move:   should be a dictionary with 'symbol' being either 'x' or 'o'
        and coordinates being a tuple with two elements\n
        example {coordiantes:(0,0),symbol:'x'}"""
        if self.has_won:
            pass
        try:
            self.board.add(move["coordinates"], move["symbol"])
        except PlayerWonStatus as won:
            self.has_won = True
            self.winner = won.player
        except DrawStatus:
            self.has_won = True
            self.winner = "DRAW"
        # all other exceptions should be delt with higher up

    def get_board_copy(self):
        """Returns copy of the game board for display"""
        return self.board.get_copy()

    def restart(self):
        """Restarts the game\n
        To be used for a new game or in case of errors"""
        self.board.clear()
        self.has_won = False
        self.winner = None


instance = Engine()
