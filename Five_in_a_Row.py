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

    if array[row][col] != 0:
        return
    
    print("Start Detecting Function")
    rule1Count = 0
    rule2Count = 0
    rule3Count = 0

    count_1, isOpen_1 = check_point_condition(point, 4, (1, 0))
    count_2, isOpen_2 = check_point_condition(point, 4, (-1, 0))
    totalCount = count_1 + count_2 + 1;
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
    totalCount = count_1 + count_2 + 1;
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
    totalCount = count_1 + count_2 + 1;
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
    totalCount = count_1 + count_2 + 1;
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

        

def check_point_condition(point, n, different):
    point = (point[0] + different[0], point[1] + different[1])
    row, col = point
    
    if (n == 0):
        return (0, True)
    elif (row < 0 or 14 > row) and (col < 0 or 14 > col) or array[row][col] == 3:
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

    isWhiteTurn = not isWhiteTurn