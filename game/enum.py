import enum

class GameMode(enum.Enum):
    HUMAN_HUMAN = "HUMAN_HUMAN"
    HUMAN_COMPUTER = "HUMAN_COMPUTER"
    COMPUTER_HUMAN = "COMPUTER_HUMAN"
    COMPUTER_COMPUTER = "COMPUTER_COMPUTER"
    TEST = "TEST"


class PointStateEnum(enum.Enum):
    EMPTY = 0
    UNSELECTABLE = 1
    BLACK = 2
    WHITE = 3


class TurnStateEnum(enum.Enum):
    BLACK = 0
    WHITE = 1


class GameStateEnum(enum.Enum):
    CONTINUE = 0
    BLACK = 1
    WHITE = 2
    DRAW = 3


class PosPointState(enum.Enum):
    DOUBLE_THREE = 1
    DOUBLE_FOUR = 2
    FIVE = 3
    OVER = 4
