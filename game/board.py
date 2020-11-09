import traceback

from .enum import GameMode, PointStateEnum, TurnStateEnum
from .exc import OutOfIndexError, CanNotSelectError
from .config import MAX_SIZE


class GameBoard(object):
    """
    GameBoard for five-in-a-row
    Contain enviroment information for game

    """

    def __init__(self, mode):
        self.count = 0
        self.array = [
            [
                PointStateEnum.BLANK for i in range(MAX_SIZE)
            ] for j in range(MAX_SIZE)
        ]
        self.turn = TurnStateEnum.BLACK

        mode_function_map = {
            GameMode.HUMAN_HUMAN: [
                self.get_point_from_stdin,
                self.get_point_from_stdin
            ],
            GameMode.HUMAN_COMPUTER: [
                self.get_point_from_stdin,
                self.get_point_from_agent
            ],
            GameMode.COMPUTER_HUMAN: [
                self.get_point_from_agent,
                self.get_point_from_stdin
            ],
            GameMode.COMPUTER_COMPUTER: [
                self.get_point_from_agent,
                self.get_point_from_agent
            ],
        }
        try:
            self.move_functions = mode_function_map[mode]
        except KeyError:
            raise ValueError(f"Wrong game mode input: {mode}")

    def __str__(self):
        return "\n".join([" ".join(row) for row in self.array])

    def start(self, mode):
        point_states = [PointStateEnum.BLACK, PointStateEnum.WHITE]

        while True:
            try:
                for move_function, point_state in zip(
                    self.move_functions, point_states
                ):
                    print(self.count)
                    row, col = move_functions()
                    self.array[row][col] = point_state
                    self.update_point_states()

            except KeyboardInterrupt:
                print("Stop Game")
                print(self.__str__())
                break
            except Exception as e:
                print(traceback.format_exc())
                print(self.__str__())

    def get_point_from_stdin(self):
        row, col = input("Input(row, col): ").split()
        row, col = int(row), int(col)
        if row < 0 or row >= MAX_SIZE or col < 0 or col >= MAX_SIZE:
            raise OutOfIndexError
        if array[row][col] in [
            PointStateEnum.UNSELECTABLE,
            PointStateEnum.BLACK,
            PointStateEnum.WHITE
        ]:
            raise CanNotSelectError
        return (row, col)

    def get_point_from_agent(self):
        pass

    def update_point_states(point):
        row, col = point
        for i in range(1, 5):
            detect_unselectable_point((row + i, col), 0)
            detect_unselectable_point((row - i, col), 0)
            detect_unselectable_point((row, col + i), 1)
            detect_unselectable_point((row, col - i), 1)
            detect_unselectable_point((row + i, col + i), 2)
            detect_unselectable_point((row - i, col - i), 2)
            detect_unselectable_point((row + i, col - i), 3)
            detect_unselectable_point((row - i, col + i), 3)
        return 

    def detect_unselectable_point(point, option):
        row, col = point

        if array[row][col] != 0:
            return
        
        print("Start Detecting Function")
        rule1Count = 0
        rule2Count = 0
        rule3Count = 0

        count_1, isOpen_1 = check_point_condition(point, 4, (1, 0))
        count_2, isOpen_2 = check_point_condition(point, 4, (-1, 0))
        totalCount = count_1 + count_2 + 1
        if (totalCount == 3 and isOpen_1 == True and isOpen_2 == True):
            rule1Count += 1
            if rule1Count == 2:
                array[row][col] = 1
                return
        if totalCount == 4:
            rule2Count += 1
            if rule2Count == 2:
                array[row][col] = 1
                return
        if totalCount > 5:
        array[row][col] = 1
        return

        count_1, isOpen_1 = check_point_condition(point, 4, (0, 1))
        count_2, isOpen_2 = check_point_condition(point, 4, (0, -1))
        totalCount = count_1 + count_2 + 1
        if (totalCount == 3 and isOpen_1 == True and isOpen_2 == True):
            rule1Count += 1
            if rule1Count == 2:
                array[row][col] = 1
                return
        if totalCount == 4:
            rule2Count += 1
            if rule2Count == 2:
                array[row][col] = 1
                return
        if totalCount > 5:
        array[row][col] = 1
        return
        
        count_1, isOpen_1 = check_point_condition(point, 4, (1, 1))
        count_2, isOpen_2 = check_point_condition(point, 4, (-1, -1))
        totalCount = count_1 + count_2 + 1
        if (totalCount == 3 and isOpen_1 == True and isOpen_2 == True):
            rule1Count += 1
            if rule1Count == 2:
                array[row][col] = 1
                return
        if totalCount == 4:
            rule2Count += 1
            if rule2Count == 2:
                array[row][col] = 1
                return
        if totalCount > 5:
        array[row][col] = 1
        return
        
        count_1, isOpen_1 = check_point_condition(point, 4, (1, -1))
        count_2, isOpen_2 = check_point_condition(point, 4, (-1, 1))
        totalCount = count_1 + count_2 + 1
        if (totalCount == 3 and isOpen_1 == True and isOpen_2 == True):
            rule1Count += 1
            if rule1Count == 2:
                array[row][col] = 2
                return
        if totalCount == 4:
            rule2Count += 1
            if rule2Count == 2:
                array[row][col] = 2
                return
        if totalCount > 5:
        array[row][col] = 2
        return

    def check_point_condition(self, point, n, different):
        point = (point[0] + different[0], point[1] + different[1])
        row, col = point
        
        if (n == 0):
            return (0, True)
        elif (row < 0 or 14 > row) and (col < 0 or 14 > col) or array[row][col] == 3:
            return (0, False)   
        else:
            _count, _isOpen = check_point_condition(point, n - 1, different)
            return ((1 if array[row][col] == 2 else 0) + _count, (True and _isOpen))
