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
                PointStateEnum.EMPTY for i in range(BOARD_SIZE)
            ] for j in range(BOARD_SIZE)
        ]
        self.unselectable_points = list()
        self.turn = TurnStateEnum.BLACK
        self.black_agent = black_agent
        self.white_agent = white_agent
        self.directions = [
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

    def set_point_state(self, point, state):
        row, col = point
        self.array[row][col] = state

    def start(self):
        point_states = [PointStateEnum.BLACK, PointStateEnum.WHITE]

        while True:
            try:
                for move_function in self.move_functions:
                    row, col = move_function()
                    point = (row, col)
                    self.array[row][col] = self.get_current_turn_point_state()

                    # self.totalBlankCount -= 1
                    # self.check_finished(
                    #     self.totalBlankCount - len(self.unselectable_points),
                    #     point
                    # )

                    if self.turn == TurnStateEnum.BLACK:
                        self.set_unselectable_points(point)
                    else:
                        if self.array[row][col] == PointStateEnum.UNSELECTABLE:
                            self.unselectable_points.remove(point)
                        self.set_selectable_points()
                    self.change_turn()

            except KeyboardInterrupt:
                print("Stop Game by keyboard interrupt")
                break
            except TestEndError:
                break

    def check_finished(self, left, point):
        # Need to Make Enum
        # 0: No Win, 1: Black Win, 2: White Win, 3: Draw

        if self.check_lines(point):
            return GamestateEnum.WHITE if self.turn == TurnStateEnum.WHITE else GamestateEnum.BLACK  # Ternary Operator
        elif left == 0:
            return GamestateEnum.DRAW
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

    def set_unselectable_points(self, point):
        # Overline
        for direction in self.directions:
            forward_count, _, _, empty_point, _ = self.check_line_state(
                point, direction, PointStateEnum.BLACK, True)
            backward_count, _, _, _, _ = self.check_line_state(
                point, (-direction[0], -direction[1]), PointStateEnum.BLACK)
            count = forward_count + backward_count + 1
            if count >= 5:
                self.set_point_state(empty_point, PointStateEnum.UNSELECTABLE)
                self.unselectable_points.append(empty_point)
        # double_three & double_four
        for origin_direction in self.directions:
            for i in range(1, 5):
                row = point[0] + i * origin_direction[0]
                col = point[1] + i * origin_direction[1]
                search_point = (row, col)
                if (
                    self.is_out_of_array(search_point)
                    or self.array[row][col] != PointStateEnum.EMPTY
                ):
                    continue
                three, four = False, False
                checked_line_points = list()
                for direction in self.directions:
                    forward_count, forward_emtpy_count, is_countious, _, forward_point = self.check_line_state(
                        search_point, direction, PointStateEnum.BLACK, True)
                    backward_count, backward_emtpy_count, _, _, backward_point = self.check_line_state(
                        search_point, (-direction[0], -direction[1]), PointStateEnum.BLACK)
                    stone_count = forward_count + backward_count + 1
                    possible_count = (
                        stone_count + forward_emtpy_count + backward_emtpy_count + int(not is_countious)
                    )
                    if possible_count < 5 or (backward_point, forward_point) in checked_line_points:
                        continue
                    # double three
                    if (
                        stone_count == 3
                        and forward_emtpy_count
                        and backward_emtpy_count
                        and possible_count > 5
                    ):
                        # if search_point == (6, 4):
                        #     print(point, direction)
                        #     print(forward_count, forward_emtpy_count, is_countious)
                        #     print(backward_count, backward_emtpy_count)
                        #     print(backward_point, forward_point)
                        #     print('')
                        if three:
                            self.set_point_state(search_point, PointStateEnum.UNSELECTABLE)
                            self.unselectable_points.append(search_point)
                            break
                        three = True
                    # double four
                    elif stone_count == 4:
                        if four:
                            self.set_point_state(search_point, PointStateEnum.UNSELECTABLE)
                            self.unselectable_points.append(search_point)
                            break
                        four = True
                    checked_line_points.append((forward_point, backward_point))

    def set_selectable_points(self):
        for point in self.unselectable_points:
            three, double_three = False, False
            four, double_four = False, False
            overline, endable = False, False
            checked_line_points = list()
            for direction in self.directions:
                forward_count, forward_emtpy_count, is_countious, _, forward_point = self.check_line_state(
                    point, direction, PointStateEnum.BLACK, True)
                backward_count, backward_emtpy_count, _, _, backward_point = self.check_line_state(
                    point, (-direction[0], -direction[1]), PointStateEnum.BLACK)
                stone_count = forward_count + backward_count + 1
                possible_count = (
                    stone_count + forward_emtpy_count + backward_emtpy_count + int(not is_countious)
                )
                if possible_count < 5 or (backward_point, forward_point) in checked_line_points:
                    continue
                if self.check_five(point, PointStateEnum.BLACK):
                    endable = True
                    break
                # double three
                if (
                    stone_count == 3
                    and forward_emtpy_count
                    and backward_emtpy_count
                    and possible_count > 5
                ):
                    # print('unset')
                    # print(point, direction)
                    # print(forward_count, forward_emtpy_count, is_countious)
                    # print(backward_count, backward_emtpy_count)
                    # print(backward_point, forward_point)
                    # print('')
                    if three:
                        double_three = True
                    three = True
                # double four
                elif stone_count == 4:
                    if four:
                        double_four = True
                        break
                    four = True
                elif stone_count >= 5:
                    overline = True
                checked_line_points.append((forward_point, backward_point))
            # if point == (6, 4):
            #     print(endable, double_three, double_four, overline)
            if endable or not (double_three or double_four or overline):
                self.set_point_state(point, PointStateEnum.EMPTY)
                self.unselectable_points.remove(point)

    def check_line_state(self, point, direction, state, allow_empty=False):
        row_dir, col_dir = direction
        row, col = point
        opposite_state = state.get_opposite()
        stone_count, empty_count = 0, 0
        empty_point = tuple()
        is_continous = True
        while True:
            row, col = row + row_dir, col + col_dir
            if self.is_out_of_array((row, col)) or self.array[row][col] == opposite_state:
                break
            elif self.array[row][col] in [
                PointStateEnum.EMPTY,
                PointStateEnum.UNSELECTABLE
            ]:
                empty_count += 1
                if empty_count >= 3:
                    break
            elif self.array[row][col] == state:
                if state == PointStateEnum.BLACK:
                    if empty_count:
                        if allow_empty and is_continous and empty_count == 1:
                            is_continous = False
                            stone_count += 1
                            empty_count = 0
                            empty_point = (row - row_dir, col - col_dir)
                            continue
                        else:
                            empty_count -= 1
                            row, col = row - row_dir, col - col_dir
                            break
                    else:
                        stone_count += 1
                else:
                    if empty_count:
                        break
                    stone_count += 1
        return stone_count, empty_count, is_continous, empty_point, (row, col)

    def check_five(self, point, color):
        for direction in self.directions:
            forward_count, _, _, _, _ = self.check_line_state(
                point, direction, color)
            backward_count, _, _, _, _ = self.check_line_state(
                point, (-direction[0], -direction[1]), color)
            count = forward_count + backward_count + 1

            if color == PointStateEnum.BLACK and count == 5:
                return True
            if color == PointStateEnum.WHITE and count >= 5:
                return True

        return False