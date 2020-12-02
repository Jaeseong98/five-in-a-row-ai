import traceback

from .enum import GameMode, PointStateEnum, TurnStateEnum, GamestateEnum
from .exc import OutOfIndexError, CanNotSelectError, TestEndError
from .config import BOARD_SIZE


class GameBoard(object):
    """
    GameBoard for five-in-a-row
    Contain enviroment information for game

    """

    def __init__(self, mode, black_agent=None, white_agent=None):
        self.totalBlankCount = BOARD_SIZE * BOARD_SIZE
        self.array = [
            [
                PointStateEnum.BLANK for i in range(BOARD_SIZE)
            ] for j in range(BOARD_SIZE)
        ]
        self.unselectable_points = list()
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
        str_map = {
            PointStateEnum.BLANK: ".",
            PointStateEnum.UNSELECTABLE: "X",
            PointStateEnum.BLACK: "B",
            PointStateEnum.WHITE: "W",
        }
        return "\n".join([
            " ".join([
                str_map[point] for point in line
            ]) for line in self.array
        ])

    # @property
    # def unselectable_points(self):
    #     unselectable_points = list()
    #     for row, line in enumerate(self.array):
    #         for col, point in enumerate(line):
    #             if point == PointStateEnum.UNSELECTABLE:
    #                 unselectable_points.append((row, col))
    #     return unselectable_points

    def change_turn(self):
        if self.turn == TurnStateEnum.BLACK:
            self.turn = TurnStateEnum.WHITE
        else:
            self.turn = TurnStateEnum.BLACK

    def get_current_turn_point_state(self):
        state_map = {
            TurnStateEnum.BLACK: PointStateEnum.BLACK,
            TurnStateEnum.WHITE: PointStateEnum.WHITE
        }
        return state_map[self.turn]

    def is_out_of_array(self, point):
        row, col = point
        return row < 0 or BOARD_SIZE - 1 < row or col < 0 or BOARD_SIZE - 1 < col

    def start(self):
        point_states = [PointStateEnum.BLACK, PointStateEnum.WHITE]

        while True:
            try:
                for move_function in self.move_functions:
                    row, col = move_function()
                    self.array[row][col] = self.get_current_turn_point_state()
                    if self.turn == TurnStateEnum.BLACK:
                        self.detect_unselectable_points()
                    else:
                        if self.array[row][col] == PointStateEnum.UNSELECTABLE:
                            self.unselectable_points.remove((row, col))
                    self.detect_selectable_points()
                    self.change_turn()
                    self.totalBlankCount -= 1
                    self.check_finished(
                        self.totalBlankCount - len(self.unselectable_points),
                        (row, col)
                    )

            except KeyboardInterrupt:
                print("Stop Game")
                break
            except TestEndError:
                break
            # except Exception:
            #     print(traceback.format_exc())

    def check_finished(self, left, point):
        # Need to Make Enum
        # 0: No Win, 1: Black Win, 2: White Win, 3: Draw

        if left == 0:
            return GamestateEnum.DRAW
        elif self.check_lines(point):
            return GamestateEnum.WHITE if self.turn == TurnStateEnum.WHITE else GamestateEnum.BLACK  # Ternary Operator
        else:
            return GamestateEnum.CONTINUE

    def get_next_point_from_stdin(self):
        row, col = input("Input(row, col): ").split()
        row, col = int(row), int(col)
        if self.is_out_of_array((row, col)):
            raise OutOfIndexError
        if self.array[row][col] in [
            PointStateEnum.BLACK,
            PointStateEnum.WHITE
        ]:
            raise CanNotSelectError
        if (
            self.array[row][col] == PointStateEnum.UNSELECTABLE
            and self.turn == PointStateEnum.BLACK
        ):
            raise CanNotSelectError
        return (row, col)

    def detect_unselectable_points(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.array[row][col] == PointStateEnum.BLANK:
                    point = (row, col)
                    is33Rule = self.check_33_rule(point, point)
                    is44Rule = self.check_44_rule(point, point)
                    isOver5Rule = self.check_over_5_rule(point)
                    if is33Rule or is44Rule or isOver5Rule:
                        print('unsec check')
                        self.array[row][col] = 1
                        self.unselectable_points.append(point)
                    elif self.array[row][col] == 0:
                        self.detect_unselectable_points_from_origin_point(point)
        return


    def detect_unselectable_points_from_origin_point(self, originPoint):
        originRow, originCol = originPoint

        self.array[originRow][originCol] = 2
        directionList = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for direction in directionList:
            point = (originPoint[0] + direction[0], originPoint[1] + direction[1])
            row, col = point
            while (
                not self.is_out_of_array(point)
                and self.array[row][col] != PointStateEnum.WHITE
            ):
                if self.array[row][col] == 2:
                    is33Rule = self.check_33_rule(originPoint, point)
                    is44Rule = self.check_44_rule(originPoint, point)
                    if is33Rule or is44Rule:
                        originRow, originCol = originPoint
                        self.array[originRow][originCol] = 1
                        self.unselectable_points.append(originPoint)
                        return
                point = (row + direction[0], col + direction[1])
                row, col = point

        self.array[originRow][originCol] = 0

    def detect_selectable_points(self):
        removeList = []
        for point in self.unselectable_points:
            is33Rule = self.check_33_rule(point, point)
            is44Rule = self.check_44_rule(point, point)
            isOver5Rule = self.check_over_5_rule(point)
            if (is33Rule == False and is44Rule == False and isOver5Rule == False):
                if self.detect_selectable_points_from_origin_point(point) == False:
                    removeList.append(point)
                    row, col = point
                    self.array[row][col] = 0
                    pass

        for point in removeList:
            self.unselectable_points.remove(point)

    def detect_selectable_points_from_origin_point(self, originPoint):
        originRow, originCol = originPoint
        self.array[originRow][originCol] = 2
        directionList = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for direction in directionList:
            point = (originPoint[0] + direction[0], originPoint[1] + direction[1])
            row, col = point
            while self.is_out_of_array(point) == False and self.array[row][col] != 3:
                if self.array[row][col] == 2:
                    is33Rule = self.check_33_rule(originPoint, point)
                    is44Rule = self.check_44_rule(originPoint, point)
                    if (is33Rule == True or is44Rule == True):
                        self.array[originRow][originCol] = 1
                        return True
                point = (row + direction[0], col + direction[1])
                row, col = point
        return False

    def check_33_rule(self, originPoint, point):
        row, col = point
        lastBlackIndex = row * BOARD_SIZE + col

        directionTupleList = [((1, 0), (-1, 0)), ((0, 1), (0, -1)), ((1, 1), (-1, -1)), ((1, -1), (-1, 1)), ((-1, 0), (1, 0)), ((0, -1), (0, 1)), ((-1, -1), (1, 1)), ((-1, 1), (1, -1))]
        
        lineCount = 0
        for direction in directionTupleList:
            count1, isOpen1, lastBlackIndex1, isBlankInclude1, blankCount1 = self.check_discountinuous_line_recursion(point, direction[0], lastBlackIndex)
            count2, isOpen2, lastBlackIndex2, isBlankInclude2, blankCount2 = self.check_discountinuous_line_recursion(point, direction[1], lastBlackIndex, isBlankInclude1)
            count = count1 + count2 + 1
            isOpen = isOpen1 and isOpen2

            if lastBlackIndex1 < lastBlackIndex2:
                beginIndex = lastBlackIndex1
                endIndex = lastBlackIndex2
            else:
                beginIndex = lastBlackIndex2
                endIndex = lastBlackIndex1

            if (count == 3 and isOpen):
                if lineCount == 0:
                    firstLineBeginIndex = beginIndex
                    firstLineEndIndex = endIndex
                    lineCount += 1
                elif firstLineBeginIndex != beginIndex or firstLineEndIndex != endIndex:
                    print("33: " + str((firstLineBeginIndex, firstLineEndIndex)) + " " + str((beginIndex, endIndex)))
                    lineCount += 1

            if (lineCount == 2):
                print("Unselectable by 33!" + str(originPoint) + " " + str(point))
                return True
        return False

    def check_44_rule(self, originPoint, point):
        row, col = point
        lastBlackIndex = row * BOARD_SIZE + col
        
        directionTupleList = [((1, 0), (-1, 0)), ((0, 1), (0, -1)), ((1, 1), (-1, -1)), ((1, -1), (-1, 1)), ((-1, 0), (1, 0)), ((0, -1), (0, 1)), ((-1, -1), (1, 1)), ((-1, 1), (1, -1))]
        
        lineCount = 0
        for direction in directionTupleList:
            count1, isOpen1, lastBlackIndex1, isBlankInclude1, blankCount1 = self.check_discountinuous_line_recursion(point, direction[0], lastBlackIndex)
            count2, isOpen2, lastBlackIndex2, isBlankInclude2, blankCount2 = self.check_discountinuous_line_recursion(point, direction[1], lastBlackIndex, isBlankInclude1)
            count = count1 + count2 + 1
            isOpen = isOpen1 or isOpen2   
        
            if isOpen == False and blankCount1 + blankCount2 > 1:
                isOpen = True

            if lastBlackIndex1 < lastBlackIndex2:
                beginIndex = lastBlackIndex1
                endIndex = lastBlackIndex2
            else:
                beginIndex = lastBlackIndex2
                endIndex = lastBlackIndex1

            if (count == 4 and isOpen):
                if lineCount == 0:
                    firstLineBeginIndex = beginIndex
                    firstLineEndIndex = endIndex
                    lineCount += 1
                elif firstLineBeginIndex != beginIndex and firstLineEndIndex != endIndex:
                    print("44: " + str((firstLineBeginIndex, firstLineEndIndex)) + " " + str((beginIndex, endIndex)))
                    lineCount += 1
            
            if lineCount == 2:
                print("Unselectable by 44!" + str(originPoint) + " " + str(point))
                return True
        return False

    def check_discountinuous_line_recursion(
        self, point, direction, lastBlackIndex,
        isIncludeBlank = False, blankCount = 0
    ):
        point = (point[0] + direction[0], point[1] + direction[1])
        row, col = point
        
        if blankCount >= 2:
            return (0, True, lastBlackIndex, isIncludeBlank, blankCount)
        elif self.is_out_of_array(point) or self.array[row][col] == 3:
            return (0, False, lastBlackIndex, isIncludeBlank, blankCount)
        elif self.array[row][col] == 0 or self.array[row][col] == 1:
            if isIncludeBlank:
                return (0, True, lastBlackIndex, isIncludeBlank, blankCount + 1)
            else:
                _count, _isOpen, _lastBlackIndex, _isIncludeBlank, _blankCount = self.check_discountinuous_line_recursion(point, direction, lastBlackIndex, isIncludeBlank, blankCount + 1)
                return (_count, _isOpen, _lastBlackIndex, _isIncludeBlank, _blankCount)
        else:
            if blankCount > 0:
                isIncludeBlank = True
            lastBlackIndex = row * BOARD_SIZE + col
            _count, _isOpen, _lastBlackIndex, _isIncludeBlank, _blankCount = self.check_discountinuous_line_recursion(point, direction, lastBlackIndex, isIncludeBlank, blankCount)
            return (_count + 1, _isOpen, _lastBlackIndex, _isIncludeBlank, _blankCount)

    def check_lines(self, point):
        directionTupleList = [((1, 0), (-1, 0)), ((0, 1), (0, -1)), ((1, 1), (-1, -1)), ((1, -1), (-1, 1))]

        for direction in directionTupleList:
            userIndex = self.get_current_turn_point_state()
            count1 = self.check_continuous_line_recursion(point, direction[0], userIndex)
            count2 = self.check_continuous_line_recursion(point, direction[1], userIndex)
            count = count1 + count2 + 1

            if self.turn == TurnStateEnum.BLACK and count == 5:
                return True
            elif count >= 5:
                return True

        return False

    def check_over_5_rule(self, point):
        directionTupleList = [((1, 0), (-1, 0)), ((0, 1), (0, -1)), ((1, 1), (-1, -1)), ((1, -1), (-1, 1))]
        for direction in directionTupleList:
            userIndex = PointStateEnum.BLACK # Always black
            count1 = self.check_continuous_line_recursion(point, direction[0], userIndex)
            count2 = self.check_continuous_line_recursion(point, direction[1], userIndex)
            count = count1 + count2 + 1

            if count > 5:
                print("Unselectable by over5!" + str(point))
                return True
        return False


    def check_continuous_line_recursion(self, point, direction, userIndex):
        point = (point[0] + direction[0], point[1] + direction[1])
        row, col = point

        if self.is_out_of_array(point) or self.array[row][col] != userIndex:
            return 0
        else:
            return 1 + self.check_continuous_line_recursion(point, direction, userIndex)