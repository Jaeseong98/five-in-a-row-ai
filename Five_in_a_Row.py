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
    if option == 0:
        count_1, isOpen_1 = check_point_condition(point, 4, (1, 0))
        count_2, isOpen_2 = check_point_condition(point, 4, (-1, 0))
        print(count_1)
    elif option == 1:
        count_1, isOpen_1 = check_point_condition(point, 4, (0, 1))
        count_2, isOpen_2 = check_point_condition(point, 4, (0, -1))
        print(count_1)
    elif option == 2:
        count_1, isOpen_1 = check_point_condition(point, 4, (1, 1))
        count_2, isOpen_2 = check_point_condition(point, 4, (-1, -1))
        print(count_1)
    elif option == 3:
        count_1, isOpen_1 = check_point_condition(point, 4, (1, -1))
        count_2, isOpen_2 = check_point_condition(point, 4, (-1, 1))
        print(count_1)

def check_point_condition(point, n, different):
    row, col = point
    dif_row, dif_col = different
    nextPoint = (row + dif_row, col + dif_col)
    row, col = point
    
    if (n == 0):
        return (0, True)
    elif array[row][col] == 3 and (row < 0 or 14 > row) and (col < 0 or 14 > col):
        return (0, False)
    else:
        _count, _isOpen = check_point_condition(nextPoint, n - 1, different)
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