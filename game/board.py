import traceback

from .enum import (
    GameMode, PointStateEnum, TurnStateEnum, GameStateEnum, PosPointState
)
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
                PointStateEnum.EMPTY for i in range(BOARD_SIZE)
            ] for j in range(BOARD_SIZE)
        ]
        self.pos_array = [
            [
                list() for i in range(BOARD_SIZE)
            ] for j in range(BOARD_SIZE)
        ]
        self.turn = TurnStateEnum.BLACK
        self.black_agent = black_agent
        self.white_agent = white_agent

        self.unselectable_points = list()
        self.base_vector = [
            (i, j) for i in range(-1, 2, 1) for j in range(-1, 2, 1) if i or j
        ]

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
            PointStateEnum.EMPTY: ".",
            PointStateEnum.UNSELECTABLE: "X",
            PointStateEnum.BLACK: "B",
            PointStateEnum.WHITE: "W",
        }
        return "\n".join([
            " ".join([
                str_map[point] for point in line
            ]) for line in self.array
        ])

    def get_point_state(self, point):
        return self.array[point[0]][point[1]]

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
        while True:
            try:
                for move_function in self.move_functions:
                    row, col = move_function()
                    self.array[row][col] = self.get_current_turn_point_state()
                    if self.turn == TurnStateEnum.BLACK:
                        # self.detect_unselectable_points()
                        self.set_pos_states((row, col))
                    else:
                        if self.array[row][col] == PointStateEnum.UNSELECTABLE:
                            self.unselectable_points.remove((row, col))
                    # self.detect_selectable_points()
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
            return GameStateEnum.DRAW
        elif self.check_lines(point):
            return GameStateEnum.WHITE if self.turn == TurnStateEnum.WHITE else GameStateEnum.BLACK  # Ternary Operator
        else:
            return GameStateEnum.CONTINUE

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
                if self.array[row][col] == PointStateEnum.EMPTY:
                    point = (row, col)
                    is33Rule = self.check_33_rule(point, point)
                    is44Rule = self.check_44_rule(point, point)
                    isOver5Rule = self.check_over_5_rule(point)
                    if is33Rule or is44Rule or isOver5Rule:
                        self.array[row][col] = PointStateEnum.UNSELECTABLE
                        self.unselectable_points.append(point)
                    elif self.array[row][col] == PointStateEnum.EMPTY:
                        self.detect_unselectable_points_from_origin_point(point)
        return


    def detect_unselectable_points_from_origin_point(self, originPoint):
        originRow, originCol = originPoint

        self.array[originRow][originCol] = PointStateEnum.BLACK
        directionList = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for direction in directionList:
            point = (originPoint[0] + direction[0], originPoint[1] + direction[1])
            row, col = point
            while (
                not self.is_out_of_array(point)
                and self.array[row][col] != PointStateEnum.WHITE
            ):
                if self.array[row][col] == PointStateEnum.BLACK:
                    is33Rule = self.check_33_rule(originPoint, point)
                    is44Rule = self.check_44_rule(originPoint, point)
                    if is33Rule or is44Rule:
                        originRow, originCol = originPoint
                        self.array[originRow][originCol] = PointStateEnum.UNSELECTABLE
                        self.unselectable_points.append(originPoint)
                        return
                point = (row + direction[0], col + direction[1])
                row, col = point

        self.array[originRow][originCol] = PointStateEnum.EMPTY

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
                    self.array[row][col] = PointStateEnum.EMPTY
                    pass

        for point in removeList:
            self.unselectable_points.remove(point)

    def detect_selectable_points_from_origin_point(self, originPoint):
        originRow, originCol = originPoint
        self.array[originRow][originCol] = PointStateEnum.BLACK
        directionList = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for direction in directionList:
            point = (originPoint[0] + direction[0], originPoint[1] + direction[1])
            row, col = point
            while (
                self.is_out_of_array(point) == False
                and self.array[row][col] != PointStateEnum.WHITE
            ):
                if self.array[row][col] == PointStateEnum.BLACK:
                    is33Rule = self.check_33_rule(originPoint, point)
                    is44Rule = self.check_44_rule(originPoint, point)
                    if (is33Rule == True or is44Rule == True):
                        self.array[originRow][originCol] = PointStateEnum.UNSELECTABLE
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
        elif self.is_out_of_array(point) or self.array[row][col] == PointStateEnum.WHITE:
            return (0, False, lastBlackIndex, isIncludeBlank, blankCount)
        elif (
            self.array[row][col] == PointStateEnum.EMPTY
            or self.array[row][col] == PointStateEnum.UNSELECTABLE
        ):
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

    def check_line_states(self, point, vector):
        # go to start point
        empty_count, possible_black_count = 0, 0
        row, col = point
        row_vector, col_vector = -vector[0], -vector[1]
        while True:
            row, col = row + row_vector, col + col_vector
            if self.is_out_of_array((row, col)):
                break
            point_state = self.array[row][col]
            if point_state in [PointStateEnum.EMPTY, PointStateEnum.UNSELECTABLE]:
                possible_black_count += 1
                empty_count += 1
                if empty_count == 3 or possible_black_count >= 5:
                    break
            elif point_state == PointStateEnum.BLACK:
                possible_black_count += 1
                empty_count = 0
            elif point_state == PointStateEnum.WHITE:
                break

        # store points until the end of line
        empty_points, empty_count = list(), 0
        start_empty_count, in_line_empty_count, end_empty_count = 0, 0, 0
        black_count, possible_black_count = 0, 0
        row_vector, col_vector = -row_vector, -col_vector
        line_started, line_ended = False, False
        start_point = (row, col)
        while True:
            row, col = row + row_vector, col + col_vector
            if self.is_out_of_array((row, col)):
                break
            point_state = self.array[row][col]
            if point_state in [PointStateEnum.EMPTY, PointStateEnum.UNSELECTABLE]:
                possible_black_count += 1
                empty_count += 1
                if empty_count == 3 or possible_black_count - start_empty_count >= 5:
                    empty_count -= 1
                    break
                if line_started:
                    line_ended = True
                empty_points.append((row, col))
            elif point_state == PointStateEnum.WHITE:
                break
            elif point_state == PointStateEnum.BLACK:
                black_count += 1
                possible_black_count += 1
                if not line_started:
                    start_empty_count = empty_count
                    empty_count = 0
                    line_started = True
                if line_ended:
                    in_line_empty_count = empty_count
                    empty_count = 0
                    line_ended = False

        end_empty_count = empty_count
        end_point = (row, col)
        return (
            start_point,
            end_point,
            empty_points,
            start_empty_count,
            in_line_empty_count,
            end_empty_count,
            black_count,
            possible_black_count
        )

    def set_pos_states(self, point):
        checked_line = list()
        for vector in self.base_vector:
            result = self.check_line_states(point, vector)
            print(point, vector, result)
            possible_black_count = result[7]
            if possible_black_count < 5:
                continue
            start_point = result[0]
            end_point = result[1]
            if (start_point, end_point) in checked_line:
                continue
            empty_points = result[2]
            start_empty_count = result[3]
            in_line_empty_count = result[4]
            end_empty_count = result[5]
            black_count = result[6]

            assert start_empty_count < 3 and end_empty_count < 3

            if (
                self.is_out_of_array(start_point)
                or self.get_point_state(start_point) in [
                    PointStateEnum.BLACK, PointStateEnum.WHITE
                ]
            ):
                empty_points.pop(0)
                start_empty_count -= 1
            if (
                self.is_out_of_array(end_point)
                or self.get_point_state(end_point) in [
                    PointStateEnum.BLACK, PointStateEnum.WHITE
                ]
            ):
                empty_points.pop(-1)
                end_empty_count -= 1

            if black_count == 2:
                target_points = list()
                if in_line_empty_count == 0:
                    target_points = empty_points[:start_empty_count] + empty_points[-end_empty_count:]
                elif in_line_empty_count == 1:
                    target_points = empty_points[:min(1, start_empty_count)] + empty_points[-min(1, end_empty_count):]
                elif in_line_empty_count == 2:
                    target_points = empty_points[start_empty_count:-end_empty_count]
                if target_points:
                    for row, col in target_points:
                        self.pos_array[row][col].append(PosPointState.DOUBLE_THREE)
                        if self.pos_array[row][col].count(PosPointState.DOUBLE_THREE) > 1:
                            self.array[row][col] = PointStateEnum.UNSELECTABLE
                            self.unselectable_points.append((row, col))
            elif black_count == 3:
                target_points = list()
                if in_line_empty_count == 0:
                    target_points = empty_points[:start_empty_count] + empty_points[-end_empty_count:]
                elif in_line_empty_count == 1:
                    target_points = empty_points[:min(1, start_empty_count)] + empty_points[-min(1, end_empty_count):]
                elif in_line_empty_count == 2:
                    target_points = empty_points[start_empty_count:-end_empty_count]
                if target_points:
                    for row, col in target_points:
                        self.pos_array[row][col].append(PosPointState.DOUBLE_FOUR)
                        if self.pos_array[row][col].count(PosPointState.DOUBLE_FOUR) > 1:
                            self.array[row][col] = PointStateEnum.UNSELECTABLE
                            self.unselectable_points.append((row, col))
            elif black_count == 4:
                if in_line_empty_count:
                    row, col = empty_points[start_empty_count - 1]
                    self.pos_array[row][col].append(PosPointState.ENDABLE)
                    self.array[row][col] = PointStateEnum.EMPTY
                else:
                    row, col = empty_points[start_empty_count - 1]
                    self.pos_array[row][col].append(PosPointState.ENDABLE)
                    self.array[row][col] = PointStateEnum.EMPTY
                    row, col = empty_points[-end_empty_count]
                    self.pos_array[row][col].append(PosPointState.ENDABLE)
                    self.array[row][col] = PointStateEnum.EMPTY
            elif black_count >= 5:
                row, col = empty_points[start_empty_count]
                self.pos_array[row][col].append(PosPointState.OVER)
                self.array[row][col] = PointStateEnum.UNSELECTABLE
                self.unselectable_points.append((row, col))
            checked_line.append((end_point, start_point))
        return

    # def unset_pos_states(self, point, vector):
    #     row, col = point
    #     row_vector, col_vector = vector
    #     for vector in self.base_vector:
    #         row, col = row + row_vector, col + col_vector
    #         if self.is_out_of_array((row, col)):
    #             row, col = point
    #             continue
    #         if self.array[row][col] == PointStateEnum.BLACK:

    #         elif self.pos_array[row][col]:


    #         else:
    #             row, col = point
    #             continue