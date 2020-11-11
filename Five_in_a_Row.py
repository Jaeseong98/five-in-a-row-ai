# Five in a Row
# 15 x 15
# 0: Selectable Blank, 1: Non Seletable Blank 2: Black, 3: White

class OutOfIndexError(Exception):    # Exception을 상속받아서 새로운 예외를 만듦
    def __init__(self):
        super().__init__('Size of array is 15 x 15 (0 - 14)')
        
class CanNotSelectError(Exception):    # Exception을 상속받아서 새로운 예외를 만듦
    def __init__(self):
        super().__init__('Can not set in this position')

def update_points_state(point):
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
        totalCount = count1 + count2 + 1

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

def check_point_condition(point, n, different):
    point = (point[0] + different[0], point[1] + different[1])
    row, col = point

    print("Start Check Point Function " + str(row)  + " " + str(col) + " " + str(n))
    if (n == 0):
        print("True")
        return (0, True)
    elif (row < 0 or 14 < row) or (col < 0 or 14 < col) or array[row][col] == 3:
        print("False: " + str((row < 0 or 14 < row))  + " " + str((col < 0 or 14 < col)) + " " + str(array[row][col] == 3))
        return (0, False)   
    else:
        _count, _isOpen = check_point_condition(point, n - 1, different)
        return ((1 if array[row][col] == 2 else 0) + _count, (True and _isOpen))


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
        update_points_state((row, col))

    #isWhiteTurn = not isWhiteTurn