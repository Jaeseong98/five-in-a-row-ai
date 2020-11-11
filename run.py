import click

from game.board import GameBoard
from game.enum import GameMode


@click.command()
@click.option('--mode', default='HUMAN_HUMAN', help='')
def run(mode):
    mode = GameMode(mode)
    gameboard = GameBoard(mode)
    gameboard.start()


if __name__ == "__main__":
    run()
