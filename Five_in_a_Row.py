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

def detect_unselectable_points(point):
    row, col = point
    for i in range(1, 6):
        detect_unselectable_points_using_origin_point((row + i, col))
        detect_unselectable_points_using_origin_point((row - i, col))
        detect_unselectable_points_using_origin_point((row, col + i))
        detect_unselectable_points_using_origin_point((row, col - i))
        detect_unselectable_points_using_origin_point((row + i, col + i))
        detect_unselectable_points_using_origin_point((row - i, col - i))
        detect_unselectable_points_using_origin_point((row + i, col - i))
        detect_unselectable_points_using_origin_point((row - i, col + i))
    return

def detect_unselectable_points_using_origin_point(originPoint):
    originRow, originCol = originPoint

    if is_out_of_array(originPoint) or array[originRow][originCol] != 0:
        return

    check_unselectable_rules(originPoint, originPoint)

    if array[originRow][originCol] == 0:
        array[originRow][originCol] = 2
        directionList = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for direction in directionList:
            point = (originPoint[0] + direction[0], originPoint[1] + direction[1])
            row, col = point
            while is_out_of_array(point) == False and array[row][col] == 2:
                check_unselectable_rules(originPoint, point)
                point = (row + direction[0], col + direction[1])
                row, col = point
                if array[originRow][originCol] == 1:
                    return
        array[originRow][originCol] = 0

def check_unselectable_rules(originPoint, point):
    global leftSelectableCount

    row, col = point
    directionList = [((1, 0), (-1, 0)), ((0, 1), (0, -1)), ((1, 1), (-1, -1)), ((1, -1), (-1, 1))]
    
    count33 = 0
    count44 = 0
    for direction in directionList:
        count1, isOpen1 = check_point_condition(point, direction[0])
        count2, isOpen2 = check_point_condition(point, direction[1])
        count = count1 + count2 + 1
        isOpen = isOpen1 and isOpen2

        if (count == 3 and isOpen):
            count33 += 1
        
        if (count == 4 and isOpen):
            count44 += 1
        
        if (count > 5 or count33 == 2 or count44 == 2):
            print("Unselectable!" + str(originPoint) + " " + str(point))
            originRow, originCol = originPoint
            array[originRow][originCol] = 1
            leftSelectableCount -= 1
            break
    return

def check_point_condition(point, direction, is_blank_include = False, blank_count = 0):
    point = (point[0] + direction[0], point[1] + direction[1])
    row, col = point
    
    #print("Start Check Point Function " + str(row)  + " " + str(col))
    if blank_count >= 2:
        return (0, True)
    elif is_out_of_array(point) or array[row][col] == 3:
        return (0, False)
    elif array[row][col] == 0 or array[row][col] == 1:
        if is_blank_include:
            return (0, True)
        else:
            _count, _isOpen = check_point_condition(point, direction, is_blank_include, blank_count + 1)
            return (_count, True and _isOpen)
    else:
        if blank_count > 0:
            is_blank_include = True
        _count, _isOpen = check_point_condition(point, direction, is_blank_include, blank_count)
        return (_count + 1, True and _isOpen)

def is_out_of_array(point):
    row, col = point
    return (row < 0 or 14 < row) or (col < 0 or 14 < col)

def is_finished_game(leftSelectableCount, point, isWhiteTurn):
    if leftSelectableCount == 0:
        return True
    else:
        return check_lines(point, isWhiteTurn)

def check_lines(point, isWhiteTurn):
    row, col = point
    directionList = [((1, 0), (-1, 0)), ((0, 1), (0, -1)), ((1, 1), (-1, -1)), ((1, -1), (-1, 1))]

    for direction in directionList:
        count1 = check_line_recursion(point, direction[0])
        count2 = check_line_recursion(point, direction[1])
        count = count1 + count2 + 1

        if count == 5 and isWhiteTurn == False:
            return True
        elif count >= 5:
            return True
    return False

def check_discountinuous_line_recursion(point, direction, is_blank_include = False, blank_count = 0):
    # TO DO ... (using check_point_condition() Method)
    pass

def check_continuous_line_recursion(point, direction):
    point = (point[0] + direction[0], point[1] + direction[1])
    row, col = point

    if is_out_of_array(point) or array[row][col] != 2:
        return 0
    else:
        return 1 + check_lines(point, direction)


# Main Logic
array = [ [ 0 for i in range(15) ] for j in range(15)]
for element in array:
        print(element)      
     
isWhiteTurn = False
leftSelectableCount = 225
point = (0, 0)

#while is_finished_game(leftSelectableCount, point, isWhiteTurn):
while True:
    isCorrect = False
    while isCorrect == False:
        try:
            point = input("Input(row, col): ").split()
            row = int(point[0])
            col = int(point[1])
            if not(0 <=row and row <= 14) and not(0 <= col and col <= 14):
                raise OutOfIndexError
            if array[row][col] == 2 or array[row][col] == 3:
                raise CanNotSelectError
            if isWhiteTurn == False and array[row][col] == 1:
                raise CanNotSelectError
            isCorrect = True
        except Exception as e:
            print("[Exception]", e)

    if array[row][col] == 0:
        leftSelectableCount -= 1

    userIndex = isWhiteTurn + 2
    array[row][col] = userIndex
        
    if isWhiteTurn == False:
        detect_unselectable_points((row, col))

    print("Left Selectable Count: " + str(leftSelectableCount))
    for element in array:
        print(element)

    #isWhiteTurn = not isWhiteTurn