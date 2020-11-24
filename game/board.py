import traceback

from .enum import GameMode, PointStateEnum, TurnStateEnum
from .exc import OutOfIndexError, CanNotSelectError, TestEndError
from .config import MAX_SIZE


class GameBoard(object):
    """
    GameBoard for five-in-a-row
    Contain enviroment information for game

    """

    def __init__(self, mode, black_agent=None, white_agent=None):
        self.count = 0
        self.array = [
            [
                PointStateEnum.BLANK for i in range(MAX_SIZE)
            ] for j in range(MAX_SIZE)
        ]
        self.turn = TurnStateEnum.BLACK
        self.black_agent = black_agent
        self.white_agent = white_agent

        try:
            mode_function_map = {
                GameMode.HUMAN_HUMAN: [
                    self.get_next_point_from_stdin,
                    self.get_next_point_from_stdin
                ],
                GameMode.HUMAN_COMPUTER: [
                    self.get_next_point_from_stdin,
                    self.white_agent.get_next_point
                ],
                GameMode.COMPUTER_HUMAN: [
                    self.black_agent.get_next_point,
                    self.get_next_point_from_stdin
                ],
                GameMode.COMPUTER_COMPUTER: [
                    self.black_agent.get_next_point,
                    self.white_agent.get_next_point
                ]
            }
            self.move_functions = mode_function_map[mode]
        except KeyError:
            raise ValueError(f"Wrong game mode input: {mode}")
        except AttributeError:
            raise ValueError(f"Invalid agent")

    def __str__(self):
        return "\n".join([
            " ".join([
                str(point.value) for point in line
            ]) for line in self.array
        ])

    @property
    def unselectable_points(self):
        unselectable_points = list()
        for row, line in enumerate(self.array):
            for col, point in enumerate(line):
                if point == PointStateEnum.UNSELECTABLE:
                    unselectable_points.append((row, col))
        return unselectable_points

    def start(self):
        point_states = [PointStateEnum.BLACK, PointStateEnum.WHITE]

        while True:
            try:
                for move_function, point_state in zip(
                    self.move_functions, point_states
                ):
                    row, col = move_function()
                    self.array[row][col] = point_state
                    # self.update_point_states((row, col))

            except KeyboardInterrupt:
                print("Stop Game")
                print(self)
                break
            except TestEndError:
                break
            except Exception:
                print(traceback.format_exc())
                print(self)

    def get_next_point_from_stdin(self):
        row, col = input("Input(row, col): ").split()
        row, col = int(row), int(col)
        if row < 0 or row >= MAX_SIZE or col < 0 or col >= MAX_SIZE:
            raise OutOfIndexError
        if self.array[row][col] in [
            PointStateEnum.UNSELECTABLE,
            PointStateEnum.BLACK,
            PointStateEnum.WHITE
        ]:
            raise CanNotSelectError
        return (row, col)

    def update_point_states(self, point):
        row, col = point
        for i in range(1, 5):
            self.detect_unselectable_point((row + i, col), 0)
            self.detect_unselectable_point((row - i, col), 0)
            self.detect_unselectable_point((row, col + i), 1)
            self.detect_unselectable_point((row, col - i), 1)
            self.detect_unselectable_point((row + i, col + i), 2)
            self.detect_unselectable_point((row - i, col - i), 2)
            self.detect_unselectable_point((row + i, col - i), 3)
            self.detect_unselectable_point((row - i, col + i), 3)
        return 

    def detect_unselectable_point(self, point, option):
        row, col = point

        if self.array[row][col] != 0:
            return
        
        print("Start Detecting Function")
        rule1Count = 0
        rule2Count = 0
        rule3Count = 0

        count_1, isOpen_1 = self.check_point_condition(point, 4, (1, 0))
        count_2, isOpen_2 = self.check_point_condition(point, 4, (-1, 0))
        totalCount = count_1 + count_2 + 1
        if (totalCount == 3 and isOpen_1 == True and isOpen_2 == True):
            rule1Count += 1
            if rule1Count == 2:
                self.array[row][col] = 1
                return
        if totalCount == 4:
            rule2Count += 1
            if rule2Count == 2:
                self.array[row][col] = 1
                return
        if totalCount > 5:
            self.array[row][col] = 1
            return

        count_1, isOpen_1 = self.check_point_condition(point, 4, (0, 1))
        count_2, isOpen_2 = self.check_point_condition(point, 4, (0, -1))
        totalCount = count_1 + count_2 + 1
        if (totalCount == 3 and isOpen_1 == True and isOpen_2 == True):
            rule1Count += 1
            if rule1Count == 2:
                self.array[row][col] = 1
                return
        if totalCount == 4:
            rule2Count += 1
            if rule2Count == 2:
                self.array[row][col] = 1
                return
        if totalCount > 5:
            self.array[row][col] = 1
            return
        
        count_1, isOpen_1 = self.check_point_condition(point, 4, (1, 1))
        count_2, isOpen_2 = self.check_point_condition(point, 4, (-1, -1))
        totalCount = count_1 + count_2 + 1
        if (totalCount == 3 and isOpen_1 == True and isOpen_2 == True):
            rule1Count += 1
            if rule1Count == 2:
                self.array[row][col] = 1
                return
        if totalCount == 4:
            rule2Count += 1
            if rule2Count == 2:
                self.array[row][col] = 1
                return
        if totalCount > 5:
            self.array[row][col] = 1
            return
        
        count_1, isOpen_1 = self.check_point_condition(point, 4, (1, -1))
        count_2, isOpen_2 = self.check_point_condition(point, 4, (-1, 1))
        totalCount = count_1 + count_2 + 1
        if (totalCount == 3 and isOpen_1 == True and isOpen_2 == True):
            rule1Count += 1
            if rule1Count == 2:
                self.array[row][col] = 2
                return
        if totalCount == 4:
            rule2Count += 1
            if rule2Count == 2:
                self.array[row][col] = 2
                return
        if totalCount > 5:
            self.array[row][col] = 2
            return

    def check_point_condition(self, point, n, different):
        point = (point[0] + different[0], point[1] + different[1])
        row, col = point
        
        if (n == 0):
            return (0, True)
        elif (row < 0 or 14 > row) and (col < 0 or 14 > col) or self.array[row][col] == 3:
            return (0, False)   
        else:
            _count, _isOpen = self.check_point_condition(point, n - 1, different)
            return ((1 if self.array[row][col] == 2 else 0) + _count, (True and _isOpen))
