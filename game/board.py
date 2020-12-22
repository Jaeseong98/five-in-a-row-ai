import traceback

from .enum import GameMode, PointStateEnum, TurnStateEnum, GamestateEnum
from .exc import (
    OutOfIndexError,
    CanNotSelectError,
    GameEndError,
    TestEndError,
)
from .config import BOARD_SIZE


class GameBoard(object):
    """
    GameBoard for five-in-a-row
    Contain enviroment information for game

    """

    def __init__(self, mode, black_agent=None, white_agent=None):
        self.total_blank_count = BOARD_SIZE * BOARD_SIZE
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
        while True:
            try:
                for move_function in self.move_functions:
                    row, col = move_function()
                    point = (row, col)
                    self.array[row][col] = self.get_current_turn_point_state()

                    self.total_blank_count -= 1
                    self.check_finished(
                        self.total_blank_count - len(self.unselectable_points),
                        point
                    )

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
        if self.check_five(point, self.get_current_turn_point_state()):
            raise GameEndError(self.turn)
        elif left == 0:
            return GameEndError()

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
                    if three:
                        double_three = True
                    three = True
                # double four
                elif stone_count == 4:
                    if four:
                        double_four = True
                        break
                    four = True
                elif stone_count >= 5 and is_countious:
                    overline = True
                checked_line_points.append((forward_point, backward_point))
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