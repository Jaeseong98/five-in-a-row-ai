import pytest

from game.board import GameBoard
from game.enum import GameMode


@pytest.fixture(scope="session")
def game_board():
    return GameBoard(GameMode.TEST)