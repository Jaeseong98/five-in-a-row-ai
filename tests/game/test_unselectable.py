import ast

from game.board import GameBoard
from game.enum import GameMode
from tests import TestAgent


def test_double_three_1(resource_manager):
    black_agent = TestAgent(
        resource_manager.read_text("/black/double_three_1.txt")
    )
    white_agent = TestAgent(
        resource_manager.read_text("/white/double_three_1.txt")
    )
    game_board = GameBoard(
        mode=GameMode.COMPUTER_COMPUTER,
        black_agent=black_agent,
        white_agent=white_agent,
    )
    game_board.start()
    assert set(game_board.unselectable_points) == ast.literal_eval(
        resource_manager.read_text("/unselectable/double_three_1.txt")
    )


def test_double_three_2(resource_manager):
    black_agent = TestAgent(
        resource_manager.read_text("/black/double_three_2.txt")
    )
    white_agent = TestAgent(
        resource_manager.read_text("/white/double_three_2.txt")
    )
    game_board = GameBoard(
        mode=GameMode.COMPUTER_COMPUTER,
        black_agent=black_agent,
        white_agent=white_agent,
    )
    game_board.start()
    assert set(game_board.unselectable_points) == set(ast.literal_eval(
        resource_manager.read_text("/unselectable/double_three_2.txt")
    ))


def test_double_three_3(resource_manager):
    black_agent = TestAgent(
        resource_manager.read_text("/black/double_three_3.txt")
    )
    white_agent = TestAgent(
        resource_manager.read_text("/white/double_three_3.txt")
    )
    game_board = GameBoard(
        mode=GameMode.COMPUTER_COMPUTER,
        black_agent=black_agent,
        white_agent=white_agent,
    )
    game_board.start()
    assert set(game_board.unselectable_points) == set(ast.literal_eval(
        resource_manager.read_text("/unselectable/double_three_3.txt")
    ))


def test_double_three_4(resource_manager):
    black_agent = TestAgent(
        resource_manager.read_text("/black/double_three_4.txt")
    )
    white_agent = TestAgent(
        resource_manager.read_text("/white/double_three_4.txt")
    )
    game_board = GameBoard(
        mode=GameMode.COMPUTER_COMPUTER,
        black_agent=black_agent,
        white_agent=white_agent,
    )
    game_board.start()
    assert set(game_board.unselectable_points) == set(ast.literal_eval(
        resource_manager.read_text("/unselectable/double_three_4.txt")
    ))


def test_double_three_5(resource_manager):
    black_agent = TestAgent(
        resource_manager.read_text("/black/double_three_5.txt")
    )
    white_agent = TestAgent(
        resource_manager.read_text("/white/double_three_5.txt")
    )
    game_board = GameBoard(
        mode=GameMode.COMPUTER_COMPUTER,
        black_agent=black_agent,
        white_agent=white_agent,
    )
    game_board.start()
    assert set(game_board.unselectable_points) == set(ast.literal_eval(
        resource_manager.read_text("/unselectable/double_three_5.txt")
    ))


def test_double_four_1(resource_manager):
    black_agent = TestAgent(
        resource_manager.read_text("/black/double_four_1.txt")
    )
    white_agent = TestAgent(
        resource_manager.read_text("/white/double_four_1.txt")
    )
    game_board = GameBoard(
        mode=GameMode.COMPUTER_COMPUTER,
        black_agent=black_agent,
        white_agent=white_agent,
    )
    game_board.start()
    assert set(game_board.unselectable_points) == ast.literal_eval(
        resource_manager.read_text("/unselectable/double_four_1.txt")
    )
