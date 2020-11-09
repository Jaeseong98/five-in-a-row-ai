import enum

class PointState(enum.Enum):
    BLANK = 0
    UNSELECTABLE = 1
    BLACK = 2
    WHITE = 3


class TurnState(enum.Enum):
    BLANK = 0
    WHITE = 1
