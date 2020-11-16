import sys

# Five in a Row
# 15 x 15
# 0: Selectable Blank
# 1: Uneletable Blank
# 2: Black
# 3: White

class OutOfIndexError(Exception):    # Exception을 상속받아서 새로운 예외를 만듦
    def __init__(self):
        super().__init__('Size of array is 15 x 15 (0 - 14)')
        
class CanNotSelectError(Exception):    # Exception을 상속받아서 새로운 예외를 만듦
    def __init__(self):
        super().__init__('Can not set in this position')

def detect_unselectable_points():
    for row in range(ARRAY_SIZE):
        for col in range(ARRAY_SIZE):
            if array[row][col] == 0:
                point = (row, col)
                is33Rule = check_33_rule(point, point)
                is44Rule = check_44_rule(point, point)
                isOver5Rule = check_over_5_rule(point)
                if is33Rule or is44Rule or isOver5Rule:
                    array[row][col] = 1
                    unselectablePointList.append(point)
                elif array[row][col] == 0:
                    detect_unselectable_points_from_origin_point(point)
    return


def detect_unselectable_points_from_origin_point(originPoint):
    originRow, originCol = originPoint

    array[originRow][originCol] = 2
    directionList = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for direction in directionList:
        point = (originPoint[0] + direction[0], originPoint[1] + direction[1])
        row, col = point
        while is_out_of_array(point) == False and array[row][col] != 3:
            if array[row][col] == 2:
                is33Rule = check_33_rule(originPoint, point)
                is44Rule = check_44_rule(originPoint, point)
                if is33Rule or is44Rule:
                    originRow, originCol = originPoint
                    array[originRow][originCol] = 1
                    unselectablePointList.append(originPoint)
                    return
            point = (row + direction[0], col + direction[1])
            row, col = point

    array[originRow][originCol] = 0

def detect_selectable_points():
    removeList = []

    for point in unselectablePointList:
        is33Rule = check_33_rule(point, point)
        is44Rule = check_44_rule(point, point)
        isOver5Rule = check_over_5_rule(point)
        if (is33Rule == False and is44Rule == False and isOver5Rule == False):
            if detect_selectable_points_from_origin_point(point) == False:
                print("Restore Selectable!")
                removeList.append(point)
                row, col = point
                array[row][col] = 0
                pass

    for point in removeList:
        unselectablePointList.remove(point)


def detect_selectable_points_from_origin_point(originPoint):
    originRow, originCol = originPoint
    
    array[originRow][originCol] = 2
    directionList = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for direction in directionList:
        point = (originPoint[0] + direction[0], originPoint[1] + direction[1])
        row, col = point
        while is_out_of_array(point) == False and array[row][col] != 3:
            if array[row][col] == 2:
                is33Rule = check_33_rule(originPoint, point)
                is44Rule = check_44_rule(originPoint, point)
                if (is33Rule == True or is44Rule == True):
                    return True
            point = (row + direction[0], col + direction[1])
            row, col = point
    array[originRow][originCol] = 1
    return False

def check_33_rule(originPoint, point):
    global unselectablePointList

    row, col = point
    directionTupleList = [((1, 0), (-1, 0)), ((0, 1), (0, -1)), ((1, 1), (-1, -1)), ((1, -1), (-1, 1))]
    
    lineCount = 0
    for direction in directionTupleList:
        count1, isOpen1, is_blank_include1, blank_count1 = check_discountinuous_line_recursion(point, direction[0])
        count2, isOpen2, is_blank_include2, blank_count2 = check_discountinuous_line_recursion(point, direction[1], is_blank_include1)
        count = count1 + count2 + 1
        isOpen = isOpen1 and isOpen2

        if (count == 3 and isOpen):
            lineCount += 1
        
        if (lineCount == 2):
            print("Unselectable by 33!" + str(originPoint) + " " + str(point))
            return True
    return False

