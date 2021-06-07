"""Module with unit tests for the engine"""
from contextlib import nullcontext
import pytest
from src.game_engine.engine import Engine
from src.game_engine.board import (
    Board,
    OutsideBoardException,
    WrongPlayerException,
    NotEnoughArgumentsException,
    PositionTakenException,
    PlayerWonStatus,
)


class TestBoard:
    # pylint: disable=no-self-use
    """Unit tests for the board class"""

    @pytest.mark.parametrize(
        "location,item,expectation",
        [
            ((-1, 0), "x", pytest.raises(OutsideBoardException)),
            ((4, 0), "x", pytest.raises(OutsideBoardException)),
            ((0, 0), "x", nullcontext()),
            ((0, -1), "x", pytest.raises(OutsideBoardException)),
            ((0, 4), "x", pytest.raises(OutsideBoardException)),
            ((2, 2), "x", nullcontext()),
            ((0, 0), "o", pytest.raises(WrongPlayerException)),
            ((0,), "x", pytest.raises(NotEnoughArgumentsException)),
        ],
    )
    def test_add(self, location, item, expectation):
        """Tests if adding entries to the board raises proper exceptions"""
        test = Board()
        with expectation:
            assert test.add(location, item) is None

    def test_wrong_location(self):
        """Tests if trying to add entry in position where another entry exists raises exception"""
        test = Board()
        test.add((0, 0), "x")
        with pytest.raises(PositionTakenException):
            test.add((0, 0), "o")

    @pytest.mark.parametrize(
        "move_set,expectation",
        [
            (
                [
                    ((0, 0), "x"),
                    ((1, 0), "o"),
                    ((0, 1), "x"),
                    ((2, 0), "o"),
                    ((0, 2), "x"),
                ],
                "x",
            ),
            (
                [
                    ((1, 0), "x"),
                    ((0, 0), "o"),
                    ((1, 1), "x"),
                    ((0, 1), "o"),
                    ((1, 2), "x"),
                ],
                "x",
            ),
            (
                [
                    ((2, 0), "x"),
                    ((0, 0), "o"),
                    ((2, 1), "x"),
                    ((0, 1), "o"),
                    ((2, 2), "x"),
                ],
                "x",
            ),
            (
                [
                    ((2, 0), "x"),
                    ((0, 0), "o"),
                    ((1, 2), "x"),
                    ((0, 1), "o"),
                    ((2, 2), "x"),
                    ((0, 2), "o"),
                ],
                "o",
            ),
        ],
    )
    def test_checks(self, move_set, expectation):
        """Check if row checking works properly"""
        test = Board()
        try:
            for move, item in move_set:
                test.add(move, item)
        except PlayerWonStatus as pws:
            assert pws.player is expectation


class TestEngine:
    """Unit test for engine class"""

    # pylint: disable=no-self-use
    @pytest.mark.parametrize(
        "move,expectation",
        [
            ({"coordinates": (0, 1), "symbol": "x"}, nullcontext()),
            (
                {"coordinates": (0, -1), "symbol": "x"},
                pytest.raises(OutsideBoardException),
            ),
            (
                {"coordinates": (0, 1), "symbol": "o"},
                pytest.raises(WrongPlayerException),
            ),
            (
                {"coordinates": (1,), "symbol": "x"},
                pytest.raises(NotEnoughArgumentsException),
            ),
        ],
    )
    def test_move(self, move, expectation):
        """Tests if move raises proper exceptions"""
        instance = Engine()
        with expectation:
            assert instance.make_move(move) is None

    def test_win(self):
        """Tests if winner is reported correctly"""
        instance = Engine()
        move_set = (
            {"coordinates": (0, 1), "symbol": "x"},
            {"coordinates": (1, 2), "symbol": "o"},
            {"coordinates": (1, 1), "symbol": "x"},
            {"coordinates": (0, 2), "symbol": "o"},
            {"coordinates": (2, 1), "symbol": "x"},
        )
        for move in move_set:
            instance.make_move(move)
        assert instance.has_won is True
        assert instance.winner == "x"
