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

'''
def update_points_state(point):
    row, col = point
    for i in range(0, 14):
        detect_unselectable_point((row + i, col))
        detect_unselectable_point((row - i, col))
        detect_unselectable_point((row, col + i))
        detect_unselectable_point((row, col - i))
        detect_unselectable_point((row + i, col + i))
        detect_unselectable_point((row - i, col - i))
        detect_unselectable_point((row + i, col - i))
        detect_unselectable_point((row - i, col + i))
    return

def detect_unselectable_point(point):
    row, col = point
    directionList = [((1, 0), (-1, 0)), ((0, 1), (0, -1)), ((1, 1), (-1, -1)), ((1, -1), (-1, 1))]

    if array[row][col] != 0:
        return

    print("--------------------------------------------------")
    print("Start Detecting Function " + str(row)  + " " + str(col))
    rule1Count = 0
    rule2Count = 0
    for direction in directionList:
        count1, isOpen1 = check_point_condition(point, 4, direction[0])
        count2, isOpen2 = check_point_condition(point, 4, direction[1])
        count = count1 + count2 + 1
        isOpen = isOpen1 and isOpen2

        print("Result: " + str(count1)  + " " + str(count2) + " " + str(isOpen1) + " " + str(isOpen2))

        # Check 3 3 Rule
        if (totalCount == 3 and isOpen1 == True and isOpen2 == True):
            rule1Count += 1

        # Check 4 4 Rule
        if totalCount == 4:
            rule2Count += 1

        # Check Over Five in a Row Rule
        if rule1Count == 2 or rule2Count == 2 or totalCount > 5:
            array[row][col] = 1
            break
'''

def detect_unselectable_points():
    #row = 0
    for row in range(15):
        for col in range(15):
            if array[row][col] == 0:
                check_unselectable_rules((row, col))
    return

def check_unselectable_rules(point):
    row, col = point
    directionList = [((1, 0), (-1, 0)), ((0, 1), (0, -1)), ((1, 1), (-1, -1)), ((1, -1), (-1, 1))]
    
    count33 = 0
    count44 = 0
    for direction in directionList:
        count1, isOpen1 = check_point_condition(point, direction[0])
        count2, isOpen2 = check_point_condition(point, direction[1])
        count = count1 + count2 + 1
        isOpen = isOpen1 and isOpen2

        #print("Result: " + str(point) + " " + str(((count1, count2), (isOpen1, isOpen2))) + " " + str((count, isOpen)))
        if (count == 3 and isOpen):
            count33 += 1
        
        if (count == 4 and isOpen):
            count44 += 1
        
        if (count > 5 or count33 == 2 or count44 == 2):
            print("Unselectable!")
            array[row][col] = 1
            break
    return

def is_3x3_rule(point):
    row, col = point
    directionList = [((1, 0), (-1, 0)), ((0, 1), (0, -1)), ((1, 1), (-1, -1)), ((1, -1), (-1, 1))]
    
    count3x3 = 0
    for direction in directionList:
        count1, isOpen1 = check_point_condition(point, direction[0])
        count2, isOpen2 = check_point_condition(point, direction[1])
        count = count1 + count2 + 1
        isOpen = isOpen1 and isOpen2

        #print("Result: " + str(point) + " " + str(((count1, count2), (isOpen1, isOpen2))) + " " + str((count, isOpen)))
        if (count == 3 and isOpen):
            count3x3 += 1
        
        if (count3x3 == 2):
            print("Unselectable!")
            array[row][col] = 1
            break
    return

def is_4x4_rule(point):
    row, col = point
    directionList = [((1, 0), (-1, 0)), ((0, 1), (0, -1)), ((1, 1), (-1, -1)), ((1, -1), (-1, 1))]

    count = 0
    for direction in directionList:
        pass
    
    return

def is_over_five_rule(point):
    row, col = point
    directionList = [((1, 0), (-1, 0)), ((0, 1), (0, -1)), ((1, 1), (-1, -1)), ((1, -1), (-1, 1))]

    count = 0
    for direction in directionList:
        pass

    return

def check_point_condition(point, different, is_blank_include = False, blank_count = 0):
    point = (point[0] + different[0], point[1] + different[1])
    row, col = point
    
    #print("Start Check Point Function " + str(row)  + " " + str(col))
    if (blank_count >= 2):
        return (0, True)
    elif (is_out_of_array(point) or array[row][col] == 3):
        return (0, False)
    elif array[row][col] == 0 or array[row][col] == 1:
        if is_blank_include:
            return (0, True)
        else:
            _count, _isOpen = check_point_condition(point, different, is_blank_include, blank_count + 1)
            return (_count, True and _isOpen)
    else:
        if blank_count > 0:
            is_blank_include = True
        _count, _isOpen = check_point_condition(point, different, is_blank_include, blank_count)
        return (_count + 1, True and _isOpen)

def is_out_of_array(point):
    row, col = point
    return (row < 0 or 14 < row) or (col < 0 or 14 < col)


# Main Logic
array = [ [ 0 for i in range(15) ] for j in range(15)]
for element in array:
        print(element)      
     
isWhiteTurn = False

while True:
    isCorrect = False
    while isCorrect == False:
        try:
            row, col = input("Input(row, col): ").split()
            row = int(row)
            col = int(col)
            if not(0 <=row and row <= 14) and not(0 <= col and col <= 14):
                raise OutOfIndexError
            if array[row][col] == 2 or array[row][col] == 3:
                raise CanNotSelectError
            if isCorrect == False and array[row][col] == 1:
                raise CanNotSelectError
            isCorrect = True
        except Exception as e:
            print("[Exception]", e)

    userIndex = isWhiteTurn + 2
    array[row][col] = userIndex

    for element in array:
        print(element)
        
    if isWhiteTurn == False:
        #update_points_state((row, col))
        detect_unselectable_points()

    #isWhiteTurn = not isWhiteTurn