def check_44_rule(originPoint, point):
    global unselectablePointList

    originRow, originCol = originPoint
    row, col = point
    directionTupleList = [((1, 0), (-1, 0)), ((0, 1), (0, -1)), ((1, 1), (-1, -1)), ((1, -1), (-1, 1))]
    
    lineCount = 0
    for direction in directionTupleList:
        count1, isOpen1, is_blank_include1, blank_count1 = check_discountinuous_line_recursion(point, direction[0])
        count2, isOpen2, is_blank_include2, blank_count2 = check_discountinuous_line_recursion(point, direction[1], is_blank_include1)
        count = count1 + count2 + 1
        isOpen = isOpen1 or isOpen2
        
        if isOpen == False and blank_count1 + blank_count2 > 1:
            isOpen = True

        if (count == 4 and isOpen):
            lineCount += 1
        
        if (lineCount == 2):
            print("Unselectable by 44!" + str(originPoint) + " " + str(point))
            return True
    return False

def check_discountinuous_line_recursion(point, direction, is_include_blank = False, blank_count = 0):
    point = (point[0] + direction[0], point[1] + direction[1])
    row, col = point
    
    if blank_count >= 2:
        return (0, True, is_include_blank, blank_count)
    elif is_out_of_array(point) or array[row][col] == 3:
        return (0, False, is_include_blank, blank_count)
    elif array[row][col] == 0 or array[row][col] == 1:
        if is_include_blank:
            return (0, True, is_include_blank, blank_count + 1)
        else:
            _count, _isOpen, _is_include_blank, _blank_count = check_discountinuous_line_recursion(point, direction, is_include_blank, blank_count + 1)
            return (_count, True and _isOpen, _is_include_blank, _blank_count)
    else:
        if blank_count > 0:
            is_include_blank = True
        _count, _isOpen, _is_include_blank, _blank_count = check_discountinuous_line_recursion(point, direction, is_include_blank, blank_count)
        return (_count + 1, True and _isOpen, _is_include_blank, _blank_count)

def is_finished_game(leftSelectableCount, point, isWhiteTurn):
    # Need to Make Enum
    # 0: No Win, 1: Black Win, 2: White Win, 3: Draw

    if leftSelectableCount == 0:
        return 3
    elif check_lines(point, isWhiteTurn):
        return 2 if isWhiteTurn else 1 # Ternary Operator
    else:
        return 0

def check_lines(point, isWhiteTurn):
    row, col = point
    directionTupleList = [((1, 0), (-1, 0)), ((0, 1), (0, -1)), ((1, 1), (-1, -1)), ((1, -1), (-1, 1))]

    for direction in directionTupleList:
        userIndex = isWhiteTurn + 2
        count1 = check_continuous_line_recursion(point, direction[0], userIndex)
        count2 = check_continuous_line_recursion(point, direction[1], userIndex)
        count = count1 + count2 + 1

        if isWhiteTurn == False and count == 5:
            return True
        elif count >= 5:
            return True

    return False

def check_over_5_rule(point):
    row, col = point
    directionTupleList = [((1, 0), (-1, 0)), ((0, 1), (0, -1)), ((1, 1), (-1, -1)), ((1, -1), (-1, 1))]
    for direction in directionTupleList:
        userIndex = isWhiteTurn + 2
        count1 = check_continuous_line_recursion(point, direction[0], userIndex)
        count2 = check_continuous_line_recursion(point, direction[1], userIndex)
        count = count1 + count2 + 1

        if count > 5:
            print("Unselectable by over5!" + str(point))
            return True
    return False


def check_continuous_line_recursion(point, direction, userIndex):
    point = (point[0] + direction[0], point[1] + direction[1])
    row, col = point

    if is_out_of_array(point) or array[row][col] != userIndex:
        return 0
    else:
        return 1 + check_continuous_line_recursion(point, direction, userIndex)

def is_out_of_array(point):
    row, col = point
    return (row < 0 or ARRAY_SIZE - 1 < row) or (col < 0 or ARRAY_SIZE - 1 < col)

