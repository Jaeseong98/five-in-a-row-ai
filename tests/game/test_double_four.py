import ast

from game.board import GameBoard
from game.enum import GameMode
from tests import TestAgent


def test_1(resource_manager):
    black_agent = TestAgent(
        resource_manager.read_text("/double_four/black/1.txt")
    )
    white_agent = TestAgent(
        resource_manager.read_text("/double_four/white/1.txt")
    )
    game_board = GameBoard(
        mode=GameMode.COMPUTER_COMPUTER,
        black_agent=black_agent,
        white_agent=white_agent,
    )
    game_board.start()
    assert set(game_board.unselectable_points) == ast.literal_eval(
        resource_manager.read_text("/double_four/unselectable/1.txt")
    )
