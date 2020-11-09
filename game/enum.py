import enum

class GameMode(enum.Enum):
    HUMAN_HUMAN = "HUMAN_HUMAN"
    HUMAN_COMPUTER = "HUMAN_COMPUTER"
    COMPUTER_HUMAN = "COMPUTER_HUMAN"
    COMPUTER_COMPUTER = "COMPUTER_COMPUTER"


class PointStateEnum(enum.Enum):
    BLANK = 0
    UNSELECTABLE = 1
    BLACK = 2
    WHITE = 3


class TurnStateEnum(enum.Enum):
    BLACK = 0
    WHITE = 1