def print_array_shape():
    global array
    for row in range(ARRAY_SIZE):
        strVal = ""
        for col in range(ARRAY_SIZE):
            if array[row][col] == 0:
                strVal += ". "
            elif array[row][col] == 1:
                strVal += "X "
            elif array[row][col] == 2:
                strVal += "B "
            elif array[row][col] == 3:
                strVal += "W "
        print(strVal)
            

ARRAY_SIZE = 15

# Main Logic
array = [ [ 0 for i in range(ARRAY_SIZE) ] for j in range(ARRAY_SIZE)] 
totalBlankCount = ARRAY_SIZE * ARRAY_SIZE
leftSelectableCount = ARRAY_SIZE * ARRAY_SIZE

testBlackPreSettingList = [
    # (3, 3), 
    # (3, 4),
    # (3, 5), 
    # (3, 6),
    # (7, 6),

    # (6, 6),
    # (6, 7),
    # (6, 9),
    # (5, 8),
    # (8, 8),

    # (0, 1),
    # (0, 2),
    # (0, 3),
    # (1, 0),
    # (3, 0),

    (3, 3),
    (3, 4),
    (3, 5),
    # (4, 6),
    # (5, 6),
]

testWhitePreSettingList = [
    # (2, 6),
    # (8, 6)

    # (3, 8),
    # (10, 8),
]

testTurnList = [
    # (3, 3), 
    # (3, 4),
    # (3, 5),
    # (5, 5),

    # (7, 8),

    # (5, 5),
]

for row, col in testBlackPreSettingList:
    array[row][col] = 2

for row, col in testWhitePreSettingList:
    array[row][col] = 3

print_array_shape()

isChangeTurn = True

unselectablePointList = []
gameState = 0
isWhiteTurn = False
curTestTurnCount = 0
while gameState == 0:
    isCorrect = False
    while isCorrect == False:
        try:
            if curTestTurnCount < len(testTurnList):
                point = testTurnList[curTestTurnCount]
                curTestTurnCount += 1
            else:
                point = input("Input(row, col): ").split()

            # For Test
            if int(point[0]) == -1: # Maintain Turn
                print("Chane isChangeTurn: " + str(isChangeTurn) + " -> " + str(not isChangeTurn))
                isChangeTurn = not isChangeTurn
                continue
            elif int(point[0]) == -2:  # Change Turn Forcibly
                print("Change isWhiteTurn: " + str(isWhiteTurn) + " -> " + str(not isWhiteTurn))
                isWhiteTurn = not isWhiteTurn
                continue
            elif int(point[0]) == -3: # Quit Forcibly
                print("Quit Forcibly")
                sys.exit()
                
            row = int(point[0])
            col = int(point[1])
            if not(0 <= row and row <= 14) and not(0 <= col and col <= 14):
                raise OutOfIndexError
            if array[row][col] == 2 or array[row][col] == 3:
                raise CanNotSelectError
            if isWhiteTurn == False and array[row][col] == 1:
                raise CanNotSelectError
            isCorrect = True
        except Exception as e:
            print("[Exception]", e)

    totalBlankCount -= 1

    if isWhiteTurn and array[row][col] == 1:
        unselectablePointList.remove((row, col))

    userIndex = isWhiteTurn + 2
    print("userIndex: " + str(userIndex))
    array[row][col] = userIndex

    if isWhiteTurn == False:
        detect_unselectable_points()
    else:
        detect_selectable_points()
        pass

    leftSelectableCount = totalBlankCount - len(unselectablePointList)
    gameState = is_finished_game(leftSelectableCount, (row, col), isWhiteTurn)

    if isChangeTurn:
        isWhiteTurn = not isWhiteTurn

    print("Left Selectable Count: " + str(leftSelectableCount))
    print("Unselectable List: " + str(unselectablePointList))
    print_array_shape()

if gameState == 1:
    print("Black Win!")
elif gameState == 2:
    print("White Win")
elif gameState == 3:
    print("Draw")
else:
    print("Error")