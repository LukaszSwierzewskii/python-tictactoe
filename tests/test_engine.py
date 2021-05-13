"""Module with unit tests for the engine"""
from contextlib import nullcontext
import pytest
from src.game_engine.board import (
    Board,
    OutsideBoardException,
    WrongPlayerException,
    NotEnoughArgumentsException,
)


class TestBoard:
    """Unit tests for the board class"""

    @pytest.mark.parametrize(
        "location,item,expectation",
        [
            ((-1, 0), 1, pytest.raises(OutsideBoardException)),
            ((4, 0), 1, pytest.raises(OutsideBoardException)),
            ((0, 0), 1, nullcontext()),
            ((0, -1), 1, pytest.raises(OutsideBoardException)),
            ((0, 4), 1, pytest.raises(OutsideBoardException)),
            ((2, 2), 1, nullcontext()),
            ((0, 0), -1, pytest.raises(WrongPlayerException)),
            ((0,), 1, pytest.raises(NotEnoughArgumentsException)),
        ],
    )
    def test_add(self, location, item, expectation):
        """Tests if adding entries to the board raises proper exceptions"""
        test = Board(1)
        with expectation:
            assert test.add(location, item) is None